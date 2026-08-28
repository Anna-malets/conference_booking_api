from typing import List
from pydantic import BaseModel

class Service(BaseModel):
    name: str
    price: float

class ConferenceRoom(BaseModel):
    id: int
    name: str
    capacity: int
    base_price: float
    services: List[Service] = []

class Booking(BaseModel):
    id: int
    room_id: int
    date: str
    start_time: str
    end_time: str
    duration: int
    total_price: float
    services: List[Service] = []
