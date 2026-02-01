# Deployment Guide

This guide will help you deploy the Hotel Booking Application to production.

## 📋 Pre-Deployment Checklist

- [ ] MongoDB Atlas cluster created and configured
- [ ] MongoDB connection string obtained
- [ ] Backend environment variables configured
- [ ] Frontend API URL updated for production
- [ ] Application tested locally
- [ ] All dependencies installed

## 🗄️ MongoDB Atlas Setup

### 1. Create MongoDB Atlas Account

1. Go to https://www.mongodb.com/cloud/atlas
2. Sign up for a free account
3. Create a new organization and project

### 2. Create a Cluster

1. Click "Build a Database"
2. Choose the FREE tier (M0)
3. Select a cloud provider and region closest to your users
4. Name your cluster (e.g., "hotel-booking-cluster")
5. Click "Create"

### 3. Configure Database Access

1. Go to "Database Access" in the left sidebar
2. Click "Add New Database User"
3. Choose "Password" authentication
4. Create a username and strong password
5. Set user privileges to "Read and write to any database"
6. Click "Add User"

### 4. Configure Network Access

1. Go to "Network Access" in the left sidebar
2. Click "Add IP Address"
3. For development: Click "Allow Access from Anywhere" (0.0.0.0/0)
4. For production: Add your server's specific IP address
5. Click "Confirm"

### 5. Get Connection String

1. Go to "Database" in the left sidebar
2. Click "Connect" on your cluster
3. Choose "Connect your application"
4. Copy the connection string
5. Replace `<password>` with your database user password
6. Replace `<dbname>` with `hotel_booking_db`

Example connection string:
```
mongodb+srv://username:password@cluster0.xxxxx.mongodb.net/hotel_booking_db?retryWrites=true&w=majority
```

## 🚀 Backend Deployment

### Option 1: Deploy to Heroku

1. **Install Heroku CLI**
   ```bash
   curl https://cli-assets.heroku.com/install.sh | sh
   ```

2. **Login to Heroku**
   ```bash
   heroku login
   ```

3. **Create Heroku App**
   ```bash
   cd backend
   heroku create your-hotel-api
   ```

4. **Set Environment Variables**
   ```bash
   heroku config:set MONGODB_URL="your-mongodb-atlas-connection-string"
   heroku config:set DATABASE_NAME="hotel_booking_db"
   ```

5. **Create Procfile**
   ```bash
   echo "web: uvicorn main:app --host 0.0.0.0 --port \$PORT" > Procfile
   ```

6. **Deploy**
   ```bash
   git init
   git add .
   git commit -m "Initial commit"
   git push heroku main
   ```

7. **Open App**
   ```bash
   heroku open
   ```

### Option 2: Deploy to Railway

1. Go to https://railway.app
2. Sign up and create a new project
3. Click "Deploy from GitHub repo"
4. Select your repository
5. Add environment variables:
   - `MONGODB_URL`: Your MongoDB Atlas connection string
   - `DATABASE_NAME`: hotel_booking_db
6. Railway will automatically detect Python and deploy

### Option 3: Deploy to Render

1. Go to https://render.com
2. Sign up and create a new Web Service
3. Connect your GitHub repository
4. Configure:
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `uvicorn main:app --host 0.0.0.0 --port $PORT`
5. Add environment variables:
   - `MONGODB_URL`: Your MongoDB Atlas connection string
   - `DATABASE_NAME`: hotel_booking_db
6. Click "Create Web Service"

## 🌐 Frontend Deployment

### Option 1: Deploy to Vercel (Recommended)

1. **Install Vercel CLI**
   ```bash
   npm install -g vercel
   ```

2. **Login to Vercel**
   ```bash
   vercel login
   ```

3. **Update API URL**
   - Open `frontend/src/api.js`
   - Update `API_BASE_URL` to your deployed backend URL:
   ```javascript
   const API_BASE_URL = 'https://your-hotel-api.herokuapp.com/api';
   ```

4. **Deploy**
   ```bash
   cd frontend
   vercel deploy --prod
   ```

### Option 2: Deploy to Netlify

1. **Install Netlify CLI**
   ```bash
   npm install -g netlify-cli
   ```

2. **Login to Netlify**
   ```bash
   netlify login
   ```

3. **Update API URL**
   - Open `frontend/src/api.js`
   - Update `API_BASE_URL` to your deployed backend URL

4. **Build and Deploy**
   ```bash
   cd frontend
   pnpm run build
   netlify deploy --prod --dir=dist
   ```

### Option 3: Deploy to GitHub Pages

1. **Install gh-pages**
   ```bash
   cd frontend
   pnpm add -D gh-pages
   ```

2. **Update package.json**
   ```json
   {
     "homepage": "https://yourusername.github.io/hotel-booking-app",
     "scripts": {
       "predeploy": "pnpm run build",
       "deploy": "gh-pages -d dist"
     }
   }
   ```

3. **Update vite.config.js**
   ```javascript
   export default defineConfig({
     base: '/hotel-booking-app/',
     // ... rest of config
   })
   ```

4. **Update API URL and Deploy**
   ```bash
   pnpm run deploy
   ```

## 🔧 Production Configuration

### Backend (.env for production)

```env
MONGODB_URL=mongodb+srv://username:password@cluster.mongodb.net/hotel_booking_db?retryWrites=true&w=majority
DATABASE_NAME=hotel_booking_db
```

### Frontend (api.js for production)

```javascript
const API_BASE_URL = process.env.VITE_API_URL || 'https://your-backend-url.com/api';
```

Then set environment variable in your deployment platform:
```
VITE_API_URL=https://your-backend-url.com/api
```

## 🔒 Security Best Practices

1. **Never commit .env files** - Add to .gitignore
2. **Use environment variables** for sensitive data
3. **Enable CORS properly** - Only allow your frontend domain
4. **Use HTTPS** in production
5. **Set strong MongoDB passwords**
6. **Restrict MongoDB network access** to your server IP
7. **Keep dependencies updated**

### Update CORS in main.py for production:

```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://your-frontend-domain.com"],  # Update this
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

## 📊 Monitoring

### Backend Health Check

```bash
curl https://your-backend-url.com/
```

### Check API Endpoints

```bash
curl https://your-backend-url.com/api/rooms
```

### View Logs

**Heroku:**
```bash
heroku logs --tail
```

**Railway/Render:**
Check the dashboard for real-time logs

## 🐛 Troubleshooting

### Backend Issues

1. **MongoDB Connection Failed**
   - Verify connection string is correct
   - Check network access whitelist
   - Ensure database user has correct permissions

2. **Port Already in Use**
   - Use environment variable for port: `--port $PORT`

3. **Module Not Found**
   - Ensure all dependencies are in requirements.txt
   - Run `pip install -r requirements.txt`

### Frontend Issues

1. **API Calls Failing**
   - Check API_BASE_URL is correct
   - Verify CORS is configured properly
   - Check network tab in browser DevTools

2. **Build Errors**
   - Clear node_modules and reinstall: `rm -rf node_modules && pnpm install`
   - Check for syntax errors in components

3. **Blank Page**
   - Check browser console for errors
   - Verify all imports are correct
   - Check that CSS files exist

## 📈 Performance Optimization

1. **Enable Gzip compression** on your server
2. **Use CDN** for static assets
3. **Optimize images** (already using Unsplash optimized URLs)
4. **Enable caching** for API responses
5. **Use production build** for frontend
6. **Monitor database queries** and add indexes if needed

## 🔄 Continuous Deployment

### GitHub Actions (Example)

Create `.github/workflows/deploy.yml`:

```yaml
name: Deploy

on:
  push:
    branches: [ main ]

jobs:
  deploy-backend:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Deploy to Heroku
        uses: akhileshns/heroku-deploy@v3.12.12
        with:
          heroku_api_key: ${{secrets.HEROKU_API_KEY}}
          heroku_app_name: "your-hotel-api"
          heroku_email: "your-email@example.com"
          appdir: "backend"

  deploy-frontend:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Deploy to Vercel
        uses: amondnet/vercel-action@v20
        with:
          vercel-token: ${{ secrets.VERCEL_TOKEN }}
          vercel-org-id: ${{ secrets.ORG_ID}}
          vercel-project-id: ${{ secrets.PROJECT_ID}}
          working-directory: ./frontend
```

## ✅ Post-Deployment Verification

1. [ ] Backend API is accessible
2. [ ] Frontend loads correctly
3. [ ] Can view room listings
4. [ ] Can create a booking
5. [ ] Can view bookings
6. [ ] Search functionality works
7. [ ] Mobile responsive design works
8. [ ] All images load properly
9. [ ] Forms validate correctly
10. [ ] Error handling works

## 📞 Support

If you encounter issues during deployment:
1. Check the troubleshooting section
2. Review platform-specific documentation
3. Check application logs
4. Verify environment variables are set correctly

---

**Happy Deploying! 🚀**
