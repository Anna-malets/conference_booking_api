from fastapi import FastAPI
from typing import List
from models import ConferenceRoom, Booking
from schemas import RoomCreate, RoomUpdate, BookingCreate
from services import RoomService, BookingService

app = FastAPI(title="Conference Room Booking API", version="1.0")

room_service = RoomService()
booking_service = BookingService(room_service)

@app.post("/rooms", response_model=ConferenceRoom)
def add_room(room: RoomCreate):
    return room_service.add_room(room)

@app.put("/rooms/{room_id}", response_model=ConferenceRoom)
def update_room(room_id: int, room: RoomUpdate):
    return room_service.update_room(room_id, room)

@app.delete("/rooms/{room_id}")
def delete_room(room_id: int):
    room_service.delete_room(room_id)
    return {"message": "Room deleted successfully"}

@app.get("/rooms/search", response_model=List[ConferenceRoom])
def search_rooms(date: str, start_time: str, end_time: str, capacity: int):
    return room_service.search_rooms(date, start_time, end_time, capacity)

@app.post("/bookings", response_model=Booking)
def book_room(booking: BookingCreate):
    return booking_service.book_room(booking)

@app.get("/reports/popular-rooms")
def popular_rooms():
    return booking_service.report_popular_rooms()

@app.get("/reports/popular-services")
def popular_services():
    return booking_service.report_popular_services()

@app.get("/reports/monthly-revenue")
def monthly_revenue():
    return booking_service.report_monthly_revenue()
