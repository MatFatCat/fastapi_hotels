from sqlalchemy import update
from sqlalchemy.exc import SQLAlchemyError

from app.dao.base import BaseDAO
from app.database import async_session_maker
from app.users.models import Users
from app.exceptions import BookingException
from app.logging.logger import logger


# DAO - Data Access Object
class UsersDAO(BaseDAO):
    model = Users

    @classmethod
    async def _update_refresh_token(cls, user_id: int, token_refresh: str):
        try:
            async with async_session_maker() as session:
                query = (
                    update(cls.model)
                    .where(cls.model.id == user_id)
                    .values(token_refresh=token_refresh)
                )
                await session.execute(query)
                await session.commit()
        except (SQLAlchemyError, Exception) as error:
            logger.error(f"Some error accured in UsersDAO.update_refresh_token: {error}")
            raise BookingException
