# Hotel Booking Standalone Webpage

## Overview

This is a **standalone HTML webpage** for the Luxury Haven Hotel booking application. It requires no backend server, no database, and no build process. Simply open the HTML file in any modern web browser to use the application.

## Features

### 🎨 Beautiful Design
- Modern, premium design with professional styling
- Responsive layout that works on desktop, tablet, and mobile
- Smooth animations and transitions
- High-quality room images from Unsplash

### 🏨 Room Listings
- 6 luxury rooms with detailed descriptions
- Price display per night
- Room amenities and features
- Maximum guest capacity
- High-quality images for each room

### 📅 Booking System
- Interactive booking modal
- Date pickers for check-in and check-out
- Guest selection dropdown
- Automatic price calculation based on number of nights
- Real-time booking summary display
- Form validation

### 📋 My Bookings Page
- View all confirmed reservations
- Search functionality to filter bookings by guest name
- Detailed booking information including:
  - Guest name
  - Room name
  - Check-in and check-out dates
  - Number of guests
  - Booking date
  - Total price
- Confirmed status badge

### 💾 Data Persistence
- Bookings are stored in browser's localStorage
- Data persists across page refreshes
- No database required

## How to Use

### Option 1: Open Directly in Browser
1. Navigate to `/home/ubuntu/hotel-booking-app/`
2. Double-click `hotel-booking-standalone.html`
3. The webpage will open in your default browser

### Option 2: Serve with HTTP Server
```bash
cd /home/ubuntu/hotel-booking-app
python3 -m http.server 8080
```
Then open `http://localhost:8080/hotel-booking-standalone.html` in your browser.

### Option 3: Deploy to Web Hosting
Upload `hotel-booking-standalone.html` to any web hosting service:
- GitHub Pages
- Netlify
- Vercel
- AWS S3 Static Website Hosting
- Any traditional web host

## Making a Booking

1. **Browse Rooms**: Scroll through the available rooms on the home page
2. **Select a Room**: Click the "Book Now" button on your preferred room
3. **Fill Booking Form**:
   - Enter your full name
   - Select check-in date
   - Select check-out date
   - Choose number of guests
4. **Review Summary**: The booking summary will automatically calculate:
   - Number of nights
   - Price per night
   - Total price
5. **Confirm Booking**: Click "Confirm Booking" button
6. **View Confirmation**: Navigate to "My Bookings" to see your reservation

## Viewing Bookings

1. Click "My Bookings" in the navigation bar
2. All confirmed bookings will be displayed
3. Use the search box to filter by guest name
4. Each booking card shows complete details

## Technical Details

### Technologies Used
- **HTML5**: Semantic markup
- **CSS3**: Modern styling with flexbox and grid
- **Vanilla JavaScript**: No frameworks or libraries required
- **localStorage API**: Client-side data persistence

### Browser Compatibility
- Chrome (recommended)
- Firefox
- Safari
- Edge
- Any modern browser with ES6+ support

### File Structure
```
hotel-booking-standalone.html
├── HTML Structure
├── <style> Embedded CSS (Premium Design)
└── <script> Embedded JavaScript
    ├── Room Data (6 luxury rooms)
    ├── Booking Logic
    ├── localStorage Management
    ├── Search Functionality
    └── UI Interactions
```

### Data Storage
All booking data is stored in the browser's localStorage under the key `hotelBookings`. The data structure is:

```javascript
{
  id: "unique-id",
  roomId: 1,
  roomName: "Deluxe Ocean View Suite",
  guestName: "Sarah Johnson",
  checkIn: "2026-02-15",
  checkOut: "2026-02-18",
  guests: 1,
  totalPrice: 899.97,
  bookingDate: "2026-02-01",
  status: "confirmed"
}
```

## Customization

### Adding New Rooms
Edit the `rooms` array in the JavaScript section:

```javascript
const rooms = [
  {
    id: 7,
    name: "Your New Room",
    description: "Room description",
    price: 199.99,
    image: "https://images.unsplash.com/photo-...",
    maxGuests: 2,
    amenities: ["WiFi", "TV", "Mini Bar"]
  }
];
```

### Changing Colors
Modify the CSS variables in the `:root` selector:

```css
:root {
  --primary-color: #1e3a5f;
  --secondary-color: #e63946;
  --accent-color: #f4a261;
}
```

### Modifying Layout
Edit the CSS classes and HTML structure as needed. The design uses modern CSS features like flexbox and grid for easy customization.

## Limitations

Since this is a standalone client-side application:

1. **No Backend**: All data is stored locally in the browser
2. **No Email Notifications**: Cannot send confirmation emails
3. **No Payment Processing**: No payment gateway integration
4. **No User Authentication**: No login system
5. **Local Storage Only**: Data is not shared across devices
6. **No Room Availability Check**: All rooms are always available

## Converting to Full-Stack

To convert this to a full-stack application with backend:

1. Use the FARM stack version in `/home/ubuntu/hotel-booking-app/`
2. Replace localStorage calls with API calls to the FastAPI backend
3. Connect to MongoDB for persistent data storage
4. Add user authentication and payment processing

See `README.md` and `DEPLOYMENT.md` in the main project folder for details.

## Live Demo

The application is currently running at:
- **Frontend**: https://8080-iuj5kdih7x1d4jegwd1it-871a975c.sg1.manus.computer/hotel-booking-standalone.html

## Screenshots

### Home Page
- Hero section with call-to-action
- Room grid with cards
- Price badges and amenities

### Booking Modal
- Room image and details
- Date pickers
- Guest selection
- Price calculation summary

### My Bookings Page
- List of all bookings
- Search functionality
- Booking details cards
- Status badges

## Support

For questions or issues:
1. Check the JavaScript console for errors
2. Ensure your browser supports localStorage
3. Clear browser cache if experiencing issues
4. Try a different modern browser

## License

This is a demonstration project. Feel free to use and modify as needed.

---

**Enjoy your stay at Luxury Haven Hotel! 🏨✨**
