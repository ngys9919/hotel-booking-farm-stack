import { useState, useEffect } from 'react';
import { useAuth } from '../context/AuthContext';
import { api } from '../api';

const AdminDashboard = () => {
  const { user } = useAuth();
  const [stats, setStats] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    fetchStats();
  }, []);

  const fetchStats = async () => {
    try {
      setLoading(true);
      const data = await api.getAdminStats();
      setStats(data);
      setError('');
    } catch (err) {
      setError(err.message || 'Failed to load statistics');
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return (
      <div className="admin-dashboard">
        <div className="loading-spinner">Loading dashboard...</div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="admin-dashboard">
        <div className="error-message">{error}</div>
      </div>
    );
  }

  return (
    <div className="admin-dashboard">
      <div className="admin-header">
        <h1>Admin Dashboard</h1>
        <p>Welcome back, {user?.full_name}</p>
      </div>

      <div className="stats-grid">
        <div className="stat-card">
          <div className="stat-icon">👥</div>
          <div className="stat-content">
            <h3>Total Users</h3>
            <p className="stat-number">{stats?.users?.total || 0}</p>
            <p className="stat-detail">
              {stats?.users?.active || 0} active • {stats?.users?.admins || 0} admins
            </p>
          </div>
        </div>

        <div className="stat-card">
          <div className="stat-icon">📅</div>
          <div className="stat-content">
            <h3>Total Bookings</h3>
            <p className="stat-number">{stats?.bookings?.total || 0}</p>
            <p className="stat-detail">
              {stats?.bookings?.confirmed || 0} confirmed • {stats?.bookings?.cancelled || 0} cancelled
            </p>
          </div>
        </div>

        <div className="stat-card">
          <div className="stat-icon">💰</div>
          <div className="stat-content">
            <h3>Total Revenue</h3>
            <p className="stat-number">
              ${stats?.revenue?.total?.toLocaleString() || 0}
            </p>
            <p className="stat-detail">From confirmed bookings</p>
          </div>
        </div>

        <div className="stat-card">
          <div className="stat-icon">📊</div>
          <div className="stat-content">
            <h3>Booking Rate</h3>
            <p className="stat-number">
              {stats?.bookings?.total > 0
                ? Math.round((stats.bookings.confirmed / stats.bookings.total) * 100)
                : 0}%
            </p>
            <p className="stat-detail">Confirmation rate</p>
          </div>
        </div>
      </div>

      <div className="admin-actions">
        <h2>Quick Actions</h2>
        <div className="action-buttons">
          <button className="action-btn" onClick={() => window.location.href = '#users'}>
            <span className="action-icon">👥</span>
            Manage Users
          </button>
          <button className="action-btn" onClick={() => window.location.href = '#bookings'}>
            <span className="action-icon">📅</span>
            Manage Bookings
          </button>
          <button className="action-btn" onClick={fetchStats}>
            <span className="action-icon">🔄</span>
            Refresh Stats
          </button>
        </div>
      </div>
    </div>
  );
};

export default AdminDashboard;
