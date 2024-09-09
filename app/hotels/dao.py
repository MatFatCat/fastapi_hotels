from app.dao.base import BaseDAO
from app.hotels.models import Hotels


# DAO - Data Access Object
class HotelsDAO(BaseDAO):
    model = Hotels
