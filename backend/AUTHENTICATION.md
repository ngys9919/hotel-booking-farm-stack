# Authentication System Documentation

## Overview

The hotel booking application now includes a comprehensive user authentication system with JWT tokens, password hashing, and protected routes.

## Features

✅ **User Registration** - Create new user accounts with email and password  
✅ **User Login** - Authenticate users and issue JWT tokens  
✅ **Password Security** - Bcrypt password hashing with salt  
✅ **JWT Tokens** - Secure token-based authentication  
✅ **Protected Routes** - Endpoints that require authentication  
✅ **User Management** - Get current user information  
✅ **Token Verification** - Validate JWT tokens  
✅ **Booking Integration** - Associate bookings with authenticated users  

## Architecture

### Backend Components

1. **auth.py** - Authentication utilities
   - JWT token creation and validation
   - Password hashing and verification
   - OAuth2 password bearer scheme
   - Current user dependency injection

2. **models.py** - Data models
   - `UserCreate` - User registration model
   - `UserLogin` - User login model
   - `User` - Database user model
   - `UserResponse` - User response model (without password)
   - `Token` - JWT token response model

3. **user_db.py** - User database operations
   - `create_user()` - Create new user with hashed password
   - `get_user_by_email()` - Retrieve user by email
   - `authenticate_user()` - Verify credentials
   - `user_to_response()` - Convert User to UserResponse

4. **auth_routes.py** - Authentication API endpoints
   - `POST /api/auth/register` - User registration
   - `POST /api/auth/login` - OAuth2 form login
   - `POST /api/auth/login/json` - JSON body login
   - `GET /api/auth/me` - Get current user (protected)
   - `GET /api/auth/verify` - Verify token (protected)

5. **user_bookings.py** - User-specific booking endpoints
   - `GET /api/user/bookings` - Get bookings for authenticated user

### Frontend Components

1. **AuthContext.jsx** - React context for authentication state
   - User state management
   - Login/logout functions
   - Token storage in localStorage
   - Auto-authentication on app load

2. **Login.jsx** - Login modal component
   - Email and password input
   - Error handling
   - Switch to registration

3. **Register.jsx** - Registration modal component
   - Full name, email, password input
   - Password confirmation
   - Validation
   - Auto-login after registration

4. **Navbar.jsx** - Updated with authentication
   - Login/Sign Up buttons (unauthenticated)
   - User info and Logout button (authenticated)
   - Modal management

5. **BookingModal.jsx** - Updated to include user email
   - Associates bookings with authenticated users
   - Sends user_email with booking data

## API Endpoints

### Public Endpoints

#### Register User
```http
POST /api/auth/register
Content-Type: application/json

{
  "email": "user@example.com",
  "password": "securepassword",
  "full_name": "John Doe"
}
```

**Response (201 Created):**
```json
{
  "id": "507f1f77bcf86cd799439011",
  "email": "user@example.com",
  "full_name": "John Doe",
  "is_active": true,
  "created_at": "2026-02-03T10:30:00"
}
```

#### Login (JSON)
```http
POST /api/auth/login/json
Content-Type: application/json

{
  "email": "user@example.com",
  "password": "securepassword"
}
```

**Response (200 OK):**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

#### Login (OAuth2 Form)
```http
POST /api/auth/login
Content-Type: application/x-www-form-urlencoded

username=user@example.com&password=securepassword
```

### Protected Endpoints (Require Authentication)

#### Get Current User
```http
GET /api/auth/me
Authorization: Bearer <access_token>
```

**Response (200 OK):**
```json
{
  "id": "507f1f77bcf86cd799439011",
  "email": "user@example.com",
  "full_name": "John Doe",
  "is_active": true,
  "created_at": "2026-02-03T10:30:00"
}
```

#### Verify Token
```http
GET /api/auth/verify
Authorization: Bearer <access_token>
```

**Response (200 OK):**
```json
{
  "valid": true,
  "email": "user@example.com",
  "message": "Token is valid"
}
```

#### Get User Bookings
```http
GET /api/user/bookings
Authorization: Bearer <access_token>
```

**Response (200 OK):**
```json
[
  {
    "id": "507f1f77bcf86cd799439012",
    "room_id": "507f1f77bcf86cd799439013",
    "room_name": "Deluxe Ocean View Suite",
    "guest_name": "John Doe",
    "check_in_date": "2026-03-01T00:00:00Z",
    "check_out_date": "2026-03-05T00:00:00Z",
    "guests": 2,
    "total_price": 1199.96,
    "booking_date": "2026-02-03T10:35:00",
    "status": "confirmed",
    "user_email": "user@example.com"
  }
]
```

## Security

### Password Hashing
- Uses **bcrypt** algorithm with automatic salt generation
- Passwords are never stored in plain text
- Hash verification is constant-time to prevent timing attacks

### JWT Tokens
- **Algorithm**: HS256 (HMAC with SHA-256)
- **Expiration**: 30 days (configurable via `ACCESS_TOKEN_EXPIRE_MINUTES`)
- **Secret Key**: Randomly generated (should be set in environment variables for production)
- **Claims**: `sub` (subject/email), `exp` (expiration)

### Token Storage
- Frontend stores tokens in `localStorage`
- Tokens are sent in `Authorization` header as `Bearer <token>`
- Tokens are validated on every protected endpoint request

## Configuration

### Environment Variables

Create a `.env` file in the `backend` directory:

```env
# JWT Configuration
SECRET_KEY=your-secret-key-here-change-in-production
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=43200  # 30 days

# MongoDB Configuration
MONGODB_URL=mongodb://localhost:27017
DATABASE_NAME=hotel_booking_db
```

### Generate Secret Key

```python
import secrets
print(secrets.token_urlsafe(32))
```

## Frontend Usage

### Using Authentication Context

```jsx
import { useAuth } from './context/AuthContext';

function MyComponent() {
  const { user, isAuthenticated, login, logout } = useAuth();

  const handleLogin = async () => {
    const result = await login('user@example.com', 'password');
    if (result.success) {
      console.log('Logged in!');
    } else {
      console.error(result.error);
    }
  };

  return (
    <div>
      {isAuthenticated ? (
        <>
          <p>Welcome, {user.full_name}!</p>
          <button onClick={logout}>Logout</button>
        </>
      ) : (
        <button onClick={handleLogin}>Login</button>
      )}
    </div>
  );
}
```

### Making Authenticated API Calls

```javascript
import { useAuth } from './context/AuthContext';

function MyComponent() {
  const { token } = useAuth();

  const fetchUserBookings = async () => {
    const response = await fetch('http://localhost:8000/api/user/bookings', {
      headers: {
        'Authorization': `Bearer ${token}`
      }
    });
    const bookings = await response.json();
    return bookings;
  };

  // ...
}
```

## Testing

### Manual Testing

1. **Start the backend server:**
   ```bash
   cd backend
   python3 main.py
   ```

2. **Test registration:**
   ```bash
   curl -X POST http://localhost:8000/api/auth/register \
     -H "Content-Type: application/json" \
     -d '{"email":"test@test.com","password":"test123","full_name":"Test User"}'
   ```

3. **Test login:**
   ```bash
   curl -X POST http://localhost:8000/api/auth/login/json \
     -H "Content-Type: application/json" \
     -d '{"email":"test@test.com","password":"test123"}'
   ```

4. **Test protected endpoint:**
   ```bash
   TOKEN="<your-access-token>"
   curl -X GET http://localhost:8000/api/auth/me \
     -H "Authorization: Bearer $TOKEN"
   ```

### Automated Testing

Run the test script:
```bash
cd backend
python3 -c "
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

# Test registration
response = client.post('/api/auth/register', json={
    'email': 'test@example.com',
    'password': 'test123',
    'full_name': 'Test User'
})
assert response.status_code == 201

# Test login
response = client.post('/api/auth/login/json', json={
    'email': 'test@example.com',
    'password': 'test123'
})
assert response.status_code == 200
token = response.json()['access_token']

# Test protected endpoint
response = client.get('/api/auth/me', headers={'Authorization': f'Bearer {token}'})
assert response.status_code == 200

print('✅ All tests passed!')
"
```

## Error Handling

### Common Errors

| Status Code | Error | Description |
|------------|-------|-------------|
| 400 | Bad Request | Invalid input data or validation error |
| 401 | Unauthorized | Invalid credentials or missing/invalid token |
| 403 | Forbidden | User account is inactive |
| 404 | Not Found | User not found |
| 500 | Internal Server Error | Server-side error |

### Error Response Format

```json
{
  "detail": "Error message describing what went wrong"
}
```

## Best Practices

1. **Never commit `.env` files** - Use `.env.example` as a template
2. **Use HTTPS in production** - Protect tokens in transit
3. **Rotate secret keys regularly** - Update `SECRET_KEY` periodically
4. **Implement rate limiting** - Prevent brute force attacks
5. **Add email verification** - Verify user email addresses
6. **Implement password reset** - Allow users to reset forgotten passwords
7. **Add refresh tokens** - Implement token refresh mechanism
8. **Log authentication events** - Monitor login attempts and failures
9. **Implement 2FA** - Add two-factor authentication for enhanced security
10. **Use secure password requirements** - Enforce strong password policies

## Future Enhancements

- [ ] Email verification
- [ ] Password reset functionality
- [ ] Refresh token mechanism
- [ ] Two-factor authentication (2FA)
- [ ] OAuth2 social login (Google, Facebook, etc.)
- [ ] Role-based access control (RBAC)
- [ ] Account lockout after failed attempts
- [ ] Password strength meter
- [ ] Session management
- [ ] Audit logging

## Troubleshooting

### Issue: "Invalid token" error

**Solution**: Check if the token has expired. Tokens expire after 30 days by default.

### Issue: "User with this email already exists"

**Solution**: Use a different email address or implement a "forgot password" feature.

### Issue: bcrypt version warning

**Solution**: This is a harmless warning. To suppress it, ensure bcrypt 4.1.2 is installed:
```bash
pip install bcrypt==4.1.2
```

### Issue: Token not persisting after page refresh

**Solution**: Check that `localStorage` is being used correctly and the token is being retrieved on app load.

## Support

For issues or questions about the authentication system:
1. Check this documentation
2. Review the code in `backend/auth.py` and `backend/auth_routes.py`
3. Check the frontend implementation in `frontend/src/context/AuthContext.jsx`
4. Create an issue on GitHub

---

**Last Updated**: February 3, 2026  
**Version**: 1.0.0
