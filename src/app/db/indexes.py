# src/app/indexes.py
import logging
from typing import Optional, Dict, Any, Iterable, Tuple
from pymongo.errors import PyMongoError
from app.db.collections import users_collection, parts_collection, services_collection

logger = logging.getLogger("db.indexes")


def _normalize_index_key(idx_doc: Dict[str, Any]) -> Tuple[Tuple[str, int], ...]:
    # Normalize index "key" field (from list_indexes) to a tuple for stable comparison
    return tuple((k, v) for k, v in idx_doc.get("key", {}).items())


def _keys_tuple(keys: Iterable[Tuple[str, int]]) -> Tuple[Tuple[str, int], ...]:
    return tuple(keys)


def _dict_equal(a: Optional[Dict[str, Any]], b: Optional[Dict[str, Any]]) -> bool:
    return (a or {}) == (b or {})


async def _get_index_by_keys(coll, keys_tuple: Tuple[Tuple[str, int], ...]):
    """Find an existing index by its key spec, else None."""
    async for idx in coll.list_indexes():
        if _normalize_index_key(idx) == keys_tuple:
            return idx
    return None


async def _ensure_index(
    coll,
    keys: Iterable[Tuple[str, int]],
    *,
    unique: bool = False,
    partialFilterExpression: Optional[Dict[str, Any]] = None,
    name: Optional[str] = None,
    collation: Optional[Dict[str, Any]] = None,  # e.g. {"locale": "en", "strength": 2}
):
    """
    Ensure an index with given keys/options exists (idempotent).
    If an index with same keys exists but options differ (unique/partial/collation),
    drop & recreate with desired options.
    """
    keys_t = _keys_tuple(keys)
    existing = await _get_index_by_keys(coll, keys_t)

    def _options_match(existing_idx: Dict[str, Any]) -> bool:
        # Compare unique, partialFilterExpression, and collation
        if bool(existing_idx.get("unique", False)) != bool(unique):
            return False
        if not _dict_equal(existing_idx.get("partialFilterExpression"), partialFilterExpression):
            return False
        # list_indexes returns a "collation" dict when present
        if not _dict_equal(existing_idx.get("collation"), collation):
            return False
        return True

    if existing:
        if _options_match(existing):
            # Already correct
            return
        # Drop mismatched
        existing_name = existing.get("name")
        if existing_name:
            try:
                await coll.drop_index(existing_name)
                logger.info(f"Dropped outdated index '{existing_name}' on {coll.name}")
            except PyMongoError as e:
                logger.warning(
                    f"⚠️ Failed to drop index '{existing_name}' on collection '{coll.name}': {e}"
                )

    # Create desired
    kwargs: Dict[str, Any] = {}
    if unique:
        kwargs["unique"] = True
    if partialFilterExpression is not None:
        kwargs["partialFilterExpression"] = partialFilterExpression
    if name is not None:
        kwargs["name"] = name
    if collation is not None:
        kwargs["collation"] = collation

    try:
        await coll.create_index(list(keys), **kwargs)
        pretty = {
            "keys": list(keys),
            "unique": unique,
            "partialFilterExpression": partialFilterExpression,
            "collation": collation,
            "name": name,
        }
        logger.info(f"Created index on {coll.name}: {pretty}")
    except PyMongoError as e:
        logger.error(f"❌ Failed to create index on {coll.name}: {keys} | Error: {e}")


async def ensure_indexes() -> None:
    """
    Create/align all indexes. Safe to call at startup.
    Notes:
      - Users: case-insensitive unique username.
      - Parts: conditional unique rules for partName/partNumber.
      - Services: case-insensitive unique name among enabled services (enabled:true).
    """
    # USERS — case-insensitive unique username
    await _ensure_index(
        users_collection,
        [("username", 1)],
        unique=True,
        collation={"locale": "en", "strength": 2},  # case-insensitive
        name="uniq_username_ci",
    )

    # PARTS — unique (partName, partNumber) when partNumber is a real string
    await _ensure_index(
        parts_collection,
        [("partName", 1), ("partNumber", 1)],
        unique=True,
        partialFilterExpression={"partNumber": {"$type": "string"}},
        name="uniq_part_name_number_string",
    )

    # PARTS — unique partName when partNumber is null
    await _ensure_index(
        parts_collection,
        [("partName", 1)],
        unique=True,
        partialFilterExpression={"partNumber": None},
        name="uniq_part_name_when_number_null",
    )

    # SERVICES — case-insensitive unique name *only for enabled:true*
    # (allows reusing the same name after soft delete)
    await _ensure_index(
        services_collection,
        [("name", 1)],
        unique=True,
        partialFilterExpression={"enabled": True},
        collation={"locale": "en", "strength": 2},  # case-insensitive
        name="uniq_service_name_enabled_true_ci",
    )

    # Helpful secondary index for queries by enabled
    await _ensure_index(
        services_collection,
        [("enabled", 1)],
        name="services_enabled_idx",
    )
