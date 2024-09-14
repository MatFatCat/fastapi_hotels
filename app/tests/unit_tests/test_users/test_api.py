from httpx import AsyncClient


async def test_register_user(ac: AsyncClient):
    response = await ac.post("/auth/register", json={
        "name": "Kevin Mitnik",
        "email": "kot@pes.com",
        "password": "sompassword",
    })

    assert response.status_code == 200
