from pydantic import BaseModel
from typing import List, Optional


class SRoom(BaseModel):
    id: int
    hotel_id: int
    name: str
    description: str
    services: List[str]
    price: int
    quantity: int
    image_id: Optional[int] = None
    total_cost: int
    rooms_left: int

    class Config:
        from_attributes = True
