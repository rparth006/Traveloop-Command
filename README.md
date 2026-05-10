# 🌍 Travel Database - Relational Database Design

A comprehensive relational database system for managing complex travel data with proper relationships between Users, Trips, Stops, Activities, and Expenses.

---

## 📋 Project Overview

This project implements a complete relational database design for a travel management system using:
- **SQLAlchemy ORM** for Python
- **SQLite** for local development (works with PostgreSQL, MySQL, etc.)
- **Proper relationships** between all entities

---

## 📚 Database Tables

### 1. **USERS** 👤
Stores user/traveler information
- Primary Key: `id`
- Unique: `email`
- Relationships: 1 user → many trips

### 2. **TRIPS** ✈️
Stores trip information
- Primary Key: `id`
- Foreign Key: `user_id` → users
- Relationships: 1 trip → many stops, activities, expenses

### 3. **STOPS** 📍
Specific locations/destinations within a trip
- Primary Key: `id`
- Foreign Key: `trip_id` → trips
- Fields: location, coordinates (lat/long), arrival/departure dates
- Relationships: 1 stop → many activities

### 4. **ACTIVITIES** 🎯
Activities/events during a trip
- Primary Key: `id`
- Foreign Keys: `trip_id` → trips, `stop_id` → stops (optional)
- Fields: name, type, time, cost, status
- Types: sightseeing, hiking, dining, relaxation, etc.

### 5. **EXPENSES** 💰
Expense tracking for trips
- Primary Key: `id`
- Foreign Key: `trip_id` → trips
- Fields: description, amount, category, payment method, status
- Categories: accommodation, food, transport, activities, etc.

---

## 🔗 Relationships

```
USERS (1:N)──→ TRIPS (1:N)──┬──→ STOPS (1:N)──→ ACTIVITIES
                             │                   (linked to stop)
                             │
                             ├──→ ACTIVITIES
                             │    (trip-level)
                             │
                             └──→ EXPENSES
```

### Key Relationships:
| From | To | Type | Behavior |
|------|----|----|-----------|
| Users | Trips | 1:Many | Cascade delete |
| Trips | Stops | 1:Many | Cascade delete |
| Trips | Activities | 1:Many | Cascade delete |
| Stops | Activities | 1:Many | Set NULL on delete |
| Trips | Expenses | 1:Many | Cascade delete |

---

## 🚀 Getting Started

### Prerequisites
```bash
pip install sqlalchemy
```

### Installation

1. **Initialize Database**
```python
python models.py
```

2. **Create Sample Data**
```python
python examples.py
```

3. **View Schema Documentation**
```python
python schema_documentation.py
```

---

## 📁 Project Files

| File | Purpose |
|------|---------|
| `models.py` | SQLAlchemy ORM models for all tables |
| `examples.py` | Sample data creation and usage examples |
| `schema_documentation.py` | SQL schema and ER diagrams |
| `SETUP_GUIDE.py` | Complete setup and operation guide |
| `database_operations.py` | CRUD helper functions |
| `README.md` | This file |

---

## 💻 Quick Usage Examples

### Create a User
```python
from models import User, create_database, get_session

engine = create_database()
session = get_session(engine)

user = User(name="John Doe", email="john@example.com")
session.add(user)
session.commit()
```

### Create a Trip with Stops and Activities
```python
from models import Trip, Stop, Activity
from datetime import date

trip = Trip(
    user_id=user.id,
    title="Paris Vacation",
    destination="Paris",
    start_date=date(2026, 6, 1),
    end_date=date(2026, 6, 15)
)
session.add(trip)
session.commit()

stop = Stop(
    trip_id=trip.id,
    location="Eiffel Tower",
    sequence_order=1,
    arrival_date=date(2026, 6, 1)
)
session.add(stop)
session.commit()

activity = Activity(
    trip_id=trip.id,
    stop_id=stop.id,
    name="Visit Eiffel Tower",
    activity_type="sightseeing",
    cost=25.0
)
session.add(activity)
session.commit()
```

### Query Trip Information
```python
# Get user's trips
trips = user.trips

# Get trip stops (ordered)
stops = sorted(trip.stops, key=lambda x: x.sequence_order or 0)

# Get activities at a stop
activities = stop.activities

# Calculate total trip expenses
total_cost = sum(expense.amount for expense in trip.expenses)
```

---

## 📊 Database Relationships - Visual Reference

### One-to-Many: User → Trips
```
┌─────────┐
│ USER    │
│ id=1    │
└────┬────┘
     │ (1 user has many trips)
     │
     ├──→ Trip 1 (Paris)
     ├──→ Trip 2 (Tokyo)
     └──→ Trip 3 (New York)
```

### One-to-Many: Trip → Stops → Activities
```
┌─────────────┐
│ TRIP (Paris)│
└──────┬──────┘
       │
       ├─→ Stop 1: Eiffel Tower
       │   ├─→ Activity: Visit tower
       │   └─→ Activity: Dinner nearby
       │
       ├─→ Stop 2: Louvre Museum
       │   ├─→ Activity: Museum tour
       │   └─→ Activity: Lunch
       │
       └─→ Stop 3: Notre-Dame
           └─→ Activity: Photography
```

### One-to-Many: Trip → Expenses
```
┌──────────────────┐
│ TRIP (Budget: ₹150K)
└────────┬─────────┘
         │
         ├─→ Expense: Flight (₹50K) [transport]
         ├─→ Expense: Hotel (₹60K) [accommodation]
         ├─→ Expense: Food (₹15K) [food]
         └─→ Expense: Activities (₹20K) [activities]
         
         Total: ₹145K
```

---

## 🔄 Data Flow Example

### Creating a Complete Trip:
1. **Create User** → Stores traveler information
2. **Create Trip** → Linked to User
3. **Add Stops** → Locations/destinations in the trip
4. **Add Activities** → Events at each stop
5. **Track Expenses** → Costs associated with the trip
6. **Query & Analyze** → Generate reports, balance budgets

---

## 📈 Advanced Queries

### Get trip budget analysis
```python
total_expenses = sum(e.amount for e in trip.expenses)
remaining = trip.budget - total_expenses
percentage = (total_expenses / trip.budget) * 100
```

### Group expenses by category
```python
by_category = {}
for expense in trip.expenses:
    if expense.category not in by_category:
        by_category[expense.category] = 0
    by_category[expense.category] += expense.amount
```

### Find trips within budget
```python
affordable = [t for t in user.trips 
              if sum(e.amount for e in t.expenses) <= max_budget]
```

---

## 🔐 Referential Integrity

- **Cascade Delete**: Deleting a Trip cascades to Stops, Activities, and Expenses
- **Set Null**: Deleting a Stop sets `stop_id` to NULL in Activities (preserves data)
- **Foreign Key Constraints**: All relationships enforced at database level

---

## 🗄️ Database Indices

Optimized queries with indices on:
- `users.email` (UNIQUE)
- `trips.user_id`
- `stops.trip_id`
- `activities.trip_id`, `stop_id`
- `expenses.trip_id`, `category`, `expense_date`, `status`

---

## 📝 Supported Database Backends

- **SQLite** (default): `sqlite:///travel_database.db`
- **PostgreSQL**: `postgresql://user:password@localhost/travel_db`
- **MySQL**: `mysql+pymysql://user:password@localhost/travel_db`

---

## ✨ Features

✅ Complete relational database design  
✅ SQLAlchemy ORM models with relationships  
✅ Cascade delete for data integrity  
✅ Timestamps on all records  
✅ Flexible activity assignment (trip-level or stop-level)  
✅ Expense tracking by category  
✅ Support for multiple database backends  
✅ Sample data and usage examples  
✅ Comprehensive documentation  

---

## 🤝 Contributing

Feel free to extend the models with:
- Reviews/ratings for activities
- Shared trips (multiple users per trip)
- Payment splitting between travelers
- Photos/media attachments
- Notifications/reminders

---

## 📄 License

Open source - Feel free to use and modify

---

## 📞 Support

For questions or issues:
1. Check `SETUP_GUIDE.py` for detailed documentation
2. Review `examples.py` for usage patterns
3. See `schema_documentation.py` for database structure

---

## 🎯 Summary

This relational database design provides:
- **Clean separation** of concerns (Users, Trips, Stops, Activities, Expenses)
- **Proper relationships** between all entities
- **Data integrity** through foreign keys and cascade rules
- **Flexibility** to handle complex travel scenarios
- **Scalability** with indexed queries and transaction support

Perfect for building a complete travel management system! 🌍✈️
