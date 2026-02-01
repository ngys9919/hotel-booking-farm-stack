import React from 'react';

const Navbar = ({ currentPage, setCurrentPage }) => {
  return (
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
        </ul>
      </div>
    </nav>
  );
};

export default Navbar;
