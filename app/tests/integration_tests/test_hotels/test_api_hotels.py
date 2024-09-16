import pytest
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from httpx import AsyncClient
from redis import asyncio as aioredis

from app.config import settings
from app.logging.logger import logger


@pytest.mark.parametrize(
    "location,date_from,date_to,status_code,hotels_count",
    [
        ("New York", "2025-11-15", "2025-11-20", 200, 1),
        ("San Francisco", "2024-09-10", "2024-09-12", 200, 0),
        ("San Francisco", "2024-09-12", "2024-09-10", 409, 0),
    ],
)
async def test_get_hotels_by_location(
    location: str,
    date_from: str,
    date_to: str,
    status_code: int,
    hotels_count: int,
    ac: AsyncClient,
):
    redis = aioredis.from_url(f"redis://{settings.REDIS_HOST}:{settings.REDIS_PORT}")
    FastAPICache.init(RedisBackend(redis), prefix="cache")
    responce = await ac.get(
        f"/hotels/{location}?date_from={date_from}&date_to={date_to}"
    )
    assert responce.status_code == status_code
    if responce.status_code == 200:
        assert len(responce.json()) == hotels_count


@pytest.mark.parametrize("hotel_id,status_code", [(1, 200), (999, 404)])
async def test_get_hotels_by_hotels_id(
    hotel_id: int, status_code: int, ac: AsyncClient
):
    responce = await ac.get(f"/hotels/id/{hotel_id}")
    assert responce.status_code == status_code


@pytest.mark.parametrize(
    "hotel_id,date_from,date_to,status_code,rooms_count,total_cost",
    [
        (2, "2024-09-10", "2024-09-12", 200, 0, 800),
        (999, "2024-09-10", "2024-09-12", 404, 0, 800),
        (999, "2024-09-12", "2024-09-11", 409, 0, 800),
    ],
)
async def test_get_rooms_by_hotel_id(
    hotel_id: int,
    date_from: str,
    date_to: str,
    status_code: int,
    rooms_count: int,
    total_cost: int,
    ac: AsyncClient,
):
    response = await ac.get(
        f"/hotels/{hotel_id}/rooms?date_from={date_from}&date_to={date_to}"
    )
    assert response.status_code == status_code
    if status_code == 200:
        assert response.json()[0]["rooms_left"] == rooms_count
        assert response.json()[0]["total_cost"] == total_cost
