import { useState, useEffect } from 'react';
import { useAuth } from '../context/AuthContext';
import AdminDashboard from './AdminDashboard';
import UserManagement from './UserManagement';
import BookingManagement from './BookingManagement';

const AdminPanel = () => {
  const { user, isAuthenticated } = useAuth();
  const [currentView, setCurrentView] = useState('dashboard');

  // Check if user is admin
  if (!isAuthenticated || user?.role !== 'admin') {
    return (
      <div className="admin-panel">
        <div className="access-denied">
          <h1>🔒 Access Denied</h1>
          <p>You need admin privileges to access this page.</p>
          <button onClick={() => window.location.href = '/'} className="btn-primary">
            Go to Home
          </button>
        </div>
      </div>
    );
  }

  const renderView = () => {
    switch (currentView) {
      case 'dashboard':
        return <AdminDashboard />;
      case 'users':
        return <UserManagement />;
      case 'bookings':
        return <BookingManagement />;
      default:
        return <AdminDashboard />;
    }
  };

  return (
    <div className="admin-panel">
      <aside className="admin-sidebar">
        <div className="sidebar-header">
          <h2>🏨 Admin Panel</h2>
          <p className="admin-name">{user?.full_name}</p>
        </div>

        <nav className="sidebar-nav">
          <button
            className={`nav-item ${currentView === 'dashboard' ? 'active' : ''}`}
            onClick={() => setCurrentView('dashboard')}
          >
            <span className="nav-icon">📊</span>
            Dashboard
          </button>

          <button
            className={`nav-item ${currentView === 'users' ? 'active' : ''}`}
            onClick={() => setCurrentView('users')}
          >
            <span className="nav-icon">👥</span>
            Users
          </button>

          <button
            className={`nav-item ${currentView === 'bookings' ? 'active' : ''}`}
            onClick={() => setCurrentView('bookings')}
          >
            <span className="nav-icon">📅</span>
            Bookings
          </button>

          <div className="nav-divider"></div>

          <button
            className="nav-item"
            onClick={() => window.location.href = '/'}
          >
            <span className="nav-icon">🏠</span>
            Back to Site
          </button>
        </nav>
      </aside>

      <main className="admin-content">
        {renderView()}
      </main>
    </div>
  );
};

export default AdminPanel;
