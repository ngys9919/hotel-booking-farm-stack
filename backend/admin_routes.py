"""
Admin API routes for user and booking management.
Requires admin role for access.
"""
from fastapi import APIRouter, Depends, HTTPException, status
from typing import List, Optional
from models import UserResponse, BookingResponse, User
from auth import get_current_admin_user
from database import users_collection, bookings_collection, get_database
from user_db import get_user_by_email, user_to_response
from bson import ObjectId
from datetime import datetime

router = APIRouter(prefix="/api/admin", tags=["Admin"])


# ==================== User Management ====================

@router.get("/users", response_model=List[UserResponse])
async def get_all_users(
    skip: int = 0,
    limit: int = 100,
    admin_email: str = Depends(get_current_admin_user)
):
    """
    Get all users (admin only).
    
    Args:
        skip: Number of users to skip (pagination)
        limit: Maximum number of users to return
        admin_email: Email of the admin user (from JWT token)
        
    Returns:
        List of all users
    """
    users = []
    async for user_data in users_collection.find().skip(skip).limit(limit).sort("created_at", -1):
        user_data["_id"] = str(user_data["_id"])
        user = User(**user_data)
        users.append(user_to_response(user))
    
    return users


@router.get("/users/{user_id}", response_model=UserResponse)
async def get_user_by_id(
    user_id: str,
    admin_email: str = Depends(get_current_admin_user)
):
    """
    Get a specific user by ID (admin only).
    
    Args:
        user_id: User's ID
        admin_email: Email of the admin user (from JWT token)
        
    Returns:
        User information
    """
    try:
        user_data = await users_collection.find_one({"_id": ObjectId(user_id)})
    except:
        # If ObjectId conversion fails, try as string
        user_data = await users_collection.find_one({"_id": user_id})
    
    if not user_data:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    user_data["_id"] = str(user_data["_id"])
    user = User(**user_data)
    return user_to_response(user)


@router.patch("/users/{user_id}")
async def update_user(
    user_id: str,
    update_data: dict,
    admin_email: str = Depends(get_current_admin_user)
):
    """
    Update user information (admin only).
    
    Args:
        user_id: User's ID
        update_data: Fields to update
        admin_email: Email of the admin user (from JWT token)
        
    Returns:
        Updated user information
    """
    # Remove fields that shouldn't be updated directly
    update_data.pop("_id", None)
    update_data.pop("id", None)
    update_data.pop("hashed_password", None)
    update_data.pop("created_at", None)
    
    try:
        result = await users_collection.update_one(
            {"_id": ObjectId(user_id)},
            {"$set": update_data}
        )
    except:
        result = await users_collection.update_one(
            {"_id": user_id},
            {"$set": update_data}
        )
    
    if result.matched_count == 0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    # Get updated user
    try:
        user_data = await users_collection.find_one({"_id": ObjectId(user_id)})
    except:
        user_data = await users_collection.find_one({"_id": user_id})
    
    user_data["_id"] = str(user_data["_id"])
    user = User(**user_data)
    return user_to_response(user)


@router.delete("/users/{user_id}")
async def delete_user(
    user_id: str,
    admin_email: str = Depends(get_current_admin_user)
):
    """
    Delete a user (admin only).
    
    Args:
        user_id: User's ID
        admin_email: Email of the admin user (from JWT token)
        
    Returns:
        Success message
    """
    try:
        result = await users_collection.delete_one({"_id": ObjectId(user_id)})
    except:
        result = await users_collection.delete_one({"_id": user_id})
    
    if result.deleted_count == 0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    return {"message": "User deleted successfully", "user_id": user_id}


# ==================== Booking Management ====================

@router.get("/bookings", response_model=List[BookingResponse])
async def get_all_bookings(
    skip: int = 0,
    limit: int = 100,
    status: Optional[str] = None,
    admin_email: str = Depends(get_current_admin_user)
):
    """
    Get all bookings (admin only).
    
    Args:
        skip: Number of bookings to skip (pagination)
        limit: Maximum number of bookings to return
        status: Filter by booking status (optional)
        admin_email: Email of the admin user (from JWT token)
        
    Returns:
        List of all bookings
    """
    query = {}
    if status:
        query["status"] = status
    
    bookings = []
    async for booking in bookings_collection.find(query).skip(skip).limit(limit).sort("booking_date", -1):
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


@router.get("/bookings/{booking_id}", response_model=BookingResponse)
async def get_booking_by_id(
    booking_id: str,
    admin_email: str = Depends(get_current_admin_user)
):
    """
    Get a specific booking by ID (admin only).
    
    Args:
        booking_id: Booking's ID
        admin_email: Email of the admin user (from JWT token)
        
    Returns:
        Booking information
    """
    try:
        booking = await bookings_collection.find_one({"_id": ObjectId(booking_id)})
    except:
        booking = await bookings_collection.find_one({"_id": booking_id})
    
    if not booking:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Booking not found"
        )
    
    return BookingResponse(
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


@router.patch("/bookings/{booking_id}")
async def update_booking_status(
    booking_id: str,
    update_data: dict,
    admin_email: str = Depends(get_current_admin_user)
):
    """
    Update booking information (admin only).
    Commonly used to update booking status.
    
    Args:
        booking_id: Booking's ID
        update_data: Fields to update (e.g., {"status": "cancelled"})
        admin_email: Email of the admin user (from JWT token)
        
    Returns:
        Updated booking information
    """
    # Remove fields that shouldn't be updated
    update_data.pop("_id", None)
    update_data.pop("id", None)
    update_data.pop("booking_date", None)
    
    try:
        result = await bookings_collection.update_one(
            {"_id": ObjectId(booking_id)},
            {"$set": update_data}
        )
    except:
        result = await bookings_collection.update_one(
            {"_id": booking_id},
            {"$set": update_data}
        )
    
    if result.matched_count == 0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Booking not found"
        )
    
    # Get updated booking
    try:
        booking = await bookings_collection.find_one({"_id": ObjectId(booking_id)})
    except:
        booking = await bookings_collection.find_one({"_id": booking_id})
    
    return BookingResponse(
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


@router.delete("/bookings/{booking_id}")
async def delete_booking(
    booking_id: str,
    admin_email: str = Depends(get_current_admin_user)
):
    """
    Delete a booking (admin only).
    
    Args:
        booking_id: Booking's ID
        admin_email: Email of the admin user (from JWT token)
        
    Returns:
        Success message
    """
    try:
        result = await bookings_collection.delete_one({"_id": ObjectId(booking_id)})
    except:
        result = await bookings_collection.delete_one({"_id": booking_id})
    
    if result.deleted_count == 0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Booking not found"
        )
    
    return {"message": "Booking deleted successfully", "booking_id": booking_id}


# ==================== Statistics ====================

@router.get("/stats")
async def get_admin_stats(admin_email: str = Depends(get_current_admin_user)):
    """
    Get admin dashboard statistics (admin only).
    
    Args:
        admin_email: Email of the admin user (from JWT token)
        
    Returns:
        Dashboard statistics
    """
    # Count users
    total_users = await users_collection.count_documents({})
    active_users = await users_collection.count_documents({"is_active": True})
    admin_users = await users_collection.count_documents({"role": "admin"})
    
    # Count bookings
    total_bookings = await bookings_collection.count_documents({})
    confirmed_bookings = await bookings_collection.count_documents({"status": "confirmed"})
    cancelled_bookings = await bookings_collection.count_documents({"status": "cancelled"})
    
    # Calculate total revenue
    pipeline = [
        {"$match": {"status": "confirmed"}},
        {"$group": {"_id": None, "total": {"$sum": "$total_price"}}}
    ]
    revenue_result = await bookings_collection.aggregate(pipeline).to_list(1)
    total_revenue = revenue_result[0]["total"] if revenue_result else 0
    
    return {
        "users": {
            "total": total_users,
            "active": active_users,
            "admins": admin_users
        },
        "bookings": {
            "total": total_bookings,
            "confirmed": confirmed_bookings,
            "cancelled": cancelled_bookings
        },
        "revenue": {
            "total": round(total_revenue, 2),
            "currency": "USD"
        }
    }
