from fastapi import FastAPI
from app.bookings.router import booking_router
from app.hotels.router import hotels_router

app = FastAPI()
app.include_router(booking_router)
app.include_router(hotels_router)
