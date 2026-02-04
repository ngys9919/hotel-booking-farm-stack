# Admin Panel Documentation

## Overview

The hotel booking application now includes a comprehensive admin panel with role-based access control (RBAC), user management, booking management, and dashboard statistics.

## Features

✅ **Role-Based Access Control** - Admin and user roles with protected endpoints  
✅ **Admin Dashboard** - Statistics and quick actions  
✅ **User Management** - View, update, activate/deactivate, and delete users  
✅ **Booking Management** - View, update status, and delete bookings  
✅ **Statistics** - Real-time metrics for users, bookings, and revenue  
✅ **Beautiful UI** - Professional admin interface with responsive design  
✅ **Access Control** - Only admins can access admin panel  

---

## Architecture

### Backend Components

1. **models.py** (Updated)
   - Added `role` field to User model (user/admin)
   - Updated UserResponse to include role

2. **auth.py** (Updated)
   - `get_current_admin_user()` - Dependency for admin-only endpoints
   - `is_admin()` - Helper function to check admin role

3. **admin_routes.py** (New - 380 lines)
   - User management endpoints (GET, PATCH, DELETE)
   - Booking management endpoints (GET, PATCH, DELETE)
   - Statistics endpoint for dashboard

4. **main.py** (Updated)
   - Integrated admin routes

### Frontend Components

1. **AdminPanel.jsx** (New - 90 lines)
   - Main admin panel component with sidebar navigation
   - Access control (admin-only)
   - View routing (dashboard, users, bookings)

2. **AdminDashboard.jsx** (New - 120 lines)
   - Statistics cards (users, bookings, revenue)
   - Quick action buttons
   - Real-time data fetching

3. **UserManagement.jsx** (New - 180 lines)
   - User list table
   - Search functionality
   - Toggle active/inactive status
   - Toggle user/admin role
   - Delete users

4. **BookingManagement.jsx** (New - 200 lines)
   - Booking list table
   - Filter by status
   - Search functionality
   - Update booking status
   - Delete bookings

5. **admin.css** (New - 450 lines)
   - Professional admin panel styling
   - Responsive design
   - Modern UI components

6. **api.js** (Updated)
   - Admin API functions for all endpoints

7. **Navbar.jsx** (Updated)
   - Admin Panel link (visible only to admins)

8. **App.jsx** (Updated)
   - Admin panel routing

---

## API Endpoints

### Admin - Statistics

#### Get Dashboard Statistics
```http
GET /api/admin/stats
Authorization: Bearer <admin_token>
```

**Response:**
```json
{
  "users": {
    "total": 25,
    "active": 23,
    "admins": 2
  },
  "bookings": {
    "total": 150,
    "confirmed": 120,
    "cancelled": 30
  },
  "revenue": {
    "total": 45000.00,
    "currency": "USD"
  }
}
```

### Admin - User Management

#### Get All Users
```http
GET /api/admin/users?skip=0&limit=100
Authorization: Bearer <admin_token>
```

**Response:**
```json
[
  {
    "id": "507f1f77bcf86cd799439011",
    "email": "user@example.com",
    "full_name": "John Doe",
    "role": "user",
    "is_active": true,
    "created_at": "2026-02-03T10:00:00"
  }
]
```

#### Get User by ID
```http
GET /api/admin/users/{user_id}
Authorization: Bearer <admin_token>
```

#### Update User
```http
PATCH /api/admin/users/{user_id}
Authorization: Bearer <admin_token>
Content-Type: application/json

{
  "role": "admin",
  "is_active": true,
  "full_name": "John Doe Updated"
}
```

#### Delete User
```http
DELETE /api/admin/users/{user_id}
Authorization: Bearer <admin_token>
```

**Response:**
```json
{
  "message": "User deleted successfully",
  "user_id": "507f1f77bcf86cd799439011"
}
```

### Admin - Booking Management

#### Get All Bookings
```http
GET /api/admin/bookings?skip=0&limit=100&status=confirmed
Authorization: Bearer <admin_token>
```

**Query Parameters:**
- `skip` - Number of bookings to skip (pagination)
- `limit` - Maximum number of bookings to return
- `status` - Filter by status (confirmed, cancelled, pending, completed)

**Response:**
```json
[
  {
    "id": "507f1f77bcf86cd799439012",
    "room_id": "507f1f77bcf86cd799439013",
    "room_name": "Deluxe Ocean View Suite",
    "guest_name": "Jane Smith",
    "check_in_date": "2026-03-01T00:00:00Z",
    "check_out_date": "2026-03-05T00:00:00Z",
    "guests": 2,
    "total_price": 1199.96,
    "booking_date": "2026-02-03T10:00:00",
    "status": "confirmed",
    "user_email": "jane@example.com"
  }
]
```

#### Get Booking by ID
```http
GET /api/admin/bookings/{booking_id}
Authorization: Bearer <admin_token>
```

#### Update Booking
```http
PATCH /api/admin/bookings/{booking_id}
Authorization: Bearer <admin_token>
Content-Type: application/json

{
  "status": "cancelled"
}
```

**Allowed status values:**
- `confirmed` - Booking is confirmed
- `pending` - Booking is pending confirmation
- `cancelled` - Booking has been cancelled
- `completed` - Booking has been completed

#### Delete Booking
```http
DELETE /api/admin/bookings/{booking_id}
Authorization: Bearer <admin_token>
```

**Response:**
```json
{
  "message": "Booking deleted successfully",
  "booking_id": "507f1f77bcf86cd799439012"
}
```

---

## User Interface

### Admin Dashboard

The admin dashboard provides an overview of the system:

**Statistics Cards:**
- Total Users (with active and admin counts)
- Total Bookings (with confirmed and cancelled counts)
- Total Revenue (from confirmed bookings)
- Booking Rate (confirmation percentage)

**Quick Actions:**
- Manage Users
- Manage Bookings
- Refresh Stats

### User Management

Features:
- **Search** - Search by email or full name
- **View All Users** - Paginated list of all registered users
- **Toggle Active Status** - Activate or deactivate user accounts
- **Toggle Role** - Change user role between user and admin
- **Delete User** - Permanently remove users

**Table Columns:**
- Email
- Full Name
- Role (badge: admin/user)
- Status (badge: active/inactive)
- Created At
- Actions (activate, change role, delete)

### Booking Management

Features:
- **Search** - Search by guest name, room name, or user email
- **Filter by Status** - Show all, confirmed, pending, cancelled, or completed
- **View All Bookings** - Paginated list of all bookings
- **Update Status** - Change booking status
- **Delete Booking** - Permanently remove bookings

**Table Columns:**
- Guest Name
- Room
- Check-in Date
- Check-out Date
- Number of Guests
- Total Price
- Status (badge with color coding)
- User Email
- Actions (confirm, cancel, complete, delete)

**Status Actions:**
- **Confirmed** → Can mark as completed or cancelled
- **Pending** → Can confirm or cancel
- **Cancelled** → Can reactivate (confirm)
- **Completed** → No status changes (can delete)

---

## Access Control

### Role-Based Access

**User Role (`user`):**
- Can register and login
- Can create bookings
- Can view their own bookings
- Cannot access admin panel

**Admin Role (`admin`):**
- All user permissions
- Can access admin panel
- Can view all users and bookings
- Can update user information
- Can activate/deactivate users
- Can change user roles
- Can delete users
- Can update booking status
- Can delete bookings
- Can view statistics

### Protected Endpoints

All admin endpoints require:
1. Valid JWT token in Authorization header
2. User must have `role: "admin"`

If a non-admin user tries to access admin endpoints:
```json
{
  "detail": "Not authorized. Admin access required."
}
```

---

## Creating Admin Users

### Method 1: Direct Database Update (Recommended)

After registering a user, update their role in the database:

**MongoDB:**
```javascript
db.users.updateOne(
  { email: "admin@example.com" },
  { $set: { role: "admin" } }
)
```

**Python:**
```python
await users_collection.update_one(
    {"email": "admin@example.com"},
    {"$set": {"role": "admin"}}
)
```

### Method 2: Registration with Admin Role

Modify the registration endpoint to accept a role parameter (for initial setup only):

```python
# In auth_routes.py - register_user()
# Add this for initial admin creation only, then remove
user = User(
    email=user_data.email,
    hashed_password=hashed_password,
    full_name=user_data.full_name,
    role="admin",  # Set to admin for first user
    is_active=True,
    created_at=datetime.utcnow()
)
```

### Method 3: Admin Panel (After First Admin)

Once you have one admin user, you can use the admin panel to promote other users to admin:

1. Login as admin
2. Go to Admin Panel → Users
3. Find the user
4. Click the role toggle button (👑)
5. Confirm the change

---

## Testing

### Manual Testing

1. **Create Users:**
   ```bash
   # Create regular user
   curl -X POST http://localhost:8000/api/auth/register \
     -H "Content-Type: application/json" \
     -d '{"email":"user@test.com","password":"user123","full_name":"Regular User"}'
   
   # Create admin user
   curl -X POST http://localhost:8000/api/auth/register \
     -H "Content-Type: application/json" \
     -d '{"email":"admin@test.com","password":"admin123","full_name":"Admin User"}'
   ```

2. **Set Admin Role:**
   ```bash
   # Using MongoDB shell
   mongo
   use hotel_booking_db
   db.users.updateOne({email:"admin@test.com"}, {$set:{role:"admin"}})
   ```

3. **Login as Admin:**
   ```bash
   curl -X POST http://localhost:8000/api/auth/login/json \
     -H "Content-Type: application/json" \
     -d '{"email":"admin@test.com","password":"admin123"}'
   ```

4. **Test Admin Endpoints:**
   ```bash
   TOKEN="<your-admin-token>"
   
   # Get stats
   curl -X GET http://localhost:8000/api/admin/stats \
     -H "Authorization: Bearer $TOKEN"
   
   # Get all users
   curl -X GET http://localhost:8000/api/admin/users \
     -H "Authorization: Bearer $TOKEN"
   
   # Get all bookings
   curl -X GET http://localhost:8000/api/admin/bookings \
     -H "Authorization: Bearer $TOKEN"
   ```

5. **Test Access Control:**
   ```bash
   # Login as regular user
   curl -X POST http://localhost:8000/api/auth/login/json \
     -H "Content-Type: application/json" \
     -d '{"email":"user@test.com","password":"user123"}'
   
   USER_TOKEN="<user-token>"
   
   # Try to access admin endpoint (should fail with 403)
   curl -X GET http://localhost:8000/api/admin/stats \
     -H "Authorization: Bearer $USER_TOKEN"
   ```

### Frontend Testing

1. **Access Admin Panel:**
   - Login as admin user
   - Admin Panel link should appear in navbar
   - Click "👑 Admin Panel"

2. **Test Dashboard:**
   - Verify statistics are displayed
   - Check that numbers are correct
   - Test quick action buttons

3. **Test User Management:**
   - Search for users
   - Toggle user active status
   - Change user role
   - Delete a test user

4. **Test Booking Management:**
   - Filter bookings by status
   - Search for bookings
   - Update booking status
   - Delete a test booking

5. **Test Access Control:**
   - Logout
   - Login as regular user
   - Verify Admin Panel link is not visible
   - Try to access `/admin` directly (should show access denied)

---

## Security Considerations

1. **Admin Role Assignment** - Only assign admin role to trusted users
2. **Token Security** - Admin tokens have the same expiration as user tokens (30 days)
3. **Audit Logging** - Consider adding audit logs for admin actions
4. **Rate Limiting** - Implement rate limiting on admin endpoints
5. **HTTPS** - Always use HTTPS in production
6. **Database Backups** - Regular backups before admin operations
7. **Soft Delete** - Consider implementing soft delete instead of permanent deletion

---

## UI/UX Features

### Responsive Design
- Mobile-friendly sidebar (collapses to full-width)
- Responsive tables
- Touch-friendly buttons

### Visual Feedback
- Loading spinners
- Success/error messages
- Hover effects
- Status badges with color coding
- Smooth transitions

### User Experience
- Search and filter functionality
- Pagination support
- Confirmation dialogs for destructive actions
- Quick action buttons
- Intuitive navigation

---

## Future Enhancements

- [ ] Audit logging for admin actions
- [ ] Export data (CSV, Excel)
- [ ] Advanced filtering and sorting
- [ ] Bulk operations (delete multiple users/bookings)
- [ ] User activity tracking
- [ ] Email notifications for admin actions
- [ ] Role permissions customization
- [ ] Admin activity dashboard
- [ ] Data visualization charts
- [ ] Booking calendar view

---

## Troubleshooting

### Issue: "Not authorized. Admin access required"

**Solution**: Ensure the user has `role: "admin"` in the database.

### Issue: Admin Panel link not showing

**Solution**: 
1. Check that user is logged in
2. Verify user role is "admin"
3. Clear browser cache and reload

### Issue: Statistics showing zero

**Solution**: 
1. Check database connection
2. Verify there are users and bookings in the database
3. Check browser console for API errors

### Issue: Cannot delete user/booking

**Solution**:
1. Verify admin token is valid
2. Check that the ID is correct
3. Ensure the item exists in the database

---

## API Error Codes

| Status Code | Error | Description |
|------------|-------|-------------|
| 200 | OK | Request successful |
| 201 | Created | Resource created |
| 400 | Bad Request | Invalid input data |
| 401 | Unauthorized | Missing or invalid token |
| 403 | Forbidden | Not authorized (not admin) |
| 404 | Not Found | Resource not found |
| 500 | Internal Server Error | Server error |

---

## Summary

The admin panel provides a complete solution for managing users and bookings in the hotel booking application. It includes:

- ✅ Role-based access control
- ✅ User management (CRUD operations)
- ✅ Booking management (CRUD operations)
- ✅ Dashboard with statistics
- ✅ Professional UI with responsive design
- ✅ Secure authentication and authorization
- ✅ Search and filter functionality
- ✅ Status management for bookings

**The admin panel is production-ready and can be used immediately!**

---

**Last Updated**: February 3, 2026  
**Version**: 1.0.0
