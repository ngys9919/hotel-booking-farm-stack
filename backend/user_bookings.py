"""
User-specific booking endpoints.
"""
from fastapi import APIRouter, Depends, HTTPException
from typing import List
from models import BookingResponse
from auth import get_current_user
from database import bookings_collection

router = APIRouter(prefix="/api/user", tags=["User Bookings"])


@router.get("/bookings", response_model=List[BookingResponse])
async def get_user_bookings(current_user_email: str = Depends(get_current_user)):
    """
    Get all bookings for the authenticated user.
    
    Args:
        current_user_email: Email of the authenticated user (from JWT token)
        
    Returns:
        List of bookings made by the user
    """
    bookings = []
    async for booking in bookings_collection.find(
        {"user_email": current_user_email}
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
