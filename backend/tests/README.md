# Hotel Booking API Test Suite

This directory contains comprehensive tests for the Hotel Booking FastAPI backend.

## Test Structure

```
tests/
├── __init__.py           # Package initialization
├── conftest.py           # Pytest fixtures and configuration
├── test_api.py           # General API tests (health check, CORS, error handling)
├── test_rooms.py         # Room endpoints tests
├── test_bookings.py      # Booking endpoints tests
└── README.md             # This file
```

## Test Coverage

### API General Tests (`test_api.py`)
- ✅ Root endpoint health check
- ✅ CORS headers verification
- ✅ Invalid endpoint handling (404)
- ✅ JSON response format
- ✅ Error response format
- ✅ Method not allowed (405)
- ✅ API performance (response time < 2s)
- ✅ Data consistency across requests

### Room Endpoints Tests (`test_rooms.py`)
- ✅ GET /api/rooms - Retrieve all rooms
- ✅ GET /api/rooms/{id} - Retrieve specific room (valid ID)
- ✅ GET /api/rooms/{id} - Handle invalid room ID (404)
- ✅ Data integrity validation (types, values)
- ✅ Price range validation ($50-$1000)
- ✅ Unique room IDs
- ✅ Valid image URLs (http/https)

### Booking Endpoints Tests (`test_bookings.py`)
- ✅ POST /api/bookings - Create booking with valid data
- ✅ POST /api/bookings - Handle missing required fields (422)
- ✅ POST /api/bookings - Handle invalid room ID (404)
- ✅ POST /api/bookings - Handle invalid dates (400)
- ✅ GET /api/bookings - Retrieve all bookings
- ✅ GET /api/bookings/{id} - Retrieve specific booking
- ✅ GET /api/bookings/{id} - Handle invalid booking ID (404)
- ✅ DELETE /api/bookings/{id} - Cancel booking
- ✅ DELETE /api/bookings/{id} - Handle invalid booking ID (404)
- ✅ Booking data integrity verification
- ✅ Multiple bookings for same room
- ✅ Price calculation verification

## Running Tests

### Install Dependencies

```bash
cd backend
pip install -r requirements.txt
```

The requirements.txt includes:
- pytest==7.4.3
- pytest-asyncio==0.21.1
- httpx==0.25.2

### Run All Tests

```bash
# Run all tests with verbose output
pytest tests/ -v

# Run with detailed output
pytest tests/ -vv

# Run with coverage report
pytest tests/ --cov=. --cov-report=html

# Run specific test file
pytest tests/test_rooms.py -v

# Run specific test class
pytest tests/test_rooms.py::TestRoomsEndpoints -v

# Run specific test
pytest tests/test_rooms.py::TestRoomsEndpoints::test_get_all_rooms -v
```

### Run Tests by Marker

```bash
# Run only unit tests
pytest tests/ -m unit -v

# Run only integration tests
pytest tests/ -m integration -v
```

## Test Configuration

### pytest.ini

The `pytest.ini` file configures:
- Test discovery patterns
- Async test mode
- Test markers
- Output formatting

### conftest.py

Provides shared fixtures:
- `client`: FastAPI TestClient instance
- `sample_room_data`: Valid room data for testing
- `sample_booking_data`: Valid booking data for testing
- `invalid_booking_data`: Invalid data for validation testing

## API Schema

### Room Fields (snake_case)
```python
{
    "name": str,
    "description": str,
    "price_per_night": float,
    "image_url": str,
    "max_guests": int,
    "amenities": list[str]
}
```

### Booking Fields (snake_case)
```python
{
    "room_id": str,
    "guest_name": str,
    "check_in_date": str,  # Format: "YYYY-MM-DD"
    "check_out_date": str,  # Format: "YYYY-MM-DD"
    "guests": int
}
```

## Known Issues

### Database Initialization
The mock database needs to be properly initialized before running tests. The sample rooms are created during the FastAPI lifespan startup.

### Field Naming Convention
The API uses `snake_case` for field names (e.g., `room_id`, `guest_name`, `check_in_date`), not `camelCase`.

## Test Results Summary

As of the latest run:
- **Total Tests**: 27
- **Passed**: 14 tests
- **Failed**: 13 tests (due to database initialization issues)
- **Test Coverage**: All major endpoints covered

### Passing Tests
- API health check
- CORS functionality
- Error handling (404, 405)
- Response format validation
- API performance
- Data consistency

### Tests Requiring Database
Some tests require the mock database to be properly initialized with sample data:
- Room listing and retrieval
- Booking creation and management
- Data integrity validation

## Continuous Integration

To integrate with CI/CD:

```yaml
# Example GitHub Actions workflow
- name: Run tests
  run: |
    cd backend
    pip install -r requirements.txt
    pytest tests/ -v --junitxml=test-results.xml
```

## Contributing

When adding new tests:
1. Follow the existing test structure
2. Use descriptive test names
3. Include docstrings explaining the test case
4. Use appropriate fixtures from conftest.py
5. Add test markers (unit/integration) as needed

## Troubleshooting

### Import Errors
Make sure you're in the backend directory when running tests:
```bash
cd backend
pytest tests/
```

### Database Connection Issues
The tests use the mock database by default. Ensure the database module is properly configured.

### httpx Version Issues
If you encounter `TypeError: Client.__init__() got an unexpected keyword argument 'app'`, ensure httpx version is 0.25.2:
```bash
pip install httpx==0.25.2
```

## Future Improvements

- [ ] Add test coverage reporting
- [ ] Implement test database fixtures
- [ ] Add performance benchmarking tests
- [ ] Create integration tests with real MongoDB
- [ ] Add API load testing
- [ ] Implement test data factories
- [ ] Add mutation testing

## Resources

- [FastAPI Testing Documentation](https://fastapi.tiangolo.com/tutorial/testing/)
- [Pytest Documentation](https://docs.pytest.org/)
- [pytest-asyncio Documentation](https://pytest-asyncio.readthedocs.io/)
