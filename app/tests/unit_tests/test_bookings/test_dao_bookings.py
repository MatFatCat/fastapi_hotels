from app.bookings.dao import BookingsDAO
import pytest
from datetime import datetime


@pytest.mark.parametrize("user_id,room_id,date_from,date_to,accessible", [
    (2, 2, "2024-10-10", "2024-10-20", True),
    (1, 2, "2024-09-10", "2024-09-12", False),
])
async def test_add_get_booking(user_id, room_id, date_from, date_to,
                                   accessible):
    new_booking = await BookingsDAO.add(
        user_id,
        room_id,
        datetime.strptime(date_from, "%Y-%m-%d"),
        datetime.strptime(date_to, "%Y-%m-%d")
    )

    if accessible:
        assert new_booking.user_id == user_id
        assert new_booking.room_id == room_id
        assert str(new_booking.date_from) == date_from
        assert str(new_booking.date_to) == date_to

        new_booking = await BookingsDAO.find_by_id(new_booking.id)
        assert new_booking is not None

    else:
        assert not new_booking
