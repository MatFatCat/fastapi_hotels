from fastapi import FastAPI
from app.bookings.router import booking_router
from app.hotels.router import hotels_router
from app.users.router import auth_router
from app.hotels.rooms.router import rooms_router

app = FastAPI()  # uvicorn app.main:app --reload

app.include_router(auth_router)
app.include_router(booking_router)
app.include_router(hotels_router)
app.include_router(rooms_router)