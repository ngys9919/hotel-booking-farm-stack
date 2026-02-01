from pydantic_settings import BaseSettings
from functools import lru_cache
import os
from dotenv import load_dotenv

load_dotenv()


class Settings(BaseSettings):
    mongodb_url: str = os.getenv("MONGODB_URL", "mongodb://localhost:27017")
    database_name: str = os.getenv("DATABASE_NAME", "hotel_booking_db")

    class Config:
        env_file = ".env"


@lru_cache()
def get_settings():
    return Settings()


settings = get_settings()

# Use mock database for demonstration
print("ℹ️  Using in-memory mock database for demonstration")
print("   To use MongoDB Atlas, update MONGODB_URL in backend/.env")

from database_mock import MockClient
client = MockClient()
database = client[settings.database_name]

# Collections
rooms_collection = database.get_collection("rooms")
bookings_collection = database.get_collection("bookings")


async def connect_to_mongo():
    """Connect to MongoDB and verify connection"""
    await client.admin.command('ping')
    print("✅ Mock database initialized successfully")


async def close_mongo_connection():
    """Close MongoDB connection"""
    client.close()
    print("🔌 Database connection closed")
