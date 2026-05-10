"""
Travel Database System - Complete Setup & Usage Guide
"""

SETUP_GUIDE = """
╔══════════════════════════════════════════════════════════════════════════════╗
║                 TRAVEL DATABASE - COMPLETE SETUP GUIDE                       ║
╚══════════════════════════════════════════════════════════════════════════════╝

📋 PROJECT STRUCTURE
════════════════════════════════════════════════════════════════════════════════

odoo project/
├── models.py                      # SQLAlchemy ORM Models
├── examples.py                    # Sample data & usage examples
├── schema_documentation.py        # SQL schema & relationships
├── database_operations.py         # CRUD operations helper
├── travel_database.db             # SQLite database (auto-created)
└── requirements.txt               # Python dependencies

════════════════════════════════════════════════════════════════════════════════


🚀 INSTALLATION & SETUP
════════════════════════════════════════════════════════════════════════════════

Step 1: Install Required Packages
──────────────────────────────────

    pip install sqlalchemy

    For specific databases (optional):
    - PostgreSQL: pip install psycopg2
    - MySQL: pip install pymysql
    - SQLite: (built-in, no installation needed)


Step 2: Initialize Database
──────────────────────────────────

Option A - Using SQLite (Recommended for development):
    python models.py

    This creates: travel_database.db

Option B - Using PostgreSQL:
    # Update connection string in models.py:
    engine = create_database('postgresql://user:password@localhost/travel_db')

Option C - Using MySQL:
    # Update connection string in models.py:
    engine = create_database('mysql+pymysql://user:password@localhost/travel_db')


Step 3: Create Sample Data
──────────────────────────────────

    python examples.py

    This creates:
    - 2 sample users
    - 2 sample trips
    - 3 stops per trip
    - 4 activities per trip
    - 4 expenses per trip


════════════════════════════════════════════════════════════════════════════════


📊 DATABASE TABLES OVERVIEW
════════════════════════════════════════════════════════════════════════════════

Table: USERS
────────────────────
Description: Stores user/traveler information
Columns: id, name, email, phone, address, created_at, updated_at
Primary Key: id
Indexes: email (UNIQUE)
Relationships: 1 user → many trips


Table: TRIPS
────────────────────
Description: Stores trip information
Columns: id, user_id, title, description, start_date, end_date, destination, 
         budget, created_at, updated_at
Primary Key: id
Foreign Key: user_id → users(id) [ON DELETE CASCADE]
Relationships: 1 trip → many stops, activities, expenses


Table: STOPS
────────────────────
Description: Stores specific locations/destinations within a trip
Columns: id, trip_id, location, latitude, longitude, arrival_date, 
         departure_date, notes, sequence_order, created_at, updated_at
Primary Key: id
Foreign Key: trip_id → trips(id) [ON DELETE CASCADE]
Relationships: 1 stop → many activities


Table: ACTIVITIES
────────────────────
Description: Stores activities/events during a trip
Columns: id, trip_id, stop_id, name, description, activity_type, start_time,
         end_time, cost, status, created_at, updated_at
Primary Key: id
Foreign Keys: 
  - trip_id → trips(id) [ON DELETE CASCADE]
  - stop_id → stops(id) [ON DELETE SET NULL] (optional)


Table: EXPENSES
────────────────────
Description: Stores expense tracking for trips
Columns: id, trip_id, description, amount, category, expense_date, 
         payment_method, status, paid_by, notes, created_at, updated_at
Primary Key: id
Foreign Key: trip_id → trips(id) [ON DELETE CASCADE]
Indexes: category, expense_date, status


════════════════════════════════════════════════════════════════════════════════


💻 BASIC OPERATIONS
════════════════════════════════════════════════════════════════════════════════

Creating Records:
─────────────────

from models import User, Trip, Stop, Activity, Expense, create_database, get_session
from datetime import date

# Initialize DB
engine = create_database()
session = get_session(engine)

# Create a user
user = User(name="John Doe", email="john@example.com", phone="1234567890")
session.add(user)
session.commit()

# Create a trip for the user
trip = Trip(
    user_id=user.id,
    title="Summer Vacation",
    destination="Paris",
    start_date=date(2026, 6, 1),
    end_date=date(2026, 6, 15),
    budget=100000.0
)
session.add(trip)
session.commit()

# Create a stop (location in trip)
stop = Stop(
    trip_id=trip.id,
    location="Eiffel Tower",
    arrival_date=date(2026, 6, 1),
    departure_date=date(2026, 6, 5),
    sequence_order=1
)
session.add(stop)
session.commit()

# Create an activity
activity = Activity(
    trip_id=trip.id,
    stop_id=stop.id,
    name="Visit Eiffel Tower",
    activity_type="sightseeing",
    cost=25.0
)
session.add(activity)
session.commit()

# Create an expense
expense = Expense(
    trip_id=trip.id,
    description="Hotel accommodation",
    amount=5000.0,
    category="accommodation",
    expense_date=date(2026, 6, 1),
    payment_method="card",
    status="paid",
    paid_by="John Doe"
)
session.add(expense)
session.commit()


Reading Records:
────────────────

# Get all users
all_users = session.query(User).all()

# Get specific user by ID
user = session.query(User).filter_by(id=1).first()

# Get user's trips
user_trips = user.trips

# Get all stops for a trip (sorted by sequence)
stops = sorted(trip.stops, key=lambda x: x.sequence_order or 0)

# Get activities by type
sightseeing = session.query(Activity).filter_by(activity_type='sightseeing').all()

# Get expenses by category
accommodations = session.query(Expense).filter_by(category='accommodation').all()

# Get total trip expenses
total = sum(e.amount for e in trip.expenses)


Updating Records:
─────────────────

# Update user information
user.phone = "9876543210"
session.commit()

# Update trip budget
trip.budget = 120000.0
session.commit()

# Update activity status
activity.status = "completed"
session.commit()

# Update expense status
expense.status = "reimbursed"
session.commit()


Deleting Records:
─────────────────

# Delete an expense (trip and stops remain)
session.delete(expense)
session.commit()

# Delete an activity (trip and stop remain)
session.delete(activity)
session.commit()

# Delete a stop (activities linked to it have stop_id set to NULL)
session.delete(stop)
session.commit()

# Delete a trip (all stops, activities, expenses are deleted via CASCADE)
session.delete(trip)
session.commit()

# Delete a user (all trips, stops, activities, expenses are deleted)
session.delete(user)
session.commit()


════════════════════════════════════════════════════════════════════════════════


📈 ADVANCED QUERIES
════════════════════════════════════════════════════════════════════════════════

Total trip cost and budget analysis:
─────────────────────────────────────

def get_trip_budget_analysis(session, trip_id):
    trip = session.query(Trip).filter_by(id=trip_id).first()
    total_expenses = sum(e.amount for e in trip.expenses)
    remaining = trip.budget - total_expenses
    
    print(f"Trip: {trip.title}")
    print(f"Budget: ₹{trip.budget}")
    print(f"Spent: ₹{total_expenses}")
    print(f"Remaining: ₹{remaining}")
    print(f"Percentage Used: {(total_expenses/trip.budget)*100:.2f}%")


Expenses grouped by category:
──────────────────────────────

def get_expenses_by_category(session, trip_id):
    expenses = session.query(Expense).filter_by(trip_id=trip_id).all()
    by_category = {}
    
    for expense in expenses:
        if expense.category not in by_category:
            by_category[expense.category] = 0
        by_category[expense.category] += expense.amount
    
    return by_category


Activities at a specific stop:
───────────────────────────────

def get_stop_activities(session, stop_id):
    stop = session.query(Stop).filter_by(id=stop_id).first()
    activities = session.query(Activity).filter_by(stop_id=stop_id).all()
    
    return {
        'stop': stop.location,
        'arrival': stop.arrival_date,
        'departure': stop.departure_date,
        'activities': len(activities),
        'schedule': activities
    }


Find trips within budget:
─────────────────────────

def get_trips_within_budget(session, user_id, max_budget):
    user = session.query(User).filter_by(id=user_id).first()
    affordable_trips = []
    
    for trip in user.trips:
        total_expenses = sum(e.amount for e in trip.expenses)
        if total_expenses <= max_budget:
            affordable_trips.append(trip)
    
    return affordable_trips


════════════════════════════════════════════════════════════════════════════════


🔐 DATABASE BEST PRACTICES
════════════════════════════════════════════════════════════════════════════════

1. Connection Management:
   ├─ Always close sessions after use
   ├─ Use context managers for automatic cleanup
   └─ Keep connections pooled for performance


2. Data Validation:
   ├─ Validate dates (end_date > start_date)
   ├─ Validate amounts (should be positive)
   ├─ Check required fields before insertion
   └─ Use proper email format validation


3. Performance Optimization:
   ├─ Use indexes on frequently queried fields
   ├─ Avoid N+1 query problems
   ├─ Use eager loading when needed
   └─ Paginate large result sets


4. Error Handling:
   ├─ Use try-except blocks for database operations
   ├─ Implement transaction rollback on errors
   ├─ Log all database operations
   └─ Handle foreign key constraint violations


5. Data Integrity:
   ├─ Use CASCADE delete for related records
   ├─ Maintain referential integrity
   ├─ Use transactions for atomic operations
   └─ Regular database backups


════════════════════════════════════════════════════════════════════════════════


🔄 RELATIONSHIP FLOWS
════════════════════════════════════════════════════════════════════════════════

Creating a Complete Trip:
──────────────────────────

1. Create User
   └─ 2. Create Trip (linked to User)
      ├─ 3a. Create Stops (linked to Trip)
      │  └─ 3b. Create Activities (linked to Stop & Trip)
      │
      ├─ 3c. Create Activities (linked to Trip only)
      │
      └─ 3d. Create Expenses (linked to Trip)


Accessing Trip Data Hierarchy:
─────────────────────────────

user = session.query(User).first()
  ↓
for trip in user.trips:
  ├─ print(trip.title)  # Trip basic info
  │
  ├─ for stop in trip.stops:  # All stops in trip
  │  ├─ print(stop.location)  # Stop info
  │  │
  │  └─ for activity in stop.activities:  # Activities at this stop
  │     └─ print(activity.name)  # Activity info
  │
  ├─ for activity in trip.activities:  # All activities in trip
  │  └─ if activity.stop:
  │     └─ print(activity.stop.location)  # Stop of activity
  │
  └─ for expense in trip.expenses:  # All expenses in trip
     └─ print(expense.description)  # Expense info


════════════════════════════════════════════════════════════════════════════════


📝 EXAMPLE: COMPLETE TRIP WORKFLOW
════════════════════════════════════════════════════════════════════════════════

# 1. User plans a trip
user = User(name="Priya", email="priya@example.com")
session.add(user)
session.commit()

# 2. Create trip
trip = Trip(user_id=user.id, title="Kerala Holiday", destination="Kerala",
           start_date=date(2026, 6, 1), end_date=date(2026, 6, 10))
session.add(trip)
session.commit()

# 3. Add stops
kochi = Stop(trip_id=trip.id, location="Kochi", sequence_order=1,
            arrival_date=date(2026, 6, 1), departure_date=date(2026, 6, 3))
alleppey = Stop(trip_id=trip.id, location="Alleppey", sequence_order=2,
               arrival_date=date(2026, 6, 3), departure_date=date(2026, 6, 6))
session.add_all([kochi, alleppey])
session.commit()

# 4. Add activities
activity1 = Activity(trip_id=trip.id, stop_id=kochi.id, name="Fort Kochi visit",
                    activity_type="sightseeing", cost=500)
activity2 = Activity(trip_id=trip.id, stop_id=alleppey.id, name="Houseboat cruise",
                    activity_type="relaxation", cost=5000)
session.add_all([activity1, activity2])
session.commit()

# 5. Add expenses
expense1 = Expense(trip_id=trip.id, description="Flight tickets",
                  amount=8000, category="transport", expense_date=date(2026, 6, 1))
expense2 = Expense(trip_id=trip.id, description="Hotel in Kochi",
                  amount=6000, category="accommodation", expense_date=date(2026, 6, 1))
session.add_all([expense1, expense2])
session.commit()

# 6. Query and display
total_cost = sum(e.amount for e in trip.expenses)
print(f"Trip Total Cost: ₹{total_cost}")

════════════════════════════════════════════════════════════════════════════════


🆘 TROUBLESHOOTING
════════════════════════════════════════════════════════════════════════════════

Issue: Foreign Key Constraint Error
Solution: Ensure parent record exists before creating child record

Issue: Duplicate Email Error
Solution: Use unique emails for users

Issue: Session Already Closed
Solution: Create new session or use context manager

Issue: N+1 Query Problem
Solution: Use eager loading or join queries

Issue: Cascade Delete Not Working
Solution: Ensure ON DELETE CASCADE is set in foreign keys

════════════════════════════════════════════════════════════════════════════════
"""

if __name__ == '__main__':
    print(SETUP_GUIDE)
