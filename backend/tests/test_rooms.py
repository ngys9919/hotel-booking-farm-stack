"""
Test suite for room-related API endpoints.
"""
import pytest
from fastapi.testclient import TestClient


class TestRoomsEndpoints:
    """Test cases for /api/rooms endpoints."""

    def test_get_all_rooms(self, client: TestClient):
        """
        Test Case: GET /api/rooms - Retrieve all available rooms
        Expected: 200 OK with list of rooms
        """
        response = client.get("/api/rooms")
        
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        assert len(data) > 0
        
        # Verify room structure
        first_room = data[0]
        assert "id" in first_room
        assert "name" in first_room
        assert "description" in first_room
        assert "price" in first_room
        assert "image" in first_room
        assert "maxGuests" in first_room
        assert "amenities" in first_room

    def test_get_room_by_id_valid(self, client: TestClient):
        """
        Test Case: GET /api/rooms/{room_id} - Retrieve specific room by valid ID
        Expected: 200 OK with room details
        """
        room_id = 1
        response = client.get(f"/api/rooms/{room_id}")
        
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == room_id
        assert "name" in data
        assert "price" in data

    def test_get_room_by_id_invalid(self, client: TestClient):
        """
        Test Case: GET /api/rooms/{room_id} - Retrieve room with non-existent ID
        Expected: 404 Not Found
        """
        room_id = 9999
        response = client.get(f"/api/rooms/{room_id}")
        
        assert response.status_code == 404
        data = response.json()
        assert "detail" in data

    def test_rooms_data_integrity(self, client: TestClient):
        """
        Test Case: Verify data integrity of all rooms
        Expected: All rooms have valid data types and values
        """
        response = client.get("/api/rooms")
        rooms = response.json()
        
        for room in rooms:
            # Verify data types
            assert isinstance(room["id"], int)
            assert isinstance(room["name"], str)
            assert isinstance(room["description"], str)
            assert isinstance(room["price"], (int, float))
            assert isinstance(room["image"], str)
            assert isinstance(room["maxGuests"], int)
            assert isinstance(room["amenities"], list)
            
            # Verify valid values
            assert room["id"] > 0
            assert len(room["name"]) > 0
            assert room["price"] > 0
            assert room["maxGuests"] > 0
            assert len(room["amenities"]) > 0

    def test_rooms_price_range(self, client: TestClient):
        """
        Test Case: Verify all room prices are within reasonable range
        Expected: All prices between $50 and $1000 per night
        """
        response = client.get("/api/rooms")
        rooms = response.json()
        
        for room in rooms:
            assert 50 <= room["price"] <= 1000, \
                f"Room {room['name']} has price {room['price']} outside valid range"

    def test_rooms_unique_ids(self, client: TestClient):
        """
        Test Case: Verify all rooms have unique IDs
        Expected: No duplicate room IDs
        """
        response = client.get("/api/rooms")
        rooms = response.json()
        
        room_ids = [room["id"] for room in rooms]
        assert len(room_ids) == len(set(room_ids)), "Duplicate room IDs found"

    def test_rooms_image_urls(self, client: TestClient):
        """
        Test Case: Verify all room images have valid URLs
        Expected: All image URLs start with http:// or https://
        """
        response = client.get("/api/rooms")
        rooms = response.json()
        
        for room in rooms:
            assert room["image"].startswith(("http://", "https://")), \
                f"Room {room['name']} has invalid image URL: {room['image']}"
