import pytest

@pytest.mark.asyncio
async def test_update_part(client, admin_token):
    # Create
    created = await client.post(
        "/api/parts/",
        json={"partName": "Plug", "partNumber": "P-1"},
        headers={"Authorization": f"Bearer {admin_token}"}
    )
    body = created.json()
    pid = body["id"]
    assert body["__v"] == 0

    # Update name and number
    resp = await client.put(
        f"/api/parts/{pid}",
        json={"partName": "Spark Plug", "partNumber": "SP-2"},
        headers={"Authorization": f"Bearer {admin_token}"}
    )
    assert resp.status_code == 200
    updated = resp.json()
    assert updated["partName"] == "Spark Plug"
    assert updated["partNumber"] == "SP-2"
    assert updated["__v"] == 1  # version bumped

@pytest.mark.asyncio
async def test_delete_part(client, admin_token):
    created = await client.post(
        "/api/parts/",
        json={"partName": "Gasket", "partNumber": "G-7"},
        headers={"Authorization": f"Bearer {admin_token}"}
    )
    pid = created.json()["id"]

    del_resp = await client.delete(f"/api/parts/{pid}", headers={"Authorization": f"Bearer {admin_token}"})
    assert del_resp.status_code == 200

    get_resp = await client.get(f"/api/parts/{pid}", headers={"Authorization": f"Bearer {admin_token}"})
    assert get_resp.status_code == 404
