from pydantic import BaseModel
from typing import List, Optional


class SHotel(BaseModel):
    id: int
    name: str
    location: str
    services: List[str]
    rooms_quantity: int
    image_id: Optional[int] = None

    class Config:
        from_attributes = True
