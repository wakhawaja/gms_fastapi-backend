import pytest

@pytest.mark.asyncio
async def test_create_service(client, admin_token):
    resp = await client.post(
        "/api/service/",
        json={"name": "Engine Tune", "enabled": True},
        headers={"Authorization": f"Bearer {admin_token}"}
    )
    assert resp.status_code == 201
    data = resp.json()
    assert data["name"] == "Engine Tune"
    assert data["enabled"] is True
    assert data["__v"] == 0

@pytest.mark.asyncio
async def test_create_service_duplicate(client, admin_token):
    await client.post(
        "/api/service/",
        json={"name": "Car Wash"},
        headers={"Authorization": f"Bearer {admin_token}"}
    )
    resp = await client.post(
        "/api/service/",
        json={"name": "Car Wash"},
        headers={"Authorization": f"Bearer {admin_token}"}
    )
    assert resp.status_code == 409
