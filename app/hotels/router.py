from datetime import date

from fastapi import APIRouter
from fastapi_cache.decorator import cache

from app.exceptions import DateToLessThanDateFromException, NoSuchHotelException
from app.hotels.dao import HotelsDAO
from app.hotels.schemas import SHotel, SHotelWithRoomsLeft

hotels_router = APIRouter(prefix="/hotels", tags=["Отели"])


@hotels_router.get("/{location}")
@cache(expire=30)
async def get_hotels(
    location: str, date_from: date, date_to: date
) -> list[SHotelWithRoomsLeft]:
    if date_to < date_from:
        raise DateToLessThanDateFromException
    return await HotelsDAO.find_all(
        location=location, date_from=date_from, date_to=date_to
    )


@hotels_router.get("/id/{hotel_id}")
@cache(expire=30)
async def get_hotel_by_id(hotel_id: int) -> SHotel:
    hotel = await HotelsDAO.find_one_or_none(id=hotel_id)

    if not hotel:
        raise NoSuchHotelException

    return hotel
