import React, { useState } from 'react';
import { useAuth } from '../context/AuthContext';
import Login from './Login';
import Register from './Register';

const Navbar = ({ currentPage, setCurrentPage }) => {
  const { user, logout, isAuthenticated } = useAuth();
  const [showLogin, setShowLogin] = useState(false);
  const [showRegister, setShowRegister] = useState(false);

  const handleLogout = () => {
    logout();
    setCurrentPage('home');
  };

  return (
    <>
      <nav className="navbar">
        <div className="navbar-container">
          <div className="navbar-logo" onClick={() => setCurrentPage('home')}>
            <span className="logo-icon">🏨</span>
            <span className="logo-text">Luxury Haven</span>
          </div>
          <ul className="navbar-menu">
            <li>
              <button
                className={`nav-link ${currentPage === 'home' ? 'active' : ''}`}
                onClick={() => setCurrentPage('home')}
              >
                Home
              </button>
            </li>
            <li>
              <button
                className={`nav-link ${currentPage === 'bookings' ? 'active' : ''}`}
                onClick={() => setCurrentPage('bookings')}
              >
                My Bookings
              </button>
            </li>
            
            {isAuthenticated ? (
              <>
                <li className="user-info">
                  <span className="user-icon">👤</span>
                  <span className="user-name">{user?.full_name}</span>
                </li>
                <li>
                  <button className="nav-link logout-btn" onClick={handleLogout}>
                    Logout
                  </button>
                </li>
              </>
            ) : (
              <>
                <li>
                  <button className="nav-link login-btn" onClick={() => setShowLogin(true)}>
                    Login
                  </button>
                </li>
                <li>
                  <button className="nav-link signup-btn" onClick={() => setShowRegister(true)}>
                    Sign Up
                  </button>
                </li>
              </>
            )}
          </ul>
        </div>
      </nav>

      {showLogin && (
        <Login
          onClose={() => setShowLogin(false)}
          onSwitchToRegister={() => {
            setShowLogin(false);
            setShowRegister(true);
          }}
        />
      )}

      {showRegister && (
        <Register
          onClose={() => setShowRegister(false)}
          onSwitchToLogin={() => {
            setShowRegister(false);
            setShowLogin(true);
          }}
        />
      )}
    </>
  );
};

export default Navbar;
