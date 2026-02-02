"""
Pytest configuration and fixtures for Hotel Booking API tests.
"""
import pytest
from fastapi.testclient import TestClient
from main import app


@pytest.fixture
def client():
    """
    Create a test client for testing the FastAPI application.
    """
    return TestClient(app)


@pytest.fixture
def sample_room_data():
    """
    Sample room data for testing.
    """
    return {
        "name": "Test Suite Room",
        "description": "A luxurious test room",
        "price_per_night": 199.99,
        "image_url": "https://images.unsplash.com/photo-1590490360182-c33d57733427",
        "max_guests": 2,
        "amenities": ["WiFi", "TV", "Air Conditioning"]
    }


@pytest.fixture
def sample_booking_data():
    """
    Sample booking data for testing.
    Note: room_id will need to be set to a valid room ID from the database
    """
    return {
        "room_id": "1",
        "guest_name": "John Doe",
        "check_in_date": "2026-03-01",
        "check_out_date": "2026-03-05",
        "guests": 2
    }


@pytest.fixture
def invalid_booking_data():
    """
    Invalid booking data for testing validation.
    """
    return {
        "room_id": "999",  # Non-existent room
        "guest_name": "",  # Empty name
        "check_in_date": "2026-03-05",
        "check_out_date": "2026-03-01",  # Check-out before check-in
        "guests": 0  # Invalid guest count
    }
