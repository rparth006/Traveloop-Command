# Traveloop API - Quick Reference Guide

## 🚀 Quick Start

```bash
# Start API Server
python api_server.py

# Base URL
http://localhost:5000/api
```

---

## 📚 API Endpoints Reference

### Authentication
```
POST   /api/auth/login           - Login user
POST   /api/auth/signup          - Create new account
POST   /api/auth/forgot-password - Request password reset
POST   /api/auth/reset-password  - Reset password with token
```

### Trips (CRUD)
```
GET    /api/trips                - Get all user trips
POST   /api/trips                - Create new trip
GET    /api/trips/<id>           - Get specific trip
PUT    /api/trips/<id>           - Update trip
DELETE /api/trips/<id>           - Delete trip
```

### Cities/Stops
```
GET    /api/trips/<id>/stops             - Get all stops in trip
POST   /api/trips/<id>/stops             - Add new city
DELETE /api/stops/<id>                   - Remove stop
POST   /api/trips/<id>/stops/reorder     - Reorder cities
GET    /api/cities?search=query          - Search cities
```

### Activities
```
GET    /api/trips/<id>/activities            - Get all activities
POST   /api/stops/<id>/activities            - Add activity to stop
PUT    /api/activities/<id>                  - Update activity
DELETE /api/activities/<id>                  - Delete activity
GET    /api/activities/trending              - Get trending activities
```

### Expenses & Budget
```
GET    /api/trips/<id>/expenses              - Get all expenses
POST   /api/trips/<id>/expenses              - Log expense
PUT    /api/expenses/<id>                    - Update expense
DELETE /api/expenses/<id>                    - Delete expense
GET    /api/trips/<id>/budget-status         - Get budget overview
GET    /api/trips/<id>/budget-breakdown      - Get cost breakdown
```

### Itinerary
```
GET    /api/trips/<id>/itinerary             - Get day-wise itinerary
GET    /api/trips/<id>/schedule              - Get trip timeline
```

### Sharing & Social
```
POST   /api/trips/<id>/share                 - Create share link
GET    /api/shared/<token>                   - View shared trip
POST   /api/trips/<id>/clone                 - Clone trip as template
GET    /api/trips/trending                   - Get trending trips
```

### User Profile
```
GET    /api/user/profile                     - Get user profile
PUT    /api/user/profile                     - Update profile
PUT    /api/user/password                    - Change password
PUT    /api/user/preferences                 - Update preferences
GET    /api/user/sessions                    - Get active sessions
```

### Admin Analytics (Requires Admin)
```
GET    /admin/analytics/overview             - Platform overview
GET    /admin/analytics/users                - User analytics
GET    /admin/analytics/destinations         - Popular destinations
GET    /admin/analytics/trends               - Trend analysis
GET    /admin/analytics/engagement           - Engagement metrics
```

### Health Check
```
GET    /health                               - Server health status
```

---

## 📝 Example Requests

### Create a Trip
```bash
curl -X POST http://localhost:5000/api/trips \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Europe Summer 2024",
    "start_date": "2024-06-01",
    "end_date": "2024-06-30",
    "budget": 150000,
    "description": "Amazing European adventure"
  }'
```

### Add a City to Trip
```bash
curl -X POST http://localhost:5000/api/trips/1/stops \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "location": "Dubai",
    "arrival_date": "2024-06-01",
    "departure_date": "2024-06-05",
    "latitude": 25.2048,
    "longitude": 55.2708,
    "notes": "Stay at Burj Khalifa area"
  }'
```

### Add Activity to a Stop
```bash
curl -X POST http://localhost:5000/api/stops/1/activities \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Desert Safari",
    "activity_type": "adventure",
    "start_time": "2024-06-02T15:00:00",
    "end_time": "2024-06-02T22:00:00",
    "cost": 5000,
    "description": "Evening desert safari with BBQ dinner"
  }'
```

### Record an Expense
```bash
curl -X POST http://localhost:5000/api/trips/1/expenses \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "description": "Hotel booking",
    "amount": 50000,
    "category": "accommodation",
    "expense_date": "2024-06-01",
    "payment_method": "card",
    "paid_by": "John",
    "notes": "Burj Khalifa Hotel, 5 nights"
  }'
```

### Get Budget Status
```bash
curl -X GET http://localhost:5000/api/trips/1/budget-status \
  -H "Authorization: Bearer YOUR_TOKEN"
```

Response:
```json
{
  "budget_status": {
    "total_budget": 150000,
    "total_spent": 95000,
    "remaining": 55000,
    "percentage_used": 63.33,
    "status": "on_track"
  },
  "alerts": []
}
```

### Create Share Link
```bash
curl -X POST http://localhost:5000/api/trips/1/share \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "expires_in_days": 30
  }'
```

Response:
```json
{
  "message": "Trip shared successfully",
  "public_url": "https://traveloop.app/trips/abc123def456",
  "share_token": "abc123def456"
}
```

### Clone a Trip
```bash
curl -X POST http://localhost:5000/api/trips/1/clone \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "My Europe Trip",
    "keep_dates": false
  }'
```

### Get Day-wise Itinerary
```bash
curl -X GET http://localhost:5000/api/trips/1/itinerary \
  -H "Authorization: Bearer YOUR_TOKEN"
```

Response:
```json
{
  "2024-06-01": {
    "stops": [{"id": 1, "location": "Dubai"}],
    "activities": [{"id": 1, "name": "Airport pickup", "time": "2024-06-01 10:00"}]
  },
  "2024-06-02": {
    "stops": [{"id": 1, "location": "Dubai"}],
    "activities": [{"id": 2, "name": "Desert Safari", "time": "2024-06-02 15:00"}]
  }
}
```

---

## 🔐 Authentication

### Get Token (Login)
```bash
curl -X POST http://localhost:5000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "user@example.com",
    "password": "password123"
  }'
```

### Use Token in Requests
```bash
# All endpoints except public ones require this header:
Authorization: Bearer YOUR_JWT_TOKEN
```

---

## 📊 Response Format

### Success Response (200)
```json
{
  "message": "Success message here",
  "data": {
    "trip_id": 1,
    "title": "Europe Trip"
  }
}
```

### Error Response (4xx/5xx)
```json
{
  "error": "Error message here",
  "status": 400,
  "details": "Additional error details if available"
}
```

---

## 🎯 Common Status Codes

| Code | Meaning |
|------|---------|
| 200 | OK - Request successful |
| 201 | Created - Resource created |
| 400 | Bad Request - Invalid input |
| 401 | Unauthorized - Missing/invalid token |
| 403 | Forbidden - Access denied |
| 404 | Not Found - Resource not found |
| 500 | Server Error - Internal error |

---

## 💡 API Tips

1. **Always include Authorization header** for protected endpoints
2. **Date format:** YYYY-MM-DD (ISO 8601)
3. **DateTime format:** YYYY-MM-DDTHH:MM:SS (ISO 8601)
4. **Currency:** Default INR, but configurable per user
5. **Pagination:** Implemented on list endpoints (limit, offset)
6. **Rate Limiting:** Coming soon (tokens per minute)
7. **CORS:** Enabled for http://localhost:3000 (development)

---

## 🧪 Testing the API

### Using Postman
1. Import the collection from `postman_collection.json`
2. Set environment variables (API_URL, TOKEN)
3. Run test requests

### Using cURL
```bash
# Test health check
curl http://localhost:5000/health

# Test protected endpoint (will fail without token)
curl -X GET http://localhost:5000/api/trips
# Response: {"message": "Token is missing!"}, 401

# Login first
TOKEN=$(curl -X POST http://localhost:5000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"user@example.com","password":"pass"}' \
  | jq '.token')

# Use token
curl -X GET http://localhost:5000/api/trips \
  -H "Authorization: Bearer $TOKEN"
```

### Using Python Requests
```python
import requests

BASE_URL = "http://localhost:5000/api"
HEADERS = {"Authorization": f"Bearer {TOKEN}"}

# Get all trips
response = requests.get(f"{BASE_URL}/trips", headers=HEADERS)
print(response.json())

# Create new trip
trip_data = {
    "title": "Summer Vacation",
    "start_date": "2024-07-01",
    "end_date": "2024-07-15",
    "budget": 100000
}
response = requests.post(f"{BASE_URL}/trips", json=trip_data, headers=HEADERS)
print(response.json())
```

---

## 📦 Batch Operations

### Reorder Multiple Stops
```bash
curl -X POST http://localhost:5000/api/trips/1/stops/reorder \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "stop_ids": [3, 1, 2]
  }'
```

---

## 🔄 Workflow Example

```
1. User Signs Up
   POST /api/auth/signup

2. User Logs In
   POST /api/auth/login
   →receives JWT token

3. User Creates Trip
   POST /api/trips
   →receives trip_id: 1

4. User Adds Cities
   POST /api/trips/1/stops (Dubai)
   POST /api/trips/1/stops (Barcelona)
   POST /api/trips/1/stops (Paris)

5. User Adds Activities
   POST /api/stops/1/activities (Desert Safari)
   POST /api/stops/2/activities (Sagrada Familia)

6. User Tracks Expenses
   POST /api/trips/1/expenses (Hotel)
   POST /api/trips/1/expenses (Flight)

7. User Checks Budget
   GET /api/trips/1/budget-status

8. User Shares Trip
   POST /api/trips/1/share
   →receives public URL

9. Other User Clones Template
   POST /api/trips/1/clone
   →creates new trip from template

10. User Exports Itinerary
    GET /api/trips/1/itinerary
```

---

## 🚨 Rate Limiting

Coming soon! Will implement:
- 1000 requests/hour per user
- Burst limit: 100 requests/minute
- 429 Too Many Requests response

---

## 📞 Support

- **Bug Reports:** GitHub Issues
- **Feature Requests:** GitHub Discussions
- **Documentation:** https://docs.traveloop.app
- **Email:** support@traveloop.app

---

**Version:** 1.0.0  
**Last Updated:** May 2026  
**API Status:** Production Ready ✅
