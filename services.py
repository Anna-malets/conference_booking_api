from typing import List
from models import ConferenceRoom, Booking, Service
from schemas import RoomCreate, RoomUpdate, BookingCreate
import itertools
from collections import Counter, defaultdict
from datetime import datetime

class RoomService:
    def __init__(self):
        self.rooms: List[ConferenceRoom] = []
        self.counter = itertools.count(1)

    def add_room(self, room: RoomCreate) -> ConferenceRoom:
        new_room = ConferenceRoom(
            id=next(self.counter),
            name=room.name,
            capacity=room.capacity,
            base_price=room.base_price,
            services=[Service(**s.dict()) for s in room.services]
        )
        self.rooms.append(new_room)
        return new_room

    def update_room(self, room_id: int, room: RoomUpdate) -> ConferenceRoom:
        for r in self.rooms:
            if r.id == room_id:
                if room.name: r.name = room.name
                if room.capacity: r.capacity = room.capacity
                if room.base_price: r.base_price = room.base_price
                if room.services: r.services = [Service(**s.dict()) for s in room.services]
                return r
        raise ValueError("Room not found")

    def delete_room(self, room_id: int):
        self.rooms = [r for r in self.rooms if r.id != room_id]

    def search_rooms(self, date: str, start_time: str, end_time: str, capacity: int) -> List[ConferenceRoom]:
        return [r for r in self.rooms if r.capacity >= capacity]

class BookingService:
    def __init__(self, room_service: RoomService):
        self.bookings: List[Booking] = []
        self.counter = itertools.count(1)
        self.room_service = room_service

    def calculate_price(self, room: ConferenceRoom, duration: int, start_time: int, services: List[Service]) -> float:
        price = room.base_price * duration
        if 18 <= start_time < 23:
            price *= 0.8
        elif 6 <= start_time < 9:
            price *= 0.9
        elif 12 <= start_time < 14:
            price *= 1.15
        price += sum(s.price for s in services)
        return price

    def book_room(self, booking: BookingCreate) -> Booking:
        room = next((r for r in self.room_service.rooms if r.id == booking.room_id), None)
        if not room:
            raise ValueError("Room not found")

        duration = int(booking.end_time.split(":")[0]) - int(booking.start_time.split(":")[0])
        total_price = self.calculate_price(room, duration, int(booking.start_time.split(":")[0]),
                                           [Service(**s.dict()) for s in booking.services])

        new_booking = Booking(
            id=next(self.counter),
            room_id=room.id,
            date=booking.date,
            start_time=booking.start_time,
            end_time=booking.end_time,
            duration=duration,
            total_price=total_price,
            services=[Service(**s.dict()) for s in booking.services]
        )
        self.bookings.append(new_booking)
        return new_booking

    def report_popular_rooms(self):
        counter = Counter([b.room_id for b in self.bookings])
        return [{"room_id": room_id, "bookings": count} for room_id, count in counter.items()]

    def report_popular_services(self):
        counter = Counter([s.name for b in self.bookings for s in b.services])
        return [{"service": service, "count": count} for service, count in counter.items()]

    def report_monthly_revenue(self):
        revenue = defaultdict(float)
        for b in self.bookings:
            month = datetime.strptime(b.date, "%Y-%m-%d").strftime("%Y-%m")
            revenue[month] += b.total_price
        return [{"month": month, "revenue": total} for month, total in revenue.items()]
