import pytest
from httpx import AsyncClient


@pytest.mark.parametrize("room_id,date_from,date_to,booked_rooms_quantity,status_code", [
    (1, "2025-05-05", "2025-05-15", 2, 200),
    (2, "2024-09-10", "2024-09-12", 1, 409),
    (2, "2024-09-09", "2024-09-11", 1, 409),
    (2, "2024-09-11", "2024-09-13", 1, 409)
])
async def test_add_and_get_booking_api(room_id, date_from, date_to, booked_rooms_quantity, status_code,
                                       authenticated_ac: AsyncClient):
    responce = await authenticated_ac.post("/bookings", params={
        "room_id": room_id,
        "date_from": date_from,
        "date_to": date_to
    }, cookies=authenticated_ac.cookies)

    assert responce.status_code == status_code

    responce = await authenticated_ac.get("/bookings")

    assert len(responce.json()) == booked_rooms_quantity
