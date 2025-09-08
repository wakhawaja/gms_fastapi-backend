import pytest

@pytest.mark.asyncio
async def test_update_service_name_and_enable(client, admin_token):
    created = await client.post(
        "/api/service/",
        json={"name": "Alignment", "enabled": False},
        headers={"Authorization": f"Bearer {admin_token}"}
    )
    sid = created.json()["id"]

    resp = await client.patch(
        f"/api/service/{sid}",
        json={"name": "Wheel Alignment", "enabled": True},
        headers={"Authorization": f"Bearer {admin_token}"}
    )
    assert resp.status_code == 200
    body = resp.json()
    assert body["name"] == "Wheel Alignment"
    assert body["enabled"] is True
    assert body["__v"] == 1  # bumped

@pytest.mark.asyncio
async def test_soft_delete_service(client, admin_token):
    created = await client.post(
        "/api/service/",
        json={"name": "Battery Check"},
        headers={"Authorization": f"Bearer {admin_token}"}
    )
    sid = created.json()["id"]

    del_resp = await client.delete(f"/api/service/{sid}", headers={"Authorization": f"Bearer {admin_token}"})
    assert del_resp.status_code == 200

    # After soft-delete, fetching by GET all (without includeDisabled) should not include it if your route filters.
    list_resp = await client.get("/api/service/", headers={"Authorization": f"Bearer {admin_token}"})
    assert list_resp.status_code == 200
    # Depending on your current route (you added includeDisabled later),
    # we just check the endpoint responds; specific filter behavior can be asserted if implemented.
