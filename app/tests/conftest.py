import asyncio
import json
import pytest
from app.database import Base, async_session_maker, engine
from app.users.models import Users
from app.hotels.models import Hotels
from app.hotels.rooms.models import Rooms
from app.bookings.models import Bookings
from sqlalchemy import insert
from datetime import datetime
from asyncio import BaseEventLoop
from httpx import AsyncClient
from app.main import app as fastapi_app
from app.config import settings


@pytest.fixture(autouse=True, scope="function")
async def prepare_database():
    assert settings.MODE == "TEST"

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

    def open_mock_json(model: str):
        with open(f"app/tests/mock_data/mock_{model}.json", "r") as file:
            return json.load(file)

    hotels = open_mock_json("hotels")
    rooms = open_mock_json("rooms")
    users = open_mock_json("users")
    bookings = open_mock_json("bookings")

    for booking in bookings:
        booking['date_from'] = datetime.strptime(booking['date_from'], "%Y-%m-%d")
        booking['date_to'] = datetime.strptime(booking['date_to'], "%Y-%m-%d")

    async with async_session_maker() as session:
        add_hotels_query = insert(Hotels).values(hotels)
        add_rooms_query = insert(Rooms).values(rooms)
        add_users_query = insert(Users).values(users)
        add_bookings_query = insert(Bookings).values(bookings)

        await session.execute(add_hotels_query)
        await session.execute(add_rooms_query)
        await session.execute(add_users_query)
        await session.execute(add_bookings_query)

        await session.commit()


@pytest.fixture(scope="session")
def event_loop(request) -> BaseEventLoop:
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="function")
async def ac():
    async with AsyncClient(app=fastapi_app, base_url="http://test") as ac:
        yield ac


@pytest.fixture(scope="session")
async def authenticated_ac():
    async with AsyncClient(app=fastapi_app, base_url="http://test") as ac:
        response = await ac.post("auth/login", json={
            "email": "jane.smith@example.com",
            "password": "test2"
        })

        assert response.status_code == 200
        assert ac.cookies["booking_access_token"]
        assert ac.cookies["booking_refresh_token"]

        yield ac


@pytest.fixture(scope="function")
async def session():
    async with async_session_maker() as session:
        yield session
