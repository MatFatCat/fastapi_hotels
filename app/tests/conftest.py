import asyncio
import json
import pytest
from app.database import Base, async_session_maker, engine
from app.config import settings
from app.users.models import Users
from app.hotels.models import Hotels
from app.hotels.rooms.models import Rooms
from app.bookings.models import Bookings
from sqlalchemy import insert
from datetime import datetime
from app.logging.logger import logger
from asyncio import BaseEventLoop


@pytest.fixture(autouse=True, scope="session")
async def prepare_database():

    logger.info(f"in prepare_database func {settings.MODE}")

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

