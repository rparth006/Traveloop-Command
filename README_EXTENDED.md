# 🌍 Complete Travel Database System

A comprehensive relational database solution for travel planning with user authentication, city/activity catalogs, packing checklists, and trip sharing features.

---

## 📋 Project Overview

This system provides everything needed to build a travel planning application:
- **User Management**: Signup/login with password hashing
- **Trip Planning**: Create trips with multiple stops and activities
- **City Catalog**: 14+ popular cities with cost indices
- **Activity Recommendations**: 100+ curated activities with ratings
- **Packing Checklists**: Default items with custom additions
- **Trip Sharing**: Generate public URLs for sharing with friends
- **Data Management**: Complete CRUD operations with relationships

---

## 🎯 Key Features

### ✅ User Authentication
- Signup with email validation
- Secure login with password hashing
- Password change functionality
- Email uniqueness enforcement

### ✅ Rich Trip Planning
- Multiple stops per trip
- Activities linked to trips or specific stops
- Expense tracking by category
- Trip budget management

### ✅ City & Activity Data
- **14 Popular Cities**: Paris, Tokyo, Goa, Kerala, Bangkok, etc.
- **8 Activity Types**: Sightseeing, Food Tours, Hiking, Water Sports, Museums, Shopping, Adventure, Relaxation
- **100+ Recommended Activities**: Each with estimated cost, duration, and ratings
- **Cost Indices**: Relative pricing for budget planning

### ✅ Packing System
- **50+ Default Items**: Organized by category
- **Smart Checklists**: Create/manage per trip
- **Progress Tracking**: Check off items, track completion
- **Custom Items**: Add your own items beyond defaults

### ✅ Trip Sharing
- Generate unique public URLs
- Password-protected sharing
- Configurable expiration dates
- Edit permissions control
- View count tracking

---

## 📁 Project Files

| File | Purpose |
|------|---------|
| **models_extended.py** | Extended SQLAlchemy ORM models with all new tables |
| **seed_data.py** | Populate database with cities, activities, packing items |
| **auth_and_sharing.py** | Authentication and sharing functionality |
| **database_operations.py** | Helper functions for CRUD operations |
| **test_suite.py** | Comprehensive testing of all features |
| **INTEGRATION_GUIDE.py** | Complete workflow examples |
| **QUICK_START.py** | 5-minute quick start guide |
| **travel_database.db** | SQLite database (auto-created) |

---

## 🚀 Quick Start

### Step 1: Install Dependencies
```bash
pip install sqlalchemy
```

### Step 2: Initialize Database
```bash
python models_extended.py
```

### Step 3: Seed Reference Data
```bash
python seed_data.py
```

This populates:
- ✓ 14 cities with coordinates and cost indices
- ✓ 8 activity types with cost ranges
- ✓ 100+ activities per city with ratings
- ✓ 50+ packing items organized by category
- ✓ 1 sample user with test trip

### Step 4: Run Tests
```bash
python test_suite.py
```

---

## 💻 Basic Usage Examples

### User Authentication

```python
from auth_and_sharing import AuthenticationManager

auth = AuthenticationManager()

# Signup
result = auth.signup("Priya Sharma", "priya@example.com", "password123")
if result['success']:
    user_id = result['user'].id

# Login
result = auth.login("priya@example.com", "password123")
if result['success']:
    user = result['user']
```

### Browse Cities & Activities

```python
from auth_and_sharing import DataRetrievalManager

data = DataRetrievalManager()

# Get all cities
cities = data.get_all_cities()

# Get activities in a city
activities = data.get_city_activities(city_id=1)

# Get countries
countries = data.get_countries()
```

### Create Trip with Stops

```python
from models_extended import Trip, Stop, Activity
from datetime import date

trip = Trip(
    user_id=user_id,
    title="Kerala Backwater Holiday",
    destination="Kerala",
    start_date=date(2026, 6, 1),
    end_date=date(2026, 6, 10),
    budget=50000
)
session.add(trip)
session.commit()

stop = Stop(
    trip_id=trip.id,
    location="Alleppey",
    arrival_date=date(2026, 6, 1),
    sequence_order=1
)
session.add(stop)
session.commit()
```

### Create Packing Checklist

```python
from models_extended import PackingChecklist, PackingChecklistItem

checklist = PackingChecklist(
    user_id=user_id,
    trip_id=trip.id,
    name="Kerala Trip Packing"
)
session.add(checklist)
session.commit()

# Add items
for item in packing_items:
    checklist_item = PackingChecklistItem(
        checklist_id=checklist.id,
        packing_item_id=item.id,
        name=item.name,
        category=item.category
    )
    session.add(checklist_item)
session.commit()
```

### Share Trip

```python
from auth_and_sharing import TripSharingManager

sharing = TripSharingManager()

result = sharing.generate_share_link(
    trip_id=trip.id,
    user_id=user_id,
    can_edit=True,
    expiry_days=30
)

if result['success']:
    print(f"Share URL: {result['full_url']}")
```

---

## 📊 Database Schema

### Core Tables
- **users**: Traveler information with password hashing
- **trips**: Trip details linked to users
- **stops**: Locations/destinations with sequence ordering
- **activities**: Events with optional stop linking
- **expenses**: Cost tracking by category

### New Tables
- **cities**: Popular destinations with cost indices
- **activity_types**: Categories of activities
- **city_activities**: Recommended activities per city
- **packing_items**: Default packing list items
- **packing_checklists**: User's trip-specific packing lists
- **packing_checklist_items**: Items in each checklist
- **shared_trips**: Public sharing configuration

### Relationships
```
User (1:N)→ Trip (1:N)→ Stop (1:N)→ Activity
                      ↓
                    Expense
                      ↓
              PackingChecklist
                      
Trip (1:1)→ SharedTrip (with public URL)

Stop (0:1)→ City (linked to cities catalog)
Activity (0:1)→ ActivityType (linked to activity types)
```

---

## 🔐 Authentication Features

### Signup
```python
auth.signup(name, email, password, phone, address)
# Returns: {
#   'success': bool,
#   'user': User object,
#   'message': str
# }
```

### Login
```python
auth.login(email, password)
# Verifies hashed password
```

### Password Change
```python
auth.change_password(user_id, old_password, new_password)
```

---

## 🔗 Trip Sharing Features

### Generate Share Link
```python
sharing.generate_share_link(
    trip_id,
    user_id,
    can_edit=False,
    expiry_days=30,
    password=None
)
# Returns unique public URL
```

### Access Shared Trip
```python
sharing.access_shared_trip(public_url, password=None)
# Returns trip details with view count increment
```

### Get User's Shared Trips
```python
sharing.get_shared_trips_for_user(user_id)
# Returns all shares created by user
```

---

## 🧳 Packing Checklist System

### Create Checklist
```python
checklist = PackingChecklist(
    user_id=user_id,
    trip_id=trip_id,
    name="Trip Packing List"
)
```

### Add Default Items
```python
packing_items = session.query(PackingItem).filter_by(
    category='Clothing'
).all()

for item in packing_items:
    PackingChecklistItem(
        checklist_id=checklist.id,
        packing_item_id=item.id,
        name=item.name,
        category=item.category
    )
```

### Add Custom Items
```python
custom_item = PackingChecklistItem(
    checklist_id=checklist.id,
    name="Custom Item",
    category="Photography",
    quantity=1
)
```

### Track Progress
```python
packed = sum(1 for item in checklist.items if item.is_packed)
total = len(checklist.items)
progress = (packed / total) * 100
```

---

## 📈 Available Cities

### India
- Delhi, Mumbai, Goa, Kerala, Jaipur

### Europe
- Paris, Amsterdam, Barcelona, Rome

### Southeast Asia
- Bangkok, Bali, Hanoi

### Japan
- Tokyo, Kyoto

---

## 🎯 Activity Types & Cost Ranges

| Type | Cost Range | Avg Duration |
|------|-----------|--------------|
| Sightseeing | $10-100 | 3 hours |
| Food Tour | $20-150 | 2.5 hours |
| Hiking | $0-100 | 4 hours |
| Water Sports | $50-200 | 2 hours |
| Museum Visit | $10-50 | 3 hours |
| Shopping | $20-500 | 3 hours |
| Adventure Sports | $50-300 | 1.5 hours |
| Relaxation | $30-200 | 2 hours |

---

## 📦 Packing Item Categories

- **Clothing**: T-shirts, pants, swimwear, jackets, shoes
- **Electronics**: Phone chargers, power banks, headphones
- **Documents**: Passport, tickets, insurance, visas
- **Toiletries**: Toothbrush, medications, sunscreen, first aid
- **Accessories**: Hats, belts, jewelry, bags
- **Recreation**: Books, travel guides, cards, games

---

## 🧪 Testing

Run comprehensive tests:
```bash
python test_suite.py
```

Tests cover:
- ✓ Database initialization
- ✓ User authentication (signup/login/password)
- ✓ City and activity data loading
- ✓ Trip creation with relationships
- ✓ Packing checklist functionality
- ✓ Trip sharing and public URLs
- ✓ Data retrieval methods

---

## 🔍 Data Validation

The system validates:
- ✓ Email format uniqueness
- ✓ Password strength (minimum 6 characters)
- ✓ Foreign key constraints
- ✓ Cascade delete rules
- ✓ Data type constraints

---

## 📚 Documentation

- **INTEGRATION_GUIDE.py**: Complete workflow examples
- **QUICK_START.py**: 5-minute setup guide
- **auth_and_sharing.py**: Authentication & sharing docs
- **database_operations.py**: CRUD helper docs
- **seed_data.py**: Data seeding examples

---

## 🚨 Important Notes

### Cascade Delete
- Deleting a User cascades to all Trips
- Deleting a Trip cascades to Stops, Activities, Expenses
- Deleting a Stop sets stop_id to NULL in Activities

### Authentication
- Passwords are hashed using SHA-256
- Email must be unique per user
- Session management via SQLAlchemy

### Data Retrieval
- All data loads from database with relationships
- Helper classes manage common operations
- Transaction support for consistency

---

## 💡 Tips & Best Practices

1. **Always commit after changes**
   ```python
   session.add(record)
   session.commit()
   ```

2. **Use helper classes for common operations**
   ```python
   from auth_and_sharing import TripSharingManager
   ```

3. **Close sessions when done**
   ```python
   session.close()
   db.close()
   ```

4. **Validate data before insertion**
   ```python
   if not is_valid_email(email):
       return error
   ```

5. **Use transactions for atomic operations**
   ```python
   try:
       session.add(record)
       session.commit()
   except:
       session.rollback()
   ```

---

## 🐛 Troubleshooting

| Issue | Solution |
|-------|----------|
| IntegrityError: UNIQUE constraint | Use unique email for each user |
| ForeignKeyConstraintError | Create parent record before child |
| Table doesn't exist | Run `python models_extended.py` |
| No cities found | Run `python seed_data.py` |
| Session already closed | Create new session |

---

## 🎓 Learning Path

1. Start with **QUICK_START.py** - Basic setup
2. Read **INTEGRATION_GUIDE.py** - Complete workflows
3. Run **seed_data.py** - Populate reference data
4. Execute **test_suite.py** - Verify functionality
5. Study **auth_and_sharing.py** - Authentication logic
6. Explore **models_extended.py** - Database schema

---

## 📞 Support

For questions or issues:
1. Check INTEGRATION_GUIDE for examples
2. Review test_suite.py for validation patterns
3. Consult QUICK_START.py for setup help
4. Study models_extended.py for schema details

---

## ✨ What's Included

✅ Complete relational database design  
✅ User authentication with password hashing  
✅ 14 cities with cost indices and coordinates  
✅ 100+ recommended activities with ratings  
✅ Packing checklist system with 50+ items  
✅ Trip sharing with public URLs and passwords  
✅ Helper classes for common operations  
✅ Comprehensive test suite  
✅ Complete documentation and examples  
✅ Data validation and integrity constraints  

---

## 🚀 Ready to Build!

Your travel database system is fully functional and ready for:
- Building a web application
- Creating a mobile app
- Developing a desktop tool
- Adding REST APIs
- Integrating with frontend frameworks

**Start with**: `python seed_data.py` & `python test_suite.py` 🌍

---

## 📝 Sample Data Included

**Sample User**: 
- Email: `sample@travelapp.com`
- Password: `demo123`

**Sample Trip**:
- Title: "Kerala Backwater Holiday"
- Duration: 10 days
- Includes packing checklist with 5+ items

---

**Happy Travel Planning! 🌍✈️🧳**
