from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from bson import ObjectId


class PyObjectId(ObjectId):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError("Invalid ObjectId")
        return ObjectId(v)

    @classmethod
    def __get_pydantic_json_schema__(cls, field_schema):
        field_schema.update(type="string")


class Room(BaseModel):
    id: Optional[PyObjectId] = Field(default=None, alias="_id")
    name: str
    description: str
    price_per_night: float
    image_url: str
    amenities: list[str] = []
    max_guests: int = 2

    class Config:
        populate_by_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}


class RoomResponse(BaseModel):
    id: str
    name: str
    description: str
    price_per_night: float
    image_url: str
    amenities: list[str]
    max_guests: int


class BookingCreate(BaseModel):
    room_id: str
    guest_name: str
    check_in_date: str
    check_out_date: str
    guests: int = 1


class Booking(BaseModel):
    id: Optional[PyObjectId] = Field(default=None, alias="_id")
    room_id: str
    room_name: str
    guest_name: str
    check_in_date: str
    check_out_date: str
    guests: int
    total_price: float
    booking_date: datetime = Field(default_factory=datetime.utcnow)
    status: str = "confirmed"

    class Config:
        populate_by_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str, datetime: lambda v: v.isoformat()}


class BookingResponse(BaseModel):
    id: str
    room_id: str
    room_name: str
    guest_name: str
    check_in_date: str
    check_out_date: str
    guests: int
    total_price: float
    booking_date: str
    status: str
