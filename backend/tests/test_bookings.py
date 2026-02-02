"""
Test suite for booking-related API endpoints.
"""
import pytest
from fastapi.testclient import TestClient


class TestBookingsEndpoints:
    """Test cases for /api/bookings endpoints."""

    def test_create_booking_valid(self, client: TestClient, sample_booking_data):
        """
        Test Case: POST /api/bookings - Create a new booking with valid data
        Expected: 200 OK with booking confirmation
        """
        response = client.post("/api/bookings", json=sample_booking_data)
        
        assert response.status_code == 200
        data = response.json()
        assert "id" in data
        assert data["guestName"] == sample_booking_data["guestName"]
        assert data["roomId"] == sample_booking_data["roomId"]
        assert data["totalPrice"] == sample_booking_data["totalPrice"]

    def test_create_booking_missing_fields(self, client: TestClient):
        """
        Test Case: POST /api/bookings - Create booking with missing required fields
        Expected: 422 Unprocessable Entity
        """
        incomplete_data = {
            "roomId": 1,
            "guestName": "Jane Doe"
            # Missing checkIn, checkOut, guests, totalPrice
        }
        response = client.post("/api/bookings", json=incomplete_data)
        
        assert response.status_code == 422

    def test_create_booking_invalid_room_id(self, client: TestClient):
        """
        Test Case: POST /api/bookings - Create booking with non-existent room ID
        Expected: 404 Not Found
        """
        invalid_booking = {
            "roomId": 9999,
            "guestName": "Test User",
            "checkIn": "2026-03-01",
            "checkOut": "2026-03-05",
            "guests": 2,
            "totalPrice": 999.99
        }
        response = client.post("/api/bookings", json=invalid_booking)
        
        assert response.status_code == 404

    def test_create_booking_invalid_dates(self, client: TestClient):
        """
        Test Case: POST /api/bookings - Create booking with check-out before check-in
        Expected: 400 Bad Request
        """
        invalid_dates_booking = {
            "roomId": 1,
            "guestName": "Test User",
            "checkIn": "2026-03-10",
            "checkOut": "2026-03-05",  # Before check-in
            "guests": 2,
            "totalPrice": 999.99
        }
        response = client.post("/api/bookings", json=invalid_dates_booking)
        
        assert response.status_code == 400

    def test_get_all_bookings(self, client: TestClient, sample_booking_data):
        """
        Test Case: GET /api/bookings - Retrieve all bookings
        Expected: 200 OK with list of bookings
        """
        # First create a booking
        client.post("/api/bookings", json=sample_booking_data)
        
        # Then retrieve all bookings
        response = client.get("/api/bookings")
        
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        assert len(data) > 0

    def test_get_booking_by_id_valid(self, client: TestClient, sample_booking_data):
        """
        Test Case: GET /api/bookings/{booking_id} - Retrieve specific booking by valid ID
        Expected: 200 OK with booking details
        """
        # Create a booking first
        create_response = client.post("/api/bookings", json=sample_booking_data)
        booking_id = create_response.json()["id"]
        
        # Retrieve the booking
        response = client.get(f"/api/bookings/{booking_id}")
        
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == booking_id
        assert data["guestName"] == sample_booking_data["guestName"]

    def test_get_booking_by_id_invalid(self, client: TestClient):
        """
        Test Case: GET /api/bookings/{booking_id} - Retrieve booking with non-existent ID
        Expected: 404 Not Found
        """
        booking_id = 99999
        response = client.get(f"/api/bookings/{booking_id}")
        
        assert response.status_code == 404

    def test_delete_booking_valid(self, client: TestClient, sample_booking_data):
        """
        Test Case: DELETE /api/bookings/{booking_id} - Cancel existing booking
        Expected: 200 OK with success message
        """
        # Create a booking first
        create_response = client.post("/api/bookings", json=sample_booking_data)
        booking_id = create_response.json()["id"]
        
        # Delete the booking
        response = client.delete(f"/api/bookings/{booking_id}")
        
        assert response.status_code == 200
        data = response.json()
        assert "message" in data
        
        # Verify booking is deleted
        get_response = client.get(f"/api/bookings/{booking_id}")
        assert get_response.status_code == 404

    def test_delete_booking_invalid(self, client: TestClient):
        """
        Test Case: DELETE /api/bookings/{booking_id} - Cancel non-existent booking
        Expected: 404 Not Found
        """
        booking_id = 99999
        response = client.delete(f"/api/bookings/{booking_id}")
        
        assert response.status_code == 404

    def test_booking_data_integrity(self, client: TestClient, sample_booking_data):
        """
        Test Case: Verify booking data integrity after creation
        Expected: All fields match the submitted data
        """
        response = client.post("/api/bookings", json=sample_booking_data)
        booking = response.json()
        
        # Verify all fields are present and correct
        assert booking["roomId"] == sample_booking_data["roomId"]
        assert booking["guestName"] == sample_booking_data["guestName"]
        assert booking["checkIn"] == sample_booking_data["checkIn"]
        assert booking["checkOut"] == sample_booking_data["checkOut"]
        assert booking["guests"] == sample_booking_data["guests"]
        assert booking["totalPrice"] == sample_booking_data["totalPrice"]

    def test_multiple_bookings_same_room(self, client: TestClient):
        """
        Test Case: Create multiple bookings for the same room
        Expected: All bookings should be created successfully
        """
        booking1 = {
            "roomId": 1,
            "guestName": "Guest One",
            "checkIn": "2026-03-01",
            "checkOut": "2026-03-05",
            "guests": 2,
            "totalPrice": 1199.96
        }
        
        booking2 = {
            "roomId": 1,
            "guestName": "Guest Two",
            "checkIn": "2026-04-01",
            "checkOut": "2026-04-05",
            "guests": 1,
            "totalPrice": 1199.96
        }
        
        response1 = client.post("/api/bookings", json=booking1)
        response2 = client.post("/api/bookings", json=booking2)
        
        assert response1.status_code == 200
        assert response2.status_code == 200
        assert response1.json()["id"] != response2.json()["id"]

    def test_booking_price_calculation(self, client: TestClient):
        """
        Test Case: Verify booking total price calculation
        Expected: Total price should match room price × number of nights
        """
        # Get room price
        room_response = client.get("/api/rooms/1")
        room_price = room_response.json()["price"]
        
        # Calculate expected total for 4 nights
        nights = 4
        expected_total = room_price * nights
        
        booking_data = {
            "roomId": 1,
            "guestName": "Price Test User",
            "checkIn": "2026-03-01",
            "checkOut": "2026-03-05",  # 4 nights
            "guests": 2,
            "totalPrice": expected_total
        }
        
        response = client.post("/api/bookings", json=booking_data)
        
        assert response.status_code == 200
        booking = response.json()
        assert booking["totalPrice"] == expected_total
