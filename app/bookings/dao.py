from app.dao.base import BaseDAO
from app.bookings.models import Bookings


# DAO - Data Access Object
class BookingsDAO(BaseDAO):
    model = Bookings
