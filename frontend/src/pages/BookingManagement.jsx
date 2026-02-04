import { useState, useEffect } from 'react';
import { api } from '../api';

const BookingManagement = () => {
  const [bookings, setBookings] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [filterStatus, setFilterStatus] = useState('all');
  const [searchTerm, setSearchTerm] = useState('');

  useEffect(() => {
    fetchBookings();
  }, [filterStatus]);

  const fetchBookings = async () => {
    try {
      setLoading(true);
      const statusFilter = filterStatus === 'all' ? null : filterStatus;
      const data = await api.getAdminBookings(0, 100, statusFilter);
      setBookings(data);
      setError('');
    } catch (err) {
      setError(err.message || 'Failed to load bookings');
    } finally {
      setLoading(false);
    }
  };

  const handleUpdateStatus = async (bookingId, newStatus) => {
    try {
      await api.updateBooking(bookingId, { status: newStatus });
      await fetchBookings();
      alert(`Booking status updated to ${newStatus}!`);
    } catch (err) {
      alert(err.message || 'Failed to update booking status');
    }
  };

  const handleDeleteBooking = async (bookingId, guestName) => {
    if (!confirm(`Are you sure you want to delete booking for ${guestName}?`)) {
      return;
    }
    
    try {
      await api.deleteBooking(bookingId);
      await fetchBookings();
      alert('Booking deleted successfully!');
    } catch (err) {
      alert(err.message || 'Failed to delete booking');
    }
  };

  const filteredBookings = bookings.filter(booking =>
    booking.guest_name.toLowerCase().includes(searchTerm.toLowerCase()) ||
    booking.room_name.toLowerCase().includes(searchTerm.toLowerCase()) ||
    (booking.user_email && booking.user_email.toLowerCase().includes(searchTerm.toLowerCase()))
  );

  const getStatusColor = (status) => {
    switch (status) {
      case 'confirmed':
        return 'status-confirmed';
      case 'cancelled':
        return 'status-cancelled';
      case 'pending':
        return 'status-pending';
      case 'completed':
        return 'status-completed';
      default:
        return '';
    }
  };

  if (loading) {
    return (
      <div className="admin-page">
        <div className="loading-spinner">Loading bookings...</div>
      </div>
    );
  }

  return (
    <div className="admin-page">
      <div className="page-header">
        <h1>Booking Management</h1>
        <p>Manage all hotel bookings</p>
      </div>

      <div className="page-controls">
        <input
          type="text"
          placeholder="Search by guest, room, or email..."
          value={searchTerm}
          onChange={(e) => setSearchTerm(e.target.value)}
          className="search-input"
        />
        
        <select
          value={filterStatus}
          onChange={(e) => setFilterStatus(e.target.value)}
          className="filter-select"
        >
          <option value="all">All Statuses</option>
          <option value="confirmed">Confirmed</option>
          <option value="pending">Pending</option>
          <option value="cancelled">Cancelled</option>
          <option value="completed">Completed</option>
        </select>

        <button onClick={fetchBookings} className="refresh-btn">
          🔄 Refresh
        </button>
      </div>

      {error && <div className="error-message">{error}</div>}

      <div className="bookings-table-container">
        <table className="admin-table">
          <thead>
            <tr>
              <th>Guest Name</th>
              <th>Room</th>
              <th>Check-in</th>
              <th>Check-out</th>
              <th>Guests</th>
              <th>Total Price</th>
              <th>Status</th>
              <th>User Email</th>
              <th>Actions</th>
            </tr>
          </thead>
          <tbody>
            {filteredBookings.map((booking) => (
              <tr key={booking.id}>
                <td>{booking.guest_name}</td>
                <td>{booking.room_name}</td>
                <td>{new Date(booking.check_in_date).toLocaleDateString()}</td>
                <td>{new Date(booking.check_out_date).toLocaleDateString()}</td>
                <td>{booking.guests}</td>
                <td>${booking.total_price.toFixed(2)}</td>
                <td>
                  <span className={`status-badge ${getStatusColor(booking.status)}`}>
                    {booking.status}
                  </span>
                </td>
                <td>{booking.user_email || 'N/A'}</td>
                <td className="action-buttons">
                  {booking.status === 'confirmed' && (
                    <>
                      <button
                        onClick={() => handleUpdateStatus(booking.id, 'completed')}
                        className="btn-small btn-success"
                        title="Mark as completed"
                      >
                        ✓
                      </button>
                      <button
                        onClick={() => handleUpdateStatus(booking.id, 'cancelled')}
                        className="btn-small btn-warning"
                        title="Cancel booking"
                      >
                        ✗
                      </button>
                    </>
                  )}
                  {booking.status === 'pending' && (
                    <>
                      <button
                        onClick={() => handleUpdateStatus(booking.id, 'confirmed')}
                        className="btn-small btn-success"
                        title="Confirm booking"
                      >
                        ✓
                      </button>
                      <button
                        onClick={() => handleUpdateStatus(booking.id, 'cancelled')}
                        className="btn-small btn-warning"
                        title="Cancel booking"
                      >
                        ✗
                      </button>
                    </>
                  )}
                  {booking.status === 'cancelled' && (
                    <button
                      onClick={() => handleUpdateStatus(booking.id, 'confirmed')}
                      className="btn-small btn-success"
                      title="Reactivate booking"
                    >
                      ↻
                    </button>
                  )}
                  <button
                    onClick={() => handleDeleteBooking(booking.id, booking.guest_name)}
                    className="btn-small btn-danger"
                    title="Delete booking"
                  >
                    🗑️
                  </button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>

      {filteredBookings.length === 0 && !loading && (
        <div className="empty-state">
          <p>No bookings found</p>
        </div>
      )}

      <div className="page-footer">
        <p>Total bookings: {filteredBookings.length}</p>
        <p>
          Confirmed: {filteredBookings.filter(b => b.status === 'confirmed').length} • 
          Cancelled: {filteredBookings.filter(b => b.status === 'cancelled').length} • 
          Pending: {filteredBookings.filter(b => b.status === 'pending').length}
        </p>
      </div>
    </div>
  );
};

export default BookingManagement;
