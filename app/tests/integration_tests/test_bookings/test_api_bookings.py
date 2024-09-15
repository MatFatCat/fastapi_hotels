import pytest
from httpx import AsyncClient
from app.logging.logger import logger


@pytest.mark.parametrize("room_id,date_from,date_to,booked_rooms_quantity,status_code", [
    (1, "2025-05-05", "2025-05-15", 2, 200),
    (2, "2024-09-10", "2024-09-12", 1, 409),
    (2, "2024-09-09", "2024-09-11", 1, 409),
    (2, "2024-09-11", "2024-09-13", 1, 409)
])
async def test_add_get_delete_booking_api(room_id, date_from, date_to, booked_rooms_quantity, status_code,
                                       authenticated_ac: AsyncClient):
    responce = await authenticated_ac.post("/bookings", params={
        "room_id": room_id,
        "date_from": date_from,
        "date_to": date_to
    })
    assert responce.status_code == status_code
    if responce.status_code == 200:
        booking_info = responce.json()
        booking_id = booking_info['id']
        responce = await authenticated_ac.get(f"/bookings/{booking_id}")
        assert responce.status_code == 200
        assert responce.json()['id'] == booking_id

    responce = await authenticated_ac.get("/bookings")
    assert responce.status_code == 200
    bookings = responce.json()
    assert len(bookings) == booked_rooms_quantity
    for booking in bookings:
        await authenticated_ac.delete(f"/bookings/{booking['id']}")
    bookings = await authenticated_ac.get("/bookings")
    assert bookings.status_code == 200
    assert not bookings.json()

