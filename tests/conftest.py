import os
import pytest
from typing import AsyncGenerator
from httpx import AsyncClient

from app.config.settings import settings
from app.core.security import hash_password
from app.core.jwt import create_access_token

# Import DB modules to patch the DB/collections to a test DB
from app.db.mongo import client as mongo_client
from app.db import indexes
from app.db import collections as db_collections
from app.db import mongo as db_mongo

from app.main import app


@pytest.fixture(scope="session", autouse=True)
def _use_test_db_name():
    """
    Force tests to use a dedicated test database (without touching production DB).
    """
    # If you want a completely separate DB name:
    test_db_name = f"{settings.MONGO_DB_NAME}_test"
    # Patch the db object to the test DB for the session
    test_db = mongo_client[test_db_name]

    # Reassign the global db in app.db.mongo
    db_mongo.db = test_db

    # Rewire collections module to test DB collections
    db_collections.users_collection = test_db.users
    db_collections.parts_collection = test_db.parts
    db_collections.services_collection = test_db.services

    yield

    # Drop the entire test DB at the end of the session
    mongo_client.drop_database(test_db_name)


@pytest.fixture(autouse=True)
async def _clean_db_between_tests():
    """
    Clean collections between tests and ensure indexes.
    """
    # Ensure indexes (idempotent)
    await indexes.ensure_indexes()

    # Clean data
    await db_collections.users_collection.delete_many({})
    await db_collections.parts_collection.delete_many({})
    await db_collections.services_collection.delete_many({})


@pytest.fixture
async def client() -> AsyncGenerator[AsyncClient, None]:
    async with AsyncClient(app=app, base_url="http://test") as ac:
        yield ac


@pytest.fixture
async def seed_users():
    """
    Insert one admin and one normal user for tests.
    Returns dict with inserted users.
    """
    admin = {
        "username": "admin",
        "userType": "admin",
        "passwordHash": hash_password("adminpass"),
    }
    user = {
        "username": "jane",
        "userType": "user",
        "passwordHash": hash_password("janepass"),
    }
    res_admin = await db_collections.users_collection.insert_one(admin)
    res_user = await db_collections.users_collection.insert_one(user)
    admin["_id"] = res_admin.inserted_id
    user["_id"] = res_user.inserted_id
    return {"admin": admin, "user": user}


@pytest.fixture
def admin_token(seed_users):
    """
    Generate JWT for the admin user (for protected routes).
    """
    admin = seed_users["admin"]
    token = create_access_token({
        "id": str(admin["_id"]),
        "username": admin["username"],
        "userType": admin["userType"],
    })
    return token


@pytest.fixture
def user_token(seed_users):
    user = seed_users["user"]
    token = create_access_token({
        "id": str(user["_id"]),
        "username": user["username"],
        "userType": user["userType"],
    })
    return token
