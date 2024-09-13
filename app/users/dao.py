from app.dao.base import BaseDAO
from app.users.models import Users
from app.database import async_session_maker
from sqlalchemy import update


# DAO - Data Access Object
class UsersDAO(BaseDAO):
    model = Users

    @classmethod
    async def update_refresh_token(cls, user_id: int, token_refresh: str):
        async with async_session_maker() as session:
            query = (
                update(cls.model)
                .where(cls.model.id == user_id)
                .values(token_refresh=token_refresh)
            )
            await session.execute(query)
            await session.commit()
