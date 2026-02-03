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
