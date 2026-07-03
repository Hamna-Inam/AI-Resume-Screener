import pytest


@pytest.mark.asyncio
async def test_register_user(client):
    response = await client.post("/v1/auth/register", json={
        "email": "newuser@test.com",
        "password": "testpass123",
        "role": "recruiter",
    })
    assert response.status_code == 201
    data = response.json()
    assert data["email"] == "newuser@test.com"
    assert "password" not in data
    assert "hashed_password" not in data


@pytest.mark.asyncio
async def test_register_duplicate_email_fails(client):
    await client.post("/v1/auth/register", json={
        "email": "dupe@test.com",
        "password": "testpass123",
        "role": "recruiter",
    })
    response = await client.post("/v1/auth/register", json={
        "email": "dupe@test.com",
        "password": "differentpass",
        "role": "recruiter",
    })
    assert response.status_code == 400


@pytest.mark.asyncio
async def test_login_success(client):
    await client.post("/v1/auth/register", json={
        "email": "logintest@test.com",
        "password": "mypassword",
        "role": "recruiter",
    })
    response = await client.post("/v1/auth/login", json={
        "email": "logintest@test.com",
        "password": "mypassword",
    })
    assert response.status_code == 200
    assert "access_token" in response.json()


@pytest.mark.asyncio
async def test_login_wrong_password_fails(client):
    await client.post("/v1/auth/register", json={
        "email": "wrongpass@test.com",
        "password": "correctpass",
        "role": "recruiter",
    })
    response = await client.post("/v1/auth/login", json={
        "email": "wrongpass@test.com",
        "password": "incorrectpass",
    })
    assert response.status_code == 401


@pytest.mark.asyncio
async def test_protected_route_requires_auth(client):
    response = await client.get("/v1/job-descriptions")
    assert response.status_code == 401