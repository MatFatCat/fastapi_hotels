from app.hotels.rooms.dao import RoomsDAO
from app.hotels.rooms.schemas import SRoom
from datetime import date
from app.hotels.router import hotels_router
from fastapi import APIRouter


rooms_router = APIRouter(
    prefix="/hotels",
    tags=["Отели"]
)


@rooms_router.get("/{hotel_id}/rooms")
async def get_rooms(hotel_id: int, date_from: date, date_to: date) -> list[SRoom]:
    return await RoomsDAO.find_all_by_hotel_id(hotel_id, date_from, date_to)
