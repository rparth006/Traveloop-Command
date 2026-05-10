"""
Travel Database - Quick Start Guide
Get started with the relational database in 5 minutes!
"""

QUICK_START = """
╔══════════════════════════════════════════════════════════════════════════════╗
║                    QUICK START - 5 MINUTE SETUP                             ║
╚══════════════════════════════════════════════════════════════════════════════╝

⚡ STEP 1: INSTALL DEPENDENCIES (1 minute)
═════════════════════════════════════════════════════════════════════════════

    pip install -r requirements.txt

    or manually:
    pip install sqlalchemy


⚡ STEP 2: INITIALIZE DATABASE (1 minute)
═════════════════════════════════════════════════════════════════════════════

    python models.py

    This creates:
    ✓ travel_database.db (SQLite database file)
    ✓ All 5 tables with relationships
    ✓ Indexes for performance


⚡ STEP 3: CREATE SAMPLE DATA (1 minute)
═════════════════════════════════════════════════════════════════════════════

    python examples.py

    This creates:
    ✓ 2 sample users
    ✓ 2 complete trips
    ✓ 3 stops per trip
    ✓ 4 activities per trip
    ✓ 4 expenses per trip


⚡ STEP 4: EXPLORE THE DATA (2 minutes)
═════════════════════════════════════════════════════════════════════════════

Open Python REPL:
    python

Then run:

    from models import create_database, get_session, User, Trip

    # Connect to database
    engine = create_database()
    session = get_session(engine)

    # Get all users
    users = session.query(User).all()
    for user in users:
        print(f"User: {user.name}, Email: {user.email}")
        print(f"  Trips: {len(user.trips)}")
        for trip in user.trips:
            print(f"    - {trip.title} to {trip.destination}")

    # Get trip details
    trip = session.query(Trip).first()
    print(f"\\nTrip: {trip.title}")
    print(f"Stops: {len(trip.stops)}")
    print(f"Activities: {len(trip.activities)}")
    print(f"Expenses: {len(trip.expenses)}")
    print(f"Total Cost: ₹{sum(e.amount for e in trip.expenses)}")

    exit()


═════════════════════════════════════════════════════════════════════════════


🎯 COMMON OPERATIONS
═════════════════════════════════════════════════════════════════════════════

from models import create_database, get_session, User, Trip, Stop, Activity, Expense
from datetime import date

engine = create_database()
session = get_session(engine)


1. CREATE A NEW USER
────────────────────

    user = User(
        name="Priya Sharma",
        email="priya@example.com",
        phone="9876543210"
    )
    session.add(user)
    session.commit()
    print(f"User created with ID: {user.id}")


2. CREATE A TRIP
────────────────

    trip = Trip(
        user_id=user.id,
        title="Goa Beach Vacation",
        destination="Goa",
        start_date=date(2026, 5, 1),
        end_date=date(2026, 5, 7),
        budget=50000.0
    )
    session.add(trip)
    session.commit()
    print(f"Trip created: {trip.title}")


3. ADD STOPS
────────────

    stop1 = Stop(
        trip_id=trip.id,
        location="Calangute Beach",
        arrival_date=date(2026, 5, 1),
        departure_date=date(2026, 5, 3),
        sequence_order=1
    )
    
    stop2 = Stop(
        trip_id=trip.id,
        location="Baga Beach",
        arrival_date=date(2026, 5, 3),
        departure_date=date(2026, 5, 7),
        sequence_order=2
    )
    
    session.add_all([stop1, stop2])
    session.commit()
    print(f"Added {len(trip.stops)} stops")


4. ADD ACTIVITIES
──────────────────

    from datetime import datetime
    
    activity = Activity(
        trip_id=trip.id,
        stop_id=stop1.id,
        name="Jet Skiing",
        activity_type="water_sports",
        cost=1500.0,
        start_time=datetime(2026, 5, 1, 10, 0),
        end_time=datetime(2026, 5, 1, 12, 0)
    )
    session.add(activity)
    session.commit()
    print(f"Activity added: {activity.name}")


5. ADD EXPENSES
────────────────

    expense = Expense(
        trip_id=trip.id,
        description="Hotel Booking",
        amount=15000.0,
        category="accommodation",
        expense_date=date(2026, 5, 1),
        payment_method="card",
        status="paid",
        paid_by="Priya Sharma"
    )
    session.add(expense)
    session.commit()
    print(f"Expense added: ₹{expense.amount}")


6. QUERY trip INFORMATION
────────────────────────

    # Get all stops (ordered)
    stops = sorted(trip.stops, key=lambda x: x.sequence_order or 0)
    print(f"Stops in order:")
    for stop in stops:
        print(f"  {stop.sequence_order}. {stop.location}")

    # Get all activities
    print(f"\\nActivities:")
    for activity in trip.activities:
        print(f"  - {activity.name}: ₹{activity.cost}")

    # Get all expenses
    print(f"\\nExpenses:")
    for expense in trip.expenses:
        print(f"  - {expense.description}: ₹{expense.amount}")
    
    # Total cost
    total = sum(e.amount for e in trip.expenses)
    print(f"\\nTotal: ₹{total}")
    print(f"Budget: ₹{trip.budget}")
    print(f"Remaining: ₹{trip.budget - total}")


7. UPDATE DATA
───────────────

    # Update trip budget
    trip.budget = 60000.0
    session.commit()

    # Update activity status
    activity.status = "completed"
    session.commit()

    # Update expense status
    expense.status = "reimbursed"
    session.commit()


8. DELETE DATA
───────────────

    # Delete an expense
    session.delete(expense)
    session.commit()

    # Delete an activity
    session.delete(activity)
    session.commit()

    # Delete a stop (activities will have stop_id set to NULL)
    session.delete(stop1)
    session.commit()

    # Delete entire trip (auto-deletes all stops, activities, expenses)
    session.delete(trip)
    session.commit()


═════════════════════════════════════════════════════════════════════════════


🎓 USING THE HELPER CLASS
═════════════════════════════════════════════════════════════════════════════

from database_operations import TravelDatabaseHelper
from datetime import date

# Initialize
db = TravelDatabaseHelper()

# Create user
user = db.create_user("Raj Patel", "raj@example.com", "9123456789")

# Create trip
trip = db.create_trip(
    user_id=user.id,
    title="Kerala Holiday",
    destination="Kerala",
    start_date=date(2026, 6, 1),
    end_date=date(2026, 6, 10)
)

# Create stop
stop = db.create_stop(
    trip_id=trip.id,
    location="Kochi",
    arrival_date=date(2026, 6, 1),
    sequence_order=1
)

# Create activity
activity = db.create_activity(
    trip_id=trip.id,
    stop_id=stop.id,
    name="Fort Kochi Visit",
    activity_type="sightseeing",
    cost=500.0
)

# Create expense
expense = db.create_expense(
    trip_id=trip.id,
    description="Flight booking",
    amount=8000.0,
    category="transport",
    expense_date=date(2026, 6, 1)
)

# Get analysis
analysis = db.get_trip_cost_analysis(trip.id)
print(f"Trip Budget: ₹{analysis['budget']}")
print(f"Total Spent: ₹{analysis['total_expenses']}")
print(f"Remaining: ₹{analysis['remaining']}")

# Get itinerary
itinerary = db.get_trip_itinerary(trip.id)
print(f"Trip: {itinerary['title']}")
for stop_data in itinerary['stops']:
    print(f"  - {stop_data['location']}")

# Get user stats
stats = db.get_user_stats(user.id)
print(f"User {stats['name']} has {stats['total_trips']} trips")

db.close()


═════════════════════════════════════════════════════════════════════════════


📊 VIEWING DATABASE SCHEMA
═════════════════════════════════════════════════════════════════════════════

    python schema_documentation.py

    This displays:
    ✓ Complete ER diagram
    ✓ All table structures
    ✓ Relationships explained
    ✓ SQL schema
    ✓ Query examples


═════════════════════════════════════════════════════════════════════════════


🔗 KEY RELATIONSHIPS
═════════════════════════════════════════════════════════════════════════════

USERS (1:N)──→ TRIPS (1:N)──┬──→ STOPS (1:N)──→ ACTIVITIES
                             │
                             ├──→ ACTIVITIES (linked to Stop or Trip)
                             │
                             └──→ EXPENSES


✓ 1 User can have many Trips
✓ 1 Trip can have many Stops
✓ 1 Trip can have many Activities
✓ 1 Trip can have many Expenses
✓ 1 Stop can have many Activities


═════════════════════════════════════════════════════════════════════════════


📁 PROJECT FILES EXPLAINED
═════════════════════════════════════════════════════════════════════════════

models.py
└─ SQLAlchemy models for all 5 tables
└─ Defines relationships between tables
└─ Contains database initialization function

examples.py
└─ Sample data creation
└─ Usage examples
└─ Query demonstrations

database_operations.py
└─ TravelDatabaseHelper class
└─ Helper functions for CRUD operations
└─ Analytics and reporting functions

schema_documentation.py
└─ Database schema documentation
└─ ER diagrams
└─ SQL structure
└─ Query examples

SETUP_GUIDE.py
└─ Comprehensive setup documentation
└─ Best practices
└─ Troubleshooting guide

README.md
└─ Project overview
└─ Feature list
└─ Quick reference

requirements.txt
└─ Python package dependencies


═════════════════════════════════════════════════════════════════════════════


🚨 IMPORTANT NOTES
═════════════════════════════════════════════════════════════════════════════

CASCADE DELETE:
  • Deleting a User deletes all their Trips
  • Deleting a Trip deletes all Stops, Activities, Expenses
  • Deleting a Stop sets stop_id to NULL in Activities

CONSTRAINTS:
  • User email must be UNIQUE
  • Foreign keys prevent orphaned records
  • Dates are validated (trip end > start)

INDEXING:
  • email (UNIQUE) on users
  • user_id on trips
  • trip_id on stops, activities, expenses
  • category, status on expenses

═════════════════════════════════════════════════════════════════════════════


💡 TIPS
═════════════════════════════════════════════════════════════════════════════

1. Always commit after changes:
   session.add(record)
   session.commit()

2. Use helper class for common operations:
   from database_operations import TravelDatabaseHelper

3. Sort stops by sequence_order:
   sorted(trip.stops, key=lambda x: x.sequence_order or 0)

4. Close session when done:
   session.close()
   db.close()  # if using helper

5. Use filters for efficient queries:
   session.query(Trip).filter_by(destination="Paris").all()

═════════════════════════════════════════════════════════════════════════════


🐛 COMMON ISSUES & SOLUTIONS
═════════════════════════════════════════════════════════════════════════════

ERROR: IntegrityError: UNIQUE constraint failed: users.email
SOLUTION: Use unique email for each user

ERROR: ForeignKeyConstraintError
SOLUTION: Ensure parent record exists before creating child

ERROR: Session already closed
SOLUTION: Create new session or use context manager

ERROR: Activity has no stop_id
SOLUTION: stop_id is optional, use trip_id only if not linked to stop

═════════════════════════════════════════════════════════════════════════════

Ready to start? Run: python examples.py 🚀

═════════════════════════════════════════════════════════════════════════════
"""

if __name__ == '__main__':
    print(QUICK_START)
