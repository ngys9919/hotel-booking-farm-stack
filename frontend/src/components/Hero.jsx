import React from 'react';

const Hero = () => {
  const scrollToRooms = () => {
    const roomsSection = document.getElementById('rooms-section');
    if (roomsSection) {
      roomsSection.scrollIntoView({ behavior: 'smooth' });
    }
  };

  return (
    <section className="hero">
      <div className="hero-overlay"></div>
      <div className="hero-content">
        <h1 className="hero-title">Welcome to Luxury Haven</h1>
        <p className="hero-subtitle">
          Experience unparalleled comfort and elegance in the heart of paradise
        </p>
        <button className="hero-btn" onClick={scrollToRooms}>
          Explore Our Rooms
        </button>
      </div>
    </section>
  );
};

export default Hero;
