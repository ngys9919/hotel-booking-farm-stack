# 🏨 Luxury Haven Hotel - FARM Stack Booking Application

A full-stack hotel room booking application built with the **FARM stack** (FastAPI, Async/Motor, React, MongoDB).

## 🌐 Repository & Demo

- **GitHub Repository**: https://github.com/ngys9919/hotel-booking-farm-stack
- **Live Demo (Standalone)**: https://ngys9919.github.io/luxury-haven-hotel/

## ✨ Features

### Backend (FastAPI + Python)
- **RESTful API** with 6 endpoints for rooms and bookings
- **Async MongoDB** integration with Motor driver
- **Mock database** fallback for testing without MongoDB
- **Automatic initialization** with 6 luxury sample rooms
- **Real-time price calculation** based on stay duration
- **Data validation** with Pydantic models
- **Auto-generated API documentation** at `/docs`
- **CORS enabled** for frontend integration

### Frontend (React + Vite)
- **Beautiful landing page** with hero section
- **Room listings** with high-quality images and details
- **Interactive booking modal** with date pickers
- **"My Bookings" page** with search functionality
- **Success notifications** and error handling
- **Fully responsive design** (mobile, tablet, desktop)
- **Modern UI** with smooth animations

### Database (MongoDB)
- **MongoDB Atlas** support for cloud database
- **Local MongoDB** support for development
- **Mock in-memory database** for testing
- **Automatic schema validation**
- **Sample data initialization**

## 📁 Project Structure

```
hotel-booking-app/
├── backend/
│   ├── main.py                 # FastAPI application
│   ├── models.py               # Pydantic models
│   ├── database.py             # MongoDB connection
│   ├── database_mock.py        # Mock database for testing
│   ├── requirements.txt        # Python dependencies
│   ├── .env                    # Environment variables (not in git)
│   └── .env.example            # Example environment configuration
├── frontend/
│   ├── src/
│   │   ├── App.jsx             # Main React component
│   │   ├── App.css             # Premium styling
│   │   ├── api.js              # API service layer
│   │   ├── components/         # React components
│   │   │   ├── Hero.jsx
│   │   │   ├── Navbar.jsx
│   │   │   ├── RoomCard.jsx
│   │   │   └── BookingModal.jsx
│   │   └── pages/              # Page components
│   │       ├── Home.jsx
│   │       └── MyBookings.jsx
│   ├── public/                 # Static assets
│   ├── index.html              # HTML entry point
│   ├── package.json            # Node dependencies
│   ├── vite.config.js          # Vite configuration
│   └── eslint.config.js        # ESLint configuration
├── hotel-booking-standalone.html  # Standalone single-file version
├── README.md                   # This file
├── PROJECT_SUMMARY.md          # Detailed project documentation
├── DEPLOYMENT.md               # Deployment instructions
├── STANDALONE-README.md        # Standalone version documentation
└── .gitignore                  # Git ignore rules
```

## 🚀 Quick Start

### Prerequisites

- **Python 3.11+** installed
- **Node.js 22+** and **pnpm** installed
- **MongoDB** (Atlas, local, or use mock database)

### 1. Clone the Repository

```bash
git clone https://github.com/ngys9919/hotel-booking-farm-stack.git
cd hotel-booking-farm-stack
```

### 2. Backend Setup

```bash
cd backend

# Install Python dependencies
pip install -r requirements.txt

# Configure environment variables
cp .env.example .env
# Edit .env with your MongoDB connection string

# Run the backend server
python3 main.py
```

Backend will be available at: **http://localhost:8000**  
API documentation at: **http://localhost:8000/docs**

### 3. Frontend Setup

```bash
cd frontend

# Install Node dependencies
pnpm install

# Run the development server
pnpm run dev
```

Frontend will be available at: **http://localhost:5173**

### 4. Access the Application

Open your browser and navigate to **http://localhost:5173**

## 🔧 Configuration

### MongoDB Setup

**Option 1: MongoDB Atlas (Recommended for Production)**

1. Create a free account at [MongoDB Atlas](https://www.mongodb.com/cloud/atlas)
2. Create a new cluster
3. Get your connection string
4. Update `backend/.env`:
   ```
   MONGODB_URL=mongodb+srv://<username>:<password>@<cluster>.mongodb.net/?retryWrites=true&w=majority
   DATABASE_NAME=hotel_booking_db
   ```

**Option 2: Local MongoDB**

```bash
# Install MongoDB locally
# Ubuntu/Debian:
sudo apt-get install mongodb

# macOS:
brew install mongodb-community

# Start MongoDB
mongod --dbpath /path/to/data/directory
```

Update `backend/.env`:
```
MONGODB_URL=mongodb://localhost:27017/
DATABASE_NAME=hotel_booking_db
```

**Option 3: Mock Database (No MongoDB Required)**

The application automatically falls back to an in-memory mock database if MongoDB connection fails. Perfect for testing!

### Environment Variables

**Backend (`backend/.env`)**:
```bash
MONGODB_URL=mongodb://localhost:27017/
DATABASE_NAME=hotel_booking_db
API_HOST=0.0.0.0
API_PORT=8000
FRONTEND_URL=http://localhost:5173
```

**Frontend (`frontend/src/api.js`)**:
```javascript
const API_BASE_URL = 'http://localhost:8000/api';
```

## 📊 API Endpoints

### Rooms
- `GET /api/rooms` - Get all available rooms
- `GET /api/rooms/{room_id}` - Get specific room details

### Bookings
- `GET /api/bookings` - Get all bookings
- `GET /api/bookings/{booking_id}` - Get specific booking
- `POST /api/bookings` - Create new booking
- `DELETE /api/bookings/{booking_id}` - Cancel booking

### Health Check
- `GET /` - API health check

### Documentation
- `GET /docs` - Interactive API documentation (Swagger UI)
- `GET /redoc` - Alternative API documentation (ReDoc)

## 🏨 Available Rooms

1. **Deluxe Ocean View Suite** - $299.99/night (Max 2 guests)
2. **Executive Business Room** - $189.99/night (Max 2 guests)
3. **Family Garden Suite** - $349.99/night (Max 4 guests)
4. **Cozy Standard Room** - $129.99/night (Max 2 guests)
5. **Presidential Penthouse** - $799.99/night (Max 2 guests)
6. **Mountain View Cabin** - $249.99/night (Max 2 guests)

## 🎨 Customization

### Adding New Rooms

Edit `backend/database_mock.py` or add directly to MongoDB:

```python
{
    "id": 7,
    "name": "New Room Name",
    "description": "Room description",
    "price": 199.99,
    "image": "https://images.unsplash.com/photo-...",
    "maxGuests": 2,
    "amenities": ["WiFi", "TV", "Mini Bar"]
}
```

### Changing Colors

Edit `frontend/src/App.css`:

```css
:root {
  --primary-color: #1e3a5f;    /* Navy blue */
  --secondary-color: #e63946;  /* Red */
  --accent-color: #f4a261;     /* Orange */
}
```

### Updating API URL

Edit `frontend/src/api.js`:

```javascript
const API_BASE_URL = 'https://your-api-domain.com/api';
```

## 🚢 Deployment

See [DEPLOYMENT.md](DEPLOYMENT.md) for detailed deployment instructions for:

- **Backend**: Heroku, Railway, Render, DigitalOcean
- **Frontend**: Vercel, Netlify, GitHub Pages
- **Database**: MongoDB Atlas
- **Full-Stack**: Docker, AWS, Google Cloud

## 🧪 Testing

### Manual Testing

1. **Test Booking Flow**:
   - Browse rooms on home page
   - Click "Book Now"
   - Fill in details and select dates
   - Verify price calculation
   - Confirm booking
   - Check "My Bookings" page

2. **Test API**:
   - Visit http://localhost:8000/docs
   - Try each endpoint
   - Verify responses

## 📝 Development

### Backend Development

```bash
cd backend

# Run with auto-reload
python3 main.py

# Or use uvicorn directly
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### Frontend Development

```bash
cd frontend

# Run dev server
pnpm run dev

# Build for production
pnpm run build

# Preview production build
pnpm run preview
```

## 🛠️ Tech Stack

### Backend
- **FastAPI** - Modern Python web framework
- **Motor** - Async MongoDB driver
- **Pydantic** - Data validation
- **Uvicorn** - ASGI server
- **Python 3.11+** - Programming language

### Frontend
- **React 18** - UI library
- **Vite** - Build tool and dev server
- **Vanilla CSS** - Styling
- **JavaScript (ES6+)** - Programming language

### Database
- **MongoDB** - NoSQL database
- **MongoDB Atlas** - Cloud database service

### DevOps
- **Git** - Version control
- **GitHub** - Code hosting
- **pnpm** - Package manager
- **ESLint** - Code linting

## 📄 License

This project is created for educational and demonstration purposes.

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📧 Support

For issues or questions:
- Open an issue on GitHub
- Check the documentation in `PROJECT_SUMMARY.md`
- Review deployment guide in `DEPLOYMENT.md`

## 🎯 Roadmap

### Planned Features
- [ ] User authentication and authorization
- [ ] Email notifications for bookings
- [ ] Payment integration (Stripe/PayPal)
- [ ] Admin dashboard for managing rooms
- [ ] Reviews and ratings system
- [ ] Multi-language support
- [ ] Calendar view for availability
- [ ] Image upload for rooms
- [ ] Advanced search and filters
- [ ] Booking modifications and cancellations

## 🏆 Acknowledgments

- Images from [Unsplash](https://unsplash.com/)
- Icons and design inspiration from modern hotel booking platforms
- Built with the FARM stack (FastAPI, Async/Motor, React, MongoDB)

---

**Built with ❤️ using the FARM Stack**

**Repository**: https://github.com/ngys9919/hotel-booking-farm-stack  
**Live Demo**: https://ngys9919.github.io/luxury-haven-hotel/  
**Documentation**: See PROJECT_SUMMARY.md for detailed information

---

*Last Updated: February 2026*
