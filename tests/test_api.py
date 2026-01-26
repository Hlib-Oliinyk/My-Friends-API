import pytest
import pytest_asyncio
from httpx import AsyncClient, ASGITransport
from main import app


@pytest_asyncio.fixture
async def async_client():
    async with AsyncClient(
        transport=ASGITransport(app),
        base_url="http://test"
    ) as ac:
        yield ac


@pytest_asyncio.fixture
async def async_auth_client():
    async with AsyncClient(
        transport=ASGITransport(app),
        base_url="http://test"
    ) as ac:
        response = await ac.post("/auth/login", json={
            "email": "glib@gmail.com",
            "password": "77777777"
        })

        token = response.json()["access_token"]

        ac.headers.update({
            "Authorization": f"Bearer {token}"
        })
        yield ac


@pytest.mark.asyncio
async def test_get_users(async_client):
    response = await async_client.get("/users/")
    assert response.status_code == 200

    data = response.json()
    assert len(data) != 0


@pytest.mark.asyncio
async def test_login(async_client):
    response = await async_client.post("/auth/login", json={
        "email": "glib@gmail.com",
        "password": "77777777"
    })
    assert response.status_code == 200


@pytest.mark.asyncio
async def test_get_all_friends_error(async_client):
    response = await async_client.get("/friends/")
    assert response.status_code == 401


@pytest.mark.asyncio
async def test_get_all_friends(async_auth_client):
    response = await async_auth_client.get("/friends/")
    assert response.status_code == 200

    data = response.json()
    print(data)


@pytest.mark.asyncio
async def test_get_friend(async_auth_client):
    response = await async_auth_client.get("/friends/3")
    assert response.status_code == 200

    data = response.json()
    print(data)


@pytest.mark.asyncio
async def test_get_all_user_friend_groups_error(async_client):
    response = await async_client.get("/friend_groups/")
    assert response.status_code == 401


@pytest.mark.asyncio
async def test_get_all_user_friend_groups(async_auth_client):
    response = await async_auth_client.get("/friend_groups/")
    assert response.status_code == 200

    data = response.json()
    print(data)