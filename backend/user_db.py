"""
User database operations for authentication.
"""
from typing import Optional
from motor.motor_asyncio import AsyncIOMotorDatabase
from models import User, UserCreate, UserResponse
from auth import get_password_hash, verify_password
from bson import ObjectId
from datetime import datetime
from database import users_collection


# Mock in-memory user database for testing
mock_users_db = {}


async def get_user_by_email(db: Optional[AsyncIOMotorDatabase], email: str) -> Optional[User]:
    """
    Get a user by email address.
    
    Args:
        db: MongoDB database instance (or None for mock)
        email: User's email address
        
    Returns:
        User object if found, None otherwise
    """
    if db is None:
        # Use mock database
        user_data = mock_users_db.get(email)
        if user_data:
            return User(**user_data)
        return None
    
    # Use real MongoDB
    user_data = await users_collection.find_one({"email": email})
    if user_data:
        user_data["_id"] = str(user_data["_id"])  # Convert ObjectId to string
        return User(**user_data)
    return None


async def create_user(db: Optional[AsyncIOMotorDatabase], user_data: UserCreate) -> User:
    """
    Create a new user.
    
    Args:
        db: MongoDB database instance (or None for mock)
        user_data: User registration data
        
    Returns:
        Created User object
        
    Raises:
        ValueError: If user already exists
    """
    # Check if user already exists
    existing_user = await get_user_by_email(db, user_data.email)
    if existing_user:
        raise ValueError("User with this email already exists")
    
    # Hash the password
    hashed_password = get_password_hash(user_data.password)
    
    # Create user object
    user = User(
        email=user_data.email,
        hashed_password=hashed_password,
        full_name=user_data.full_name,
        is_active=True,
        created_at=datetime.utcnow()
    )
    
    if db is None:
        # Use mock database
        user_id = str(ObjectId())
        user_dict = user.model_dump()
        user_dict["_id"] = user_id
        user_dict["id"] = user_id
        mock_users_db[user_data.email] = user_dict
        return User(**user_dict)
    
    # Use real MongoDB
    result = await users_collection.insert_one(user.model_dump(by_alias=True, exclude=["id"]))
    user_dict = user.model_dump()
    user_dict["_id"] = str(result.inserted_id)  # Convert ObjectId to string
    return User(**user_dict)


async def authenticate_user(db: Optional[AsyncIOMotorDatabase], email: str, password: str) -> Optional[User]:
    """
    Authenticate a user with email and password.
    
    Args:
        db: MongoDB database instance (or None for mock)
        email: User's email address
        password: User's password
        
    Returns:
        User object if authentication successful, None otherwise
    """
    user = await get_user_by_email(db, email)
    if not user:
        return None
    
    if not verify_password(password, user.hashed_password):
        return None
    
    return user


async def update_user(db: Optional[AsyncIOMotorDatabase], email: str, update_data: dict) -> Optional[User]:
    """
    Update user information.
    
    Args:
        db: MongoDB database instance (or None for mock)
        email: User's email address
        update_data: Dictionary of fields to update
        
    Returns:
        Updated User object if successful, None otherwise
    """
    if db is None:
        # Use mock database
        if email not in mock_users_db:
            return None
        
        mock_users_db[email].update(update_data)
        return User(**mock_users_db[email])
    
    # Use real MongoDB
    result = await db.users.find_one_and_update(
        {"email": email},
        {"$set": update_data},
        return_document=True
    )
    
    if result:
        return User(**result)
    return None


def user_to_response(user: User) -> UserResponse:
    """
    Convert User model to UserResponse (without password).
    
    Args:
        user: User object
        
    Returns:
        UserResponse object
    """
    return UserResponse(
        id=str(user.id) if user.id else "",
        email=user.email,
        full_name=user.full_name,
        role=user.role,
        is_active=user.is_active,
        created_at=user.created_at.isoformat() if isinstance(user.created_at, datetime) else user.created_at
    )
