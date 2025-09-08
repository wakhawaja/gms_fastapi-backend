import pytest

@pytest.mark.asyncio
async def test_login_ok(client, seed_users):
    payload = {"username": "admin", "password": "adminpass"}
    resp = await client.post("/api/auth/login", json=payload)
    assert resp.status_code == 200
    data = resp.json()
    assert data["username"] == "admin"
    assert data["userType"] == "admin"
    assert isinstance(data["token"], str) and len(data["token"]) > 10

@pytest.mark.asyncio
async def test_login_invalid_username(client):
    resp = await client.post("/api/auth/login", json={"username": "nope", "password": "whatever"})
    assert resp.status_code == 401

@pytest.mark.asyncio
async def test_login_invalid_password(client, seed_users):
    resp = await client.post("/api/auth/login", json={"username": "admin", "password": "wrong"})
    assert resp.status_code == 401
