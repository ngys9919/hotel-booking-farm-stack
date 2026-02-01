import React, { useState, useEffect } from 'react';
import Hero from '../components/Hero';
import RoomCard from '../components/RoomCard';
import BookingModal from '../components/BookingModal';
import { api } from '../api';

const Home = () => {
  const [rooms, setRooms] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [selectedRoom, setSelectedRoom] = useState(null);
  const [showSuccess, setShowSuccess] = useState(false);
  const [bookingResult, setBookingResult] = useState(null);

  useEffect(() => {
    fetchRooms();
  }, []);

  const fetchRooms = async () => {
    try {
      setLoading(true);
      const data = await api.getRooms();
      setRooms(data);
    } catch (err) {
      setError('Failed to load rooms. Please try again later.');
    } finally {
      setLoading(false);
    }
  };

  const handleBookRoom = (room) => {
    setSelectedRoom(room);
  };

  const handleCloseModal = () => {
    setSelectedRoom(null);
  };

  const handleBookingSuccess = (result) => {
    setBookingResult(result);
    setSelectedRoom(null);
    setShowSuccess(true);
    setTimeout(() => setShowSuccess(false), 5000);
  };

  return (
    <div className="home-page">
      <Hero />

      <section id="rooms-section" className="rooms-section">
        <div className="container">
          <div className="section-header">
            <h2 className="section-title">Our Exclusive Rooms</h2>
            <p className="section-subtitle">
              Choose from our carefully curated selection of luxury accommodations
            </p>
          </div>

          {loading && (
            <div className="loading-container">
              <div className="spinner"></div>
              <p>Loading rooms...</p>
            </div>
          )}

          {error && (
            <div className="error-container">
              <p className="error-text">{error}</p>
              <button onClick={fetchRooms} className="retry-btn">
                Retry
              </button>
            </div>
          )}

          {!loading && !error && (
            <div className="rooms-grid">
              {rooms.map((room) => (
                <RoomCard key={room.id} room={room} onBook={handleBookRoom} />
              ))}
            </div>
          )}
        </div>
      </section>

      {selectedRoom && (
        <BookingModal
          room={selectedRoom}
          onClose={handleCloseModal}
          onSuccess={handleBookingSuccess}
        />
      )}

      {showSuccess && bookingResult && (
        <div className="success-notification">
          <div className="success-content">
            <span className="success-icon">✓</span>
            <div>
              <h4>Booking Confirmed!</h4>
              <p>
                Your reservation for {bookingResult.room_name} has been confirmed.
              </p>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default Home;
