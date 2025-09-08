import pytest

@pytest.mark.asyncio
async def test_create_part_as_admin(client, admin_token):
    resp = await client.post(
        "/api/parts/",
        json={"partName": "Oil Filter", "partNumber": "OF-123"},
        headers={"Authorization": f"Bearer {admin_token}"}
    )
    assert resp.status_code == 201, resp.text
    data = resp.json()
    assert data["partName"] == "Oil Filter"
    assert data["partNumber"] == "OF-123"
    assert data["__v"] == 0

@pytest.mark.asyncio
async def test_create_part_duplicate(client, admin_token):
    # First creation
    await client.post(
        "/api/parts/",
        json={"partName": "Brake Pad", "partNumber": "BP-1"},
        headers={"Authorization": f"Bearer {admin_token}"}
    )
    # Duplicate name+number
    resp = await client.post(
        "/api/parts/",
        json={"partName": "Brake Pad", "partNumber": "BP-1"},
        headers={"Authorization": f"Bearer {admin_token}"}
    )
    assert resp.status_code in (409, 400)  # 409 preferred

@pytest.mark.asyncio
async def test_create_part_requires_admin(client, user_token):
    resp = await client.post(
        "/api/parts/",
        json={"partName": "Air Filter", "partNumber": "AF-22"},
        headers={"Authorization": f"Bearer {user_token}"}
    )
    assert resp.status_code in (401, 403)
