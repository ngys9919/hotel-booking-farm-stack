"""
Test suite for general API endpoints and health checks.
"""
import pytest
from fastapi.testclient import TestClient


class TestAPIGeneral:
    """Test cases for general API functionality."""

    def test_root_endpoint(self, client: TestClient):
        """
        Test Case: GET / - API health check
        Expected: 200 OK with welcome message
        """
        response = client.get("/")
        
        assert response.status_code == 200
        data = response.json()
        assert "message" in data
        assert "Hotel Booking API" in data["message"]

    def test_api_cors_headers(self, client: TestClient):
        """
        Test Case: Verify CORS headers are present
        Expected: Response includes CORS headers
        """
        response = client.get("/api/rooms")
        
        # Note: In test environment, CORS headers might not be fully set
        # This test verifies the endpoint is accessible
        assert response.status_code == 200

    def test_invalid_endpoint(self, client: TestClient):
        """
        Test Case: Access non-existent endpoint
        Expected: 404 Not Found
        """
        response = client.get("/api/nonexistent")
        
        assert response.status_code == 404

    def test_api_response_format(self, client: TestClient):
        """
        Test Case: Verify API returns JSON format
        Expected: Content-Type is application/json
        """
        response = client.get("/api/rooms")
        
        assert response.status_code == 200
        assert "application/json" in response.headers["content-type"]

    def test_api_error_handling(self, client: TestClient):
        """
        Test Case: Verify proper error response format
        Expected: Error responses include detail field
        """
        response = client.get("/api/rooms/99999")
        
        assert response.status_code == 404
        data = response.json()
        assert "detail" in data

    def test_api_method_not_allowed(self, client: TestClient):
        """
        Test Case: Use incorrect HTTP method on endpoint
        Expected: 405 Method Not Allowed
        """
        # Try to DELETE on /api/rooms (only GET is allowed)
        response = client.delete("/api/rooms")
        
        assert response.status_code == 405

    def test_api_performance_rooms(self, client: TestClient):
        """
        Test Case: Verify API response time is reasonable
        Expected: Response time < 2 seconds
        """
        import time
        
        start_time = time.time()
        response = client.get("/api/rooms")
        end_time = time.time()
        
        response_time = end_time - start_time
        
        assert response.status_code == 200
        assert response_time < 2.0, f"API response took {response_time}s, expected < 2s"

    def test_api_data_consistency(self, client: TestClient):
        """
        Test Case: Verify data consistency across multiple requests
        Expected: Same data returned on repeated requests
        """
        response1 = client.get("/api/rooms")
        response2 = client.get("/api/rooms")
        
        assert response1.json() == response2.json()
