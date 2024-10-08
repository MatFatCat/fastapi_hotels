from collections.abc import AsyncIterator
from contextlib import asynccontextmanager
import time

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from redis import asyncio as aioredis
from sqladmin import Admin
from fastapi import Request
from fastapi_versioning import VersionedFastAPI

from prometheus_fastapi_instrumentator import Instrumentator, metrics
import sentry_sdk

from app.admin.auth import authentication_backend
from app.admin.views import BookingsAdmin, HotelsAdmin, RoomsAdmin, UsersAdmin
from app.bookings.router import booking_router
from app.config import settings
from app.database import engine
from app.hotels.rooms.router import rooms_router
from app.hotels.router import hotels_router
from app.images.router import images_router
from app.pages.router import pages_router
from app.users.router import auth_router
from app.logging.logger import logger
from app.prometheus.router import router as prometheus_router

sentry_sdk.init(
    dsn="https://93db2b0e72a22e1a351b4bb380ff823b@o4507967134826496.ingest.de.sentry.io/4507967138234448",
    traces_sample_rate=1.0,
    profiles_sample_rate=1.0,
)


@asynccontextmanager
async def lifespan(_: FastAPI) -> AsyncIterator[None]:
    redis = aioredis.from_url(f"redis://{settings.REDIS_HOST}:{settings.REDIS_PORT}")
    FastAPICache.init(RedisBackend(redis), prefix="cache")
    yield

# -- FOR DEVELOPMENT STAGE --
#  uvicorn app.main:app --reload
#  celery -A app.tasks.celery_root:celery worker --loglevel=INFO
#  celery -A app.tasks.celery_root:celery flower

# -- FOR DEPLOY WITH DOCKER --
# docker-compose build
# docker-compose up
# you can check the dics of the 1st version of the API on localhost:7777/v1/docs
# check prometheus on localhost:9090
# check grafana dashboard on localhost:3000

#  pyright app/bookings/dao.py - example of using pyrigh lib for resolving errors in files
# also can use autoflake, flake8, black for reformatting code style

app = FastAPI(lifespan=lifespan)

app.include_router(auth_router)
app.include_router(booking_router)
app.include_router(hotels_router)
app.include_router(rooms_router)
app.include_router(pages_router)
app.include_router(images_router)
app.include_router(prometheus_router)

origins = ["http://localhost:3000", "http://test"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS", "DELETE", "PATCH", "PUT"],
    allow_headers=[
        "Content-Type",
        "Set-Cookie",
        "Access-Control-Allow-Headers",
        "Access-Control-Allow-Origin",
        "Authorization",
    ],
)

# app = VersionedFastAPI(app,
#                        version_format='{major}',
#                        prefix_format='/v{major}',
#                        description='API для бронирования отелей',
#                        )

instrumentator = Instrumentator(
    should_group_status_codes=False,
    excluded_handlers=[".*admin.*", "/metrics"]
)
instrumentator.instrument(app).expose(app)

app.mount("/static", StaticFiles(directory="app/static"), "static")

admin = Admin(app, engine, authentication_backend=authentication_backend)

admin.add_view(UsersAdmin)
admin.add_view(BookingsAdmin)
admin.add_view(HotelsAdmin)
admin.add_view(RoomsAdmin)
