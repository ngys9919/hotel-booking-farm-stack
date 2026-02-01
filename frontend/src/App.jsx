import React, { useState } from 'react';
import Navbar from './components/Navbar';
import Home from './pages/Home';
import MyBookings from './pages/MyBookings';
import './App.css';

function App() {
  const [currentPage, setCurrentPage] = useState('home');

  return (
    <div className="app">
      <Navbar currentPage={currentPage} setCurrentPage={setCurrentPage} />
      <main className="main-content">
        {currentPage === 'home' ? <Home /> : <MyBookings />}
      </main>
      <footer className="footer">
        <div className="container">
          <p>&copy; 2026 Luxury Haven Hotel. All rights reserved.</p>
        </div>
      </footer>
    </div>
  );
}

export default App;
