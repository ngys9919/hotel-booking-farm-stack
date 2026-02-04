const API_BASE_URL = 'http://localhost:8000/api';
const AUTH_BASE_URL = 'http://localhost:8000/api/auth';

export const api = {
  // Get all rooms
  async getRooms() {
    const response = await fetch(`${API_BASE_URL}/rooms`);
    if (!response.ok) throw new Error('Failed to fetch rooms');
    return response.json();
  },

  // Get a specific room
  async getRoom(roomId) {
    const response = await fetch(`${API_BASE_URL}/rooms/${roomId}`);
    if (!response.ok) throw new Error('Failed to fetch room');
    return response.json();
  },

  // Create a booking
  async createBooking(bookingData) {
    const response = await fetch(`${API_BASE_URL}/bookings`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(bookingData),
    });
    if (!response.ok) {
      const error = await response.json();
      throw new Error(error.detail || 'Failed to create booking');
    }
    return response.json();
  },

  // Get all bookings
  async getAllBookings() {
    const response = await fetch(`${API_BASE_URL}/bookings`);
    if (!response.ok) throw new Error('Failed to fetch bookings');
    return response.json();
  },

  // Get bookings by guest name
  async getBookingsByGuest(guestName) {
    const response = await fetch(`${API_BASE_URL}/bookings/guest/${encodeURIComponent(guestName)}`);
    if (!response.ok) throw new Error('Failed to fetch bookings');
    return response.json();
  },
};

// Authentication API functions
export const login = async (email, password) => {
  const response = await fetch(`${AUTH_BASE_URL}/login/json`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({ email, password }),
  });
  if (!response.ok) {
    const error = await response.json();
    throw new Error(error.detail || 'Login failed');
  }
  return response.json();
};

export const register = async (email, password, fullName) => {
  const response = await fetch(`${AUTH_BASE_URL}/register`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({
      email,
      password,
      full_name: fullName,
    }),
  });
  if (!response.ok) {
    const error = await response.json();
    throw new Error(error.detail || 'Registration failed');
  }
  return response.json();
};

export const getCurrentUser = async (token) => {
  const response = await fetch(`${AUTH_BASE_URL}/me`, {
    headers: {
      'Authorization': `Bearer ${token}`,
    },
  });
  if (!response.ok) {
    throw new Error('Failed to get user info');
  }
  return response.json();
};

export const verifyToken = async (token) => {
  const response = await fetch(`${AUTH_BASE_URL}/verify`, {
    headers: {
      'Authorization': `Bearer ${token}`,
    },
  });
  if (!response.ok) {
    throw new Error('Token verification failed');
  }
  return response.json();
};


// Admin API functions
const ADMIN_BASE_URL = 'http://localhost:8000/api/admin';

const getAuthHeaders = () => {
  const token = localStorage.getItem('token');
  return {
    'Content-Type': 'application/json',
    'Authorization': `Bearer ${token}`,
  };
};

// Admin - Statistics
api.getAdminStats = async () => {
  const response = await fetch(`${ADMIN_BASE_URL}/stats`, {
    headers: getAuthHeaders(),
  });
  if (!response.ok) {
    const error = await response.json();
    throw new Error(error.detail || 'Failed to fetch statistics');
  }
  return response.json();
};

// Admin - User Management
api.getAllUsers = async (skip = 0, limit = 100) => {
  const response = await fetch(`${ADMIN_BASE_URL}/users?skip=${skip}&limit=${limit}`, {
    headers: getAuthHeaders(),
  });
  if (!response.ok) {
    const error = await response.json();
    throw new Error(error.detail || 'Failed to fetch users');
  }
  return response.json();
};

api.getUserById = async (userId) => {
  const response = await fetch(`${ADMIN_BASE_URL}/users/${userId}`, {
    headers: getAuthHeaders(),
  });
  if (!response.ok) {
    const error = await response.json();
    throw new Error(error.detail || 'Failed to fetch user');
  }
  return response.json();
};

api.updateUser = async (userId, updateData) => {
  const response = await fetch(`${ADMIN_BASE_URL}/users/${userId}`, {
    method: 'PATCH',
    headers: getAuthHeaders(),
    body: JSON.stringify(updateData),
  });
  if (!response.ok) {
    const error = await response.json();
    throw new Error(error.detail || 'Failed to update user');
  }
  return response.json();
};

api.deleteUser = async (userId) => {
  const response = await fetch(`${ADMIN_BASE_URL}/users/${userId}`, {
    method: 'DELETE',
    headers: getAuthHeaders(),
  });
  if (!response.ok) {
    const error = await response.json();
    throw new Error(error.detail || 'Failed to delete user');
  }
  return response.json();
};

// Admin - Booking Management
api.getAdminBookings = async (skip = 0, limit = 100, status = null) => {
  let url = `${ADMIN_BASE_URL}/bookings?skip=${skip}&limit=${limit}`;
  if (status) {
    url += `&status=${status}`;
  }
  const response = await fetch(url, {
    headers: getAuthHeaders(),
  });
  if (!response.ok) {
    const error = await response.json();
    throw new Error(error.detail || 'Failed to fetch bookings');
  }
  return response.json();
};

api.getBookingById = async (bookingId) => {
  const response = await fetch(`${ADMIN_BASE_URL}/bookings/${bookingId}`, {
    headers: getAuthHeaders(),
  });
  if (!response.ok) {
    const error = await response.json();
    throw new Error(error.detail || 'Failed to fetch booking');
  }
  return response.json();
};

api.updateBooking = async (bookingId, updateData) => {
  const response = await fetch(`${ADMIN_BASE_URL}/bookings/${bookingId}`, {
    method: 'PATCH',
    headers: getAuthHeaders(),
    body: JSON.stringify(updateData),
  });
  if (!response.ok) {
    const error = await response.json();
    throw new Error(error.detail || 'Failed to update booking');
  }
  return response.json();
};

api.deleteBooking = async (bookingId) => {
  const response = await fetch(`${ADMIN_BASE_URL}/bookings/${bookingId}`, {
    method: 'DELETE',
    headers: getAuthHeaders(),
  });
  if (!response.ok) {
    const error = await response.json();
    throw new Error(error.detail || 'Failed to delete booking');
  }
  return response.json();
};
