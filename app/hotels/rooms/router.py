from datetime import date
from typing import Optional, Union

from fastapi import APIRouter
from fastapi_cache.decorator import cache

from app.exceptions import DateToLessThanDateFromException, NoSuchHotelException
from app.hotels.rooms.dao import RoomsDAO
from app.hotels.rooms.schemas import SRoom

rooms_router = APIRouter(prefix="/hotels", tags=["Отели"])


@rooms_router.get("/{hotel_id}/rooms")
@cache(expire=30)
async def get_rooms(
    hotel_id: int, date_from: date, date_to: date
) -> Optional[list[SRoom]]:
    if date_to < date_from:
        raise DateToLessThanDateFromException
    rooms = await RoomsDAO.find_all_by_hotel_id(hotel_id, date_from, date_to)
    if not rooms:
        raise NoSuchHotelException

    return rooms
