import pytest

@pytest.mark.asyncio
async def test_get_services_empty(client, user_token):
    resp = await client.get("/api/service/", headers={"Authorization": f"Bearer {user_token}"})
    assert resp.status_code == 200
    assert resp.json() == []

@pytest.mark.asyncio
async def test_get_service_by_id(client, admin_token, user_token):
    created = await client.post(
        "/api/service/",
        json={"name": "Detailing"},
        headers={"Authorization": f"Bearer {admin_token}"}
    )
    sid = created.json()["id"]

    resp = await client.get(f"/api/service/{sid}", headers={"Authorization": f"Bearer {user_token}"})
    assert resp.status_code == 200
    assert resp.json()["id"] == sid
