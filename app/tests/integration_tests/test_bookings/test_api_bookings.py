import pytest
from httpx import AsyncClient


@pytest.mark.parametrize("room_id,date_from,date_to,status_code", [
    (1, "2025-05-05", "2025-05-15", 200)
])
async def test_add_and_get_booking_api(room_id, date_from, date_to, status_code,
                                       authenticated_ac: AsyncClient):
    responce = await authenticated_ac.post("/bookings", params={
        "room_id": room_id,
        "date_from": date_from,
        "date_to": date_to
    }, cookies=authenticated_ac.cookies)

    assert responce.status_code == status_code
