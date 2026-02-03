import React, { useState } from 'react';
import { AuthProvider } from './context/AuthContext';
import Navbar from './components/Navbar';
import Home from './pages/Home';
import MyBookings from './pages/MyBookings';
import './App.css';
import './auth.css';

function App() {
  const [currentPage, setCurrentPage] = useState('home');

  return (
    <AuthProvider>
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
    </AuthProvider>
  );
}

export default App;
