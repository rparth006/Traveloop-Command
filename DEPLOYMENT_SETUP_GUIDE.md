# Traveloop - Complete Setup & Deployment Guide

## 📋 Table of Contents
1. Development Environment Setup
2. Database Configuration
3. Backend Deployment
4. Frontend Deployment
5. Production Deployment
6. API Documentation
7. Troubleshooting

---

## 1. Development Environment Setup

### Prerequisites
- Python 3.9+
- Node.js 16+ (for frontend)
- PostgreSQL 12+ (recommended for production)
- Git

### Backend Setup

```bash
# Clone repository
git clone <repository-url>
cd travel-scheduler

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Create .env file
cp .env.example .env

# Edit .env with your configuration
# DATABASE_URL=sqlite:///travel_database.db (for dev)
# DATABASE_URL=postgresql://user:pass@localhost/travel_db (for prod)
# SECRET_KEY=your-secret-key-here
# DEBUG=True
```

### Frontend Setup

```bash
# Create React app (or use Vue)
npx create-react-app traveloop-frontend
cd traveloop-frontend

# Install dependencies
npm install

# Create .env file
REACT_APP_API_URL=http://localhost:5000/api

# Start development server
npm start
```

---

## 2. Database Configuration

### Development (SQLite)

```python
# In models.py or settings
DATABASE_URL = 'sqlite:///travel_database.db'
```

### Production (PostgreSQL)

```bash
# Install PostgreSQL
# Ubuntu:
sudo apt-get install postgresql postgresql-contrib

# macOS (with Homebrew):
brew install postgresql

# Create database
createdb traveloop_db
createuser traveloop_user
psql -U postgres -d traveloop_db
# In psql:
ALTER USER traveloop_user WITH PASSWORD 'secure_password';
ALTER ROLE traveloop_user CREATEDB;
GRANT ALL PRIVILEGES ON DATABASE traveloop_db TO traveloop_user;
\q
```

### Initialize Database

```python
from models import create_database

# For first-time setup
create_database('postgresql://user:pass@localhost/traveloop_db')

# This creates all tables automatically
```

---

## 3. Backend Deployment (Local Development)

### Running the API Server

```bash
# Make sure virtual environment is activated
source venv/bin/activate  # or venv\Scripts\activate on Windows

# Set environment variables
export FLASK_APP=api_server.py
export FLASK_ENV=development
export DEBUG=True

# Run the server
python api_server.py

# Server will be available at http://localhost:5000
```

### Testing the Backend

```bash
# Run test suite
python -m pytest test_suite.py -v

# Run with coverage
python -m pytest test_suite.py --cov=. --cov-report=html

# Run specific test
python -m pytest test_suite.py::TraveloopTestBase::test_create_trip -v
```

---

## 4. Frontend Deployment (Local Development)

### Running the Frontend

```bash
cd traveloop-frontend
npm start

# Frontend will be available at http://localhost:3000
```

### Building for Production

```bash
npm run build

# Creates optimized production build in 'build' folder
# Size will be ~150KB (gzipped)
```

---

## 5. Production Deployment

### Option A: Deployment on Heroku

```bash
# Install Heroku CLI
# https://devcenter.heroku.com/articles/heroku-cli

# Login to Heroku
heroku login

# Create app
heroku create traveloop-app

# Set environment variables
heroku config:set DATABASE_URL=postgresql://...
heroku config:set SECRET_KEY=your-secret-key
heroku config:set DEBUG=False

# Deploy
git push heroku main

# View logs
heroku logs --tail
```

### Option B: Deployment on AWS/DigitalOcean

#### Backend (Using Gunicorn + Nginx)

```bash
# Install production dependencies
pip install gunicorn

# Run with Gunicorn (4 workers)
gunicorn -w 4 -b 0.0.0.0:5000 api_server:app

# Create systemd service file
sudo nano /etc/systemd/system/traveloop.service
```

Content of traveloop.service:
```ini
[Unit]
Description=Traveloop API Server
After=network.target

[Service]
User=www-data
WorkingDirectory=/home/user/traveloop
ExecStart=/home/user/traveloop/venv/bin/gunicorn -w 4 -b 127.0.0.1:5000 api_server:app
Restart=always

[Install]
WantedBy=multi-user.target
```

```bash
# Enable and start service
sudo systemctl enable traveloop
sudo systemctl start traveloop
```

#### Nginx Configuration

```nginx
server {
    listen 80;
    server_name api.traveloop.app;

    location / {
        proxy_pass http://127.0.0.1:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

#### Frontend (Using Nginx)

```nginx
server {
    listen 80;
    server_name traveloop.app;
    root /home/user/traveloop/build;

    location / {
        try_files $uri /index.html;
    }

    location /api {
        proxy_pass http://api.traveloop.app;
    }
}
```

### Option C: Docker Deployment

Create `Dockerfile`:
```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENV FLASK_APP=api_server.py
ENV PYTHONUNBUFFERED=1

EXPOSE 5000

CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "api_server:app"]
```

Create `docker-compose.yml`:
```yaml
version: '3.8'
services:
  db:
    image: postgres:15
    environment:
      POSTGRES_DB: traveloop_db
      POSTGRES_USER: traveloop_user
      POSTGRES_PASSWORD: secure_password
    volumes:
      - postgres_data:/var/lib/postgresql/data
    ports:
      - "5432:5432"

  api:
    build: .
    ports:
      - "5000:5000"
    environment:
      DATABASE_URL: postgresql://traveloop_user:secure_password@db:5432/traveloop_db
      SECRET_KEY: your-secret-key
      DEBUG: "False"
    depends_on:
      - db

  frontend:
    image: node:18
    working_dir: /app
    volumes:
      - ./traveloop-frontend:/app
    ports:
      - "3000:3000"
    command: npm start

volumes:
  postgres_data:
```

Deploy with Docker:
```bash
docker-compose up -d
```

---

## 6. API Documentation

### Base URL
```
http://localhost:5000 (development)
https://api.traveloop.app (production)
```

### Authentication
Include JWT token in headers:
```
Authorization: Bearer <your-jwt-token>
```

### Key Endpoints

#### Trips
```
GET  /api/trips                    # Get all user trips
POST /api/trips                    # Create new trip
GET  /api/trips/<id>               # Get trip details
PUT  /api/trips/<id>               # Update trip
DELETE /api/trips/<id>             # Delete trip
```

#### Cities/Stops
```
GET  /api/trips/<id>/stops         # Get all stops
POST /api/trips/<id>/stops         # Add stop
DELETE /api/stops/<id>             # Delete stop
POST /api/trips/<id>/stops/reorder # Reorder stops
```

#### Activities
```
GET  /api/trips/<id>/activities    # Get all activities
POST /api/stops/<id>/activities    # Add activity
PUT  /api/activities/<id>          # Update activity
DELETE /api/activities/<id>        # Delete activity
```

#### Expenses
```
GET  /api/trips/<id>/expenses      # Get all expenses
POST /api/trips/<id>/expenses      # Add expense
PUT  /api/expenses/<id>            # Update expense
DELETE /api/expenses/<id>          # Delete expense
GET  /api/trips/<id>/budget-status # Get budget status
```

#### Sharing
```
POST /api/trips/<id>/share         # Create share link
GET  /api/shared/<token>           # View shared trip
POST /api/trips/<id>/clone         # Clone trip
```

#### Analytics (Admin)
```
GET  /admin/analytics/overview     # Platform overview
GET  /admin/analytics/users        # User analytics
GET  /admin/analytics/destinations # Destination analytics
```

---

## 7. Environment Variables

Create `.env` file:
```env
# Database
DATABASE_URL=sqlite:///travel_database.db
# DATABASE_URL=postgresql://user:password@localhost/traveloop_db

# Flask
FLASK_ENV=development
DEBUG=True
SECRET_KEY=your-secret-key-change-in-production

# JWT
JWT_SECRET_KEY=jwt-secret-key

# API Settings
API_HOST=0.0.0.0
API_PORT=5000
CORS_ORIGINS=http://localhost:3000,https://traveloop.app

# Email (for notifications)
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_USERNAME=your-email@gmail.com
MAIL_PASSWORD=your-app-password

# AWS S3 (for file upload)
AWS_ACCESS_KEY_ID=your-key
AWS_SECRET_ACCESS_KEY=your-secret
AWS_S3_BUCKET=traveloop-bucket
```

---

## 8. Troubleshooting

### Common Issues

**Issue: Database Connection Error**
```
Solution:
1. Check DATABASE_URL in .env
2. Verify database is running (for PostgreSQL)
3. Ensure database credentials are correct
4. Run migrate command if needed
```

**Issue: Port Already in Use**
```bash
# Find and kill process on port
lsof -ti:5000 | xargs kill -9  # macOS/Linux
netstat -ano | findstr :5000   # Windows
taskkill /PID <PID> /F
```

**Issue: CORS Errors**
```
Solution:
1. Check CORS_ORIGINS in .env
2. Verify frontend URL is in allowed origins
3. Check browser console for actual error
4. Update Flask-CORS configuration
```

**Issue: Authentication Failed**
```
Solution:
1. Check JWT_SECRET_KEY is set correctly
2. Verify token is included in Authorization header
3. Check token hasn't expired
4. Regenerate token if needed
```

### Performance Optimization

```python
# In api_server.py
from functools import lru_cache

# Cache expensive queries
@lru_cache(maxsize=128)
def get_cities(country):
    return query_cities(country)

# Use connection pooling
from sqlalchemy import create_engine
engine = create_engine(
    DATABASE_URL,
    pool_size=10,
    max_overflow=20
)
```

### Monitoring & Logging

```python
import logging

# Configure logging
logging.basicConfig(
    filename='app.log',
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)

# Use in code
logger.info(f"Trip created: {trip.id}")
logger.error(f"Error: {str(e)}")
```

---

## Quick Start Commands

```bash
# Development
source venv/bin/activate
python api_server.py

# Testing
python -m pytest test_suite.py -v

# Production Build
npm run build
gunicorn -w 4 -b 0.0.0.0:5000 api_server:app

# Docker
docker-compose up -d
```

---

## Support & Resources

- API Documentation: `/docs` (when using Swagger)
- Issue Tracker: GitHub Issues
- Community Forum: https://community.traveloop.app
- Documentation: https://docs.traveloop.app

---

**Version:** 1.0.0  
**Last Updated:** May 2026  
**Status:** Production Ready
