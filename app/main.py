from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.bookings.router import booking_router
from app.hotels.router import hotels_router
from app.users.router import auth_router
from app.hotels.rooms.router import rooms_router
from app.pages.router import pages_router
from fastapi.staticfiles import StaticFiles
from app.images.router import images_router
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from collections.abc import AsyncIterator
from redis import asyncio as aioredis
from contextlib import asynccontextmanager
from app.config import settings


@asynccontextmanager
async def lifespan(_: FastAPI) -> AsyncIterator[None]:
    redis = aioredis.from_url(f"redis://{settings.REDIS_HOST}:{settings.REDIS_PORT}")
    FastAPICache.init(RedisBackend(redis), prefix="cache")
    yield


app = FastAPI(lifespan=lifespan)  # uvicorn app.main:app --reload
app.mount("/static", StaticFiles(directory="app/static"), "static")


app.include_router(auth_router)
app.include_router(booking_router)
app.include_router(hotels_router)
app.include_router(rooms_router)
app.include_router(pages_router)
app.include_router(images_router)


origins = [
    "http://localhost:3000"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS", "DELETE", "PATCH", "PUT"],
    allow_headers=["Content-Type", "Set-Cookie", "Access-Control-Allow-Headers", "Access-Control-Allow-Origin",
                   "Authorization"],
)
