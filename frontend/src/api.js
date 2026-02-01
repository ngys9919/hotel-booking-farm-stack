const API_BASE_URL = 'http://localhost:8000/api';

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
