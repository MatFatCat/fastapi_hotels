from app.dao.base import BaseDAO
from app.users.models import Users


# DAO - Data Access Object
class UsersDAO(BaseDAO):
    model = Users
