import React, { useState, useEffect } from 'react';
import { api } from '../api';

const MyBookings = () => {
  const [bookings, setBookings] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [searchName, setSearchName] = useState('');

  useEffect(() => {
    fetchBookings();
  }, []);

  const fetchBookings = async () => {
    try {
      setLoading(true);
      const data = await api.getAllBookings();
      setBookings(data);
    } catch (err) {
      setError('Failed to load bookings. Please try again later.');
    } finally {
      setLoading(false);
    }
  };

  const handleSearch = async (e) => {
    e.preventDefault();
    if (!searchName.trim()) {
      fetchBookings();
      return;
    }

    try {
      setLoading(true);
      const data = await api.getBookingsByGuest(searchName);
      setBookings(data);
    } catch (err) {
      setError('Failed to search bookings. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  const formatDate = (dateString) => {
    const date = new Date(dateString);
    return date.toLocaleDateString('en-US', {
      year: 'numeric',
      month: 'long',
      day: 'numeric',
    });
  };

  return (
    <div className="bookings-page">
      <div className="container">
        <div className="bookings-header">
          <h1 className="page-title">My Bookings</h1>
          <p className="page-subtitle">View and manage your reservations</p>
        </div>

        <form onSubmit={handleSearch} className="search-form">
          <input
            type="text"
            placeholder="Search by guest name..."
            value={searchName}
            onChange={(e) => setSearchName(e.target.value)}
            className="search-input"
          />
          <button type="submit" className="search-btn">
            Search
          </button>
          {searchName && (
            <button
              type="button"
              onClick={() => {
                setSearchName('');
                fetchBookings();
              }}
              className="clear-btn"
            >
              Clear
            </button>
          )}
        </form>

        {loading && (
          <div className="loading-container">
            <div className="spinner"></div>
            <p>Loading bookings...</p>
          </div>
        )}

        {error && (
          <div className="error-container">
            <p className="error-text">{error}</p>
            <button onClick={fetchBookings} className="retry-btn">
              Retry
            </button>
          </div>
        )}

        {!loading && !error && bookings.length === 0 && (
          <div className="empty-state">
            <div className="empty-icon">📅</div>
            <h3>No bookings found</h3>
            <p>
              {searchName
                ? 'No bookings found for this guest name.'
                : "You don't have any bookings yet. Start exploring our rooms!"}
            </p>
          </div>
        )}

        {!loading && !error && bookings.length > 0 && (
          <div className="bookings-list">
            {bookings.map((booking) => (
              <div key={booking.id} className="booking-card">
                <div className="booking-header">
                  <h3 className="booking-room-name">{booking.room_name}</h3>
                  <span className={`booking-status ${booking.status}`}>
                    {booking.status}
                  </span>
                </div>
                <div className="booking-details">
                  <div className="booking-info">
                    <div className="info-item">
                      <span className="info-label">Guest Name:</span>
                      <span className="info-value">{booking.guest_name}</span>
                    </div>
                    <div className="info-item">
                      <span className="info-label">Check-in:</span>
                      <span className="info-value">
                        {formatDate(booking.check_in_date)}
                      </span>
                    </div>
                    <div className="info-item">
                      <span className="info-label">Check-out:</span>
                      <span className="info-value">
                        {formatDate(booking.check_out_date)}
                      </span>
                    </div>
                    <div className="info-item">
                      <span className="info-label">Guests:</span>
                      <span className="info-value">{booking.guests}</span>
                    </div>
                    <div className="info-item">
                      <span className="info-label">Booking Date:</span>
                      <span className="info-value">
                        {formatDate(booking.booking_date)}
                      </span>
                    </div>
                  </div>
                  <div className="booking-price">
                    <span className="price-label">Total Price</span>
                    <span className="price-value">${booking.total_price.toFixed(2)}</span>
                  </div>
                </div>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
};

export default MyBookings;
