import React from 'react';

const RoomCard = ({ room, onBook }) => {
  return (
    <div className="room-card">
      <div className="room-image-container">
        <img src={room.image_url} alt={room.name} className="room-image" />
        <div className="room-price-badge">${room.price_per_night}/night</div>
      </div>
      <div className="room-details">
        <h3 className="room-name">{room.name}</h3>
        <p className="room-description">{room.description}</p>
        <div className="room-amenities">
          {room.amenities.slice(0, 4).map((amenity, index) => (
            <span key={index} className="amenity-tag">
              {amenity}
            </span>
          ))}
        </div>
        <div className="room-footer">
          <span className="room-guests">Up to {room.max_guests} guests</span>
          <button className="book-btn" onClick={() => onBook(room)}>
            Book Now
          </button>
        </div>
      </div>
    </div>
  );
};

export default RoomCard;
