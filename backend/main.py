from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from datetime import datetime
from bson import ObjectId

from database import (
    connect_to_mongo,
    close_mongo_connection,
    rooms_collection,
    bookings_collection,
)
from models import (
    Room,
    RoomResponse,
    BookingCreate,
    Booking,
    BookingResponse,
)
from auth_routes import router as auth_router
from user_bookings import router as user_bookings_router
from admin_routes import router as admin_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    await connect_to_mongo()
    await initialize_sample_rooms()
    yield
    # Shutdown
    await close_mongo_connection()


app = FastAPI(
    title="Hotel Booking API",
    description="A modern hotel room booking system built with FastAPI and MongoDB",
    version="1.0.0",
    lifespan=lifespan,
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include authentication routes
app.include_router(auth_router)
app.include_router(user_bookings_router)
app.include_router(admin_router)


async def initialize_sample_rooms():
    """Initialize database with sample rooms if empty"""
    count = await rooms_collection.count_documents({})
    if count == 0:
        sample_rooms = [
            {
                "name": "Deluxe Ocean View Suite",
                "description": "Spacious suite with breathtaking ocean views, king-size bed, private balcony, and luxury amenities. Perfect for a romantic getaway.",
                "price_per_night": 299.99,
                "image_url": "https://images.unsplash.com/photo-1582719478250-c89cae4dc85b?w=800&q=80",
                "amenities": ["Ocean View", "King Bed", "Private Balcony", "Mini Bar", "WiFi"],
                "max_guests": 2,
            },
            {
                "name": "Executive Business Room",
                "description": "Modern room designed for business travelers with a comfortable workspace, high-speed internet, and premium coffee maker.",
                "price_per_night": 189.99,
                "image_url": "https://images.unsplash.com/photo-1566665797739-1674de7a421a?w=800&q=80",
                "amenities": ["Work Desk", "High-Speed WiFi", "Coffee Maker", "Queen Bed"],
                "max_guests": 2,
            },
            {
                "name": "Family Garden Suite",
                "description": "Spacious two-bedroom suite with garden access, perfect for families. Includes a living area and kitchenette.",
                "price_per_night": 349.99,
                "image_url": "https://images.unsplash.com/photo-1590490360182-c33d57733427?w=800&q=80",
                "amenities": ["2 Bedrooms", "Garden View", "Kitchenette", "Living Area", "WiFi"],
                "max_guests": 4,
            },
            {
                "name": "Cozy Standard Room",
                "description": "Comfortable and affordable room with all essential amenities. Perfect for solo travelers or couples on a budget.",
                "price_per_night": 129.99,
                "image_url": "https://images.unsplash.com/photo-1631049307264-da0ec9d70304?w=800&q=80",
                "amenities": ["Double Bed", "WiFi", "TV", "Air Conditioning"],
                "max_guests": 2,
            },
            {
                "name": "Presidential Penthouse",
                "description": "Ultimate luxury penthouse with panoramic city views, private terrace, jacuzzi, and personalized concierge service.",
                "price_per_night": 799.99,
                "image_url": "https://images.unsplash.com/photo-1578683010236-d716f9a3f461?w=800&q=80",
                "amenities": ["Panoramic View", "Private Terrace", "Jacuzzi", "Concierge", "King Bed", "WiFi"],
                "max_guests": 2,
            },
            {
                "name": "Mountain View Cabin",
                "description": "Rustic yet elegant cabin with stunning mountain views, fireplace, and a cozy atmosphere for nature lovers.",
                "price_per_night": 249.99,
                "image_url": "https://images.unsplash.com/photo-1596394516093-501ba68a0ba6?w=800&q=80",
                "amenities": ["Mountain View", "Fireplace", "Queen Bed", "WiFi", "Balcony"],
                "max_guests": 2,
            },
        ]
        await rooms_collection.insert_many(sample_rooms)
        print(f"✅ Initialized {len(sample_rooms)} sample rooms")


@app.get("/")
async def root():
    return {
        "message": "Welcome to Hotel Booking API",
        "version": "1.0.0",
        "endpoints": {
            "rooms": "/api/rooms",
            "bookings": "/api/bookings",
            "create_booking": "/api/bookings (POST)",
            "register": "/api/auth/register (POST)",
            "login": "/api/auth/login (POST)",
            "me": "/api/auth/me (GET - requires auth)",
        },
    }


@app.get("/api/rooms", response_model=list[RoomResponse])
async def get_rooms():
    """Get all available rooms"""
    rooms = []
    async for room in rooms_collection.find():
        rooms.append(
            RoomResponse(
                id=str(room["_id"]),
                name=room["name"],
                description=room["description"],
                price_per_night=room["price_per_night"],
                image_url=room["image_url"],
                amenities=room.get("amenities", []),
                max_guests=room.get("max_guests", 2),
            )
        )
    return rooms


@app.get("/api/rooms/{room_id}", response_model=RoomResponse)
async def get_room(room_id: str):
    """Get a specific room by ID"""
    if not ObjectId.is_valid(room_id):
        raise HTTPException(status_code=400, detail="Invalid room ID")

    room = await rooms_collection.find_one({"_id": ObjectId(room_id)})
    if not room:
        raise HTTPException(status_code=404, detail="Room not found")

    return RoomResponse(
        id=str(room["_id"]),
        name=room["name"],
        description=room["description"],
        price_per_night=room["price_per_night"],
        image_url=room["image_url"],
        amenities=room.get("amenities", []),
        max_guests=room.get("max_guests", 2),
    )


@app.post("/api/bookings", response_model=BookingResponse)
async def create_booking(booking: BookingCreate):
    """Create a new booking"""
    # Validate room exists
    if not ObjectId.is_valid(booking.room_id):
        raise HTTPException(status_code=400, detail="Invalid room ID")

    room = await rooms_collection.find_one({"_id": ObjectId(booking.room_id)})
    if not room:
        raise HTTPException(status_code=404, detail="Room not found")

    # Calculate total price
    try:
        check_in = datetime.fromisoformat(booking.check_in_date.replace("Z", "+00:00"))
        check_out = datetime.fromisoformat(booking.check_out_date.replace("Z", "+00:00"))
        nights = (check_out - check_in).days

        if nights <= 0:
            raise HTTPException(
                status_code=400, detail="Check-out date must be after check-in date"
            )

        total_price = nights * room["price_per_night"]
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid date format")

    # Create booking document
    booking_doc = {
        "room_id": booking.room_id,
        "room_name": room["name"],
        "guest_name": booking.guest_name,
        "check_in_date": booking.check_in_date,
        "check_out_date": booking.check_out_date,
        "guests": booking.guests,
        "total_price": total_price,
        "booking_date": datetime.utcnow(),
        "status": "confirmed",
        "user_email": booking.user_email,
    }

    result = await bookings_collection.insert_one(booking_doc)
    booking_doc["_id"] = result.inserted_id

    return BookingResponse(
        id=str(booking_doc["_id"]),
        room_id=booking_doc["room_id"],
        room_name=booking_doc["room_name"],
        guest_name=booking_doc["guest_name"],
        check_in_date=booking_doc["check_in_date"],
        check_out_date=booking_doc["check_out_date"],
        guests=booking_doc["guests"],
        total_price=booking_doc["total_price"],
        booking_date=booking_doc["booking_date"].isoformat(),
        status=booking_doc["status"],
        user_email=booking_doc.get("user_email"),
    )


@app.get("/api/bookings", response_model=list[BookingResponse])
async def get_all_bookings():
    """Get all bookings"""
    bookings = []
    async for booking in bookings_collection.find().sort("booking_date", -1):
        bookings.append(
            BookingResponse(
                id=str(booking["_id"]),
                room_id=booking["room_id"],
                room_name=booking["room_name"],
                guest_name=booking["guest_name"],
                check_in_date=booking["check_in_date"],
                check_out_date=booking["check_out_date"],
                guests=booking["guests"],
                total_price=booking["total_price"],
                booking_date=booking["booking_date"].isoformat(),
                status=booking["status"],
                user_email=booking.get("user_email"),
            )
        )
    return bookings


@app.get("/api/bookings/guest/{guest_name}", response_model=list[BookingResponse])
async def get_bookings_by_guest(guest_name: str):
    """Get bookings for a specific guest"""
    bookings = []
    async for booking in bookings_collection.find(
        {"guest_name": {"$regex": guest_name, "$options": "i"}}
    ).sort("booking_date", -1):
        bookings.append(
            BookingResponse(
                id=str(booking["_id"]),
                room_id=booking["room_id"],
                room_name=booking["room_name"],
                guest_name=booking["guest_name"],
                check_in_date=booking["check_in_date"],
                check_out_date=booking["check_out_date"],
                guests=booking["guests"],
                total_price=booking["total_price"],
                booking_date=booking["booking_date"].isoformat(),
                status=booking["status"],
                user_email=booking.get("user_email"),
            )
        )
    return bookings


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
