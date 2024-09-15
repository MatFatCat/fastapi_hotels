from app.hotels.rooms.dao import RoomsDAO
from app.hotels.rooms.schemas import SRoom
from datetime import date
from typing import Optional, Union
from fastapi import APIRouter
from app.exceptions import NoSuchHotelException
from fastapi import HTTPException


rooms_router = APIRouter(
    prefix="/hotels",
    tags=["Отели"]
)


@rooms_router.get("/{hotel_id}/rooms")
async def get_rooms(hotel_id: int, date_from: date, date_to: date) -> Optional[list[SRoom]]:
    rooms = await RoomsDAO.find_all_by_hotel_id(hotel_id, date_from, date_to)

    if not rooms:
        raise NoSuchHotelException

    return rooms

