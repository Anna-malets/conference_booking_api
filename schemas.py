from typing import List, Optional
from pydantic import BaseModel

class ServiceSchema(BaseModel):
    name: str
    price: float

class RoomCreate(BaseModel):
    name: str
    capacity: int
    base_price: float
    services: List[ServiceSchema] = []

class RoomUpdate(BaseModel):
    name: Optional[str]
    capacity: Optional[int]
    base_price: Optional[float]
    services: Optional[List[ServiceSchema]]

class BookingCreate(BaseModel):
    room_id: int
    date: str
    start_time: str
    end_time: str
    services: List[ServiceSchema] = []
