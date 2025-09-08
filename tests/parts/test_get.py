import pytest

@pytest.mark.asyncio
async def test_get_parts_empty(client, user_token):
    resp = await client.get("/api/parts/", headers={"Authorization": f"Bearer {user_token}"})
    assert resp.status_code == 200
    assert resp.json() == []

@pytest.mark.asyncio
async def test_get_part_by_id(client, admin_token, user_token):
    # Create
    created = await client.post(
        "/api/parts/",
        json={"partName": "Belt", "partNumber": "B-9"},
        headers={"Authorization": f"Bearer {admin_token}"}
    )
    pid = created.json()["id"]

    # Fetch by id
    resp = await client.get(f"/api/parts/{pid}", headers={"Authorization": f"Bearer {user_token}"})
    assert resp.status_code == 200
    body = resp.json()
    assert body["id"] == pid
    assert body["partName"] == "Belt"

@pytest.mark.asyncio
async def test_get_part_by_id_not_found(client, user_token):
    resp = await client.get("/api/parts/66aabbccddeeff0011223344", headers={"Authorization": f"Bearer {user_token}"})
    assert resp.status_code in (400, 404)
