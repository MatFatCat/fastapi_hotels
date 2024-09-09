from fastapi import APIRouter
from app.hotels.dao import HotelsDAO
from app.hotels.schemas import SHotel

hotels_router = APIRouter(
    prefix="/hotels",
    tags=["Отели"]
)


@hotels_router.get("")
async def get_hotels() -> list[SHotel]:
    return await HotelsDAO.find_all()
