from httpx import AsyncClient
import pytest


@pytest.mark.parametrize(
    "name,email,password,status_code",
    [
        ("Kevin", "kot@pes.com", "sompassword", 200),
        ("Kevin", "john.doe@example.com", "anotherpassword", 409),
        ("SomeUser", "wrongemail", "anotherpassword", 422),
    ],
)
async def test_register_user(
    name: str, email: str, password: str, status_code: int, ac: AsyncClient
):
    response = await ac.post(
        "/auth/register",
        json={
            "name": name,
            "email": email,
            "password": password,
        },
    )

    assert response.status_code == status_code


@pytest.mark.parametrize(
    "email,password,status_code",
    [
        ("john.doe@example.com", "test", 200),
        ("jane.smith@example.com", "test2", 200),
        ("john.doe@example.com", "somewrongpasswordofuser", 401),
    ],
)
async def test_login_user(email: str, password: str, status_code: int, ac: AsyncClient):
    responce = await ac.post("auth/login", json={"email": email, "password": password})

    assert responce.status_code == status_code


async def test_user_me(authenticated_ac: AsyncClient):
    response = await authenticated_ac.get("auth/me")
    assert response.status_code == 200
    assert response.json()["email"] == "jane.smith@example.com"
    assert response.json()["id"] == 2
