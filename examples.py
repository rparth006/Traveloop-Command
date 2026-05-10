"""
Travel Database - Usage Examples and Sample Data
Demonstrates how to use the relational database models
"""

from models import (
    create_database, get_session, User, Trip, Stop, Activity, Expense
)
from datetime import datetime, date, timedelta

def create_sample_data():
    """Create and insert sample travel data with relationships"""
    
    # Initialize database
    engine = create_database()
    session = get_session(engine)
    
    # Clear existing data (optional)
    session.query(User).delete()
    session.query(Trip).delete()
    session.query(Stop).delete()
    session.query(Activity).delete()
    session.query(Expense).delete()
    
    print("=" * 60)
    print("CREATING SAMPLE TRAVEL DATA")
    print("=" * 60)
    
    # 1. Create Users
    print("\n[1] Creating Users...")
    user1 = User(
        name="Raj Patel",
        email="raj@example.com",
        phone="9876543210",
        address="Ahmedabad, Gujarat"
    )
    
    user2 = User(
        name="Priya Sharma",
        email="priya@example.com",
        phone="9123456789",
        address="Mumbai, Maharashtra"
    )
    
    session.add_all([user1, user2])
    session.commit()
    print(f"  ✓ Created {user1.name}")
    print(f"  ✓ Created {user2.name}")
    
    # 2. Create Trips
    print("\n[2] Creating Trips...")
    trip1 = Trip(
        user_id=user1.id,
        title="Kerala Beach Vacation",
        description="A relaxing trip to Kerala beaches",
        start_date=date(2026, 6, 1),
        end_date=date(2026, 6, 10),
        destination="Kerala",
        budget=50000.0
    )
    
    trip2 = Trip(
        user_id=user2.id,
        title="Amsterdam Adventure",
        description="Exploring the canals and cities of Netherlands",
        start_date=date(2026, 7, 15),
        end_date=date(2026, 7, 30),
        destination="Amsterdam, Netherlands",
        budget=150000.0
    )
    
    session.add_all([trip1, trip2])
    session.commit()
    print(f"  ✓ Created Trip: {trip1.title}")
    print(f"  ✓ Created Trip: {trip2.title}")
    
    # 3. Create Stops (One Trip → Multiple Stops)
    print("\n[3] Creating Stops for Trip 1 (Kerala)...")
    stop1 = Stop(
        trip_id=trip1.id,
        location="Kochi",
        latitude=9.9312,
        longitude=76.2673,
        arrival_date=date(2026, 6, 1),
        departure_date=date(2026, 6, 3),
        notes="Start at Kochi Fort",
        sequence_order=1
    )
    
    stop2 = Stop(
        trip_id=trip1.id,
        location="Alleppey",
        latitude=9.4981,
        longitude=76.3388,
        arrival_date=date(2026, 6, 3),
        departure_date=date(2026, 6, 6),
        notes="Houseboat experience",
        sequence_order=2
    )
    
    stop3 = Stop(
        trip_id=trip1.id,
        location="Munnar",
        latitude=10.5869,
        longitude=77.0564,
        arrival_date=date(2026, 6, 6),
        departure_date=date(2026, 6, 10),
        notes="Tea plantations and mountain views",
        sequence_order=3
    )
    
    session.add_all([stop1, stop2, stop3])
    session.commit()
    print(f"  ✓ Stop 1: {stop1.location}")
    print(f"  ✓ Stop 2: {stop2.location}")
    print(f"  ✓ Stop 3: {stop3.location}")
    
    # 4. Create Activities (One Trip → Multiple Activities)
    print("\n[4] Creating Activities...")
    activity1 = Activity(
        trip_id=trip1.id,
        stop_id=stop1.id,
        name="Visit Kochi Fort",
        description="Explore the historic Fort Kochi",
        activity_type="sightseeing",
        start_time=datetime(2026, 6, 1, 10, 0),
        end_time=datetime(2026, 6, 1, 14, 0),
        cost=500.0,
        status="planned"
    )
    
    activity2 = Activity(
        trip_id=trip1.id,
        stop_id=stop2.id,
        name="Houseboat Cruise",
        description="Backwater houseboat experience",
        activity_type="relaxation",
        start_time=datetime(2026, 6, 4, 8, 0),
        end_time=datetime(2026, 6, 4, 18, 0),
        cost=5000.0,
        status="planned"
    )
    
    activity3 = Activity(
        trip_id=trip1.id,
        stop_id=stop3.id,
        name="Tea Plantation Trek",
        description="Trek through tea gardens",
        activity_type="hiking",
        start_time=datetime(2026, 6, 7, 6, 0),
        end_time=datetime(2026, 6, 7, 12, 0),
        cost=1500.0,
        status="planned"
    )
    
    activity4 = Activity(
        trip_id=trip1.id,
        stop_id=stop2.id,
        name="Local Cuisine Tasting",
        description="Traditional Kerala food",
        activity_type="dining",
        start_time=datetime(2026, 6, 5, 19, 0),
        end_time=datetime(2026, 6, 5, 21, 0),
        cost=800.0,
        status="planned"
    )
    
    session.add_all([activity1, activity2, activity3, activity4])
    session.commit()
    print(f"  ✓ Activity 1: {activity1.name}")
    print(f"  ✓ Activity 2: {activity2.name}")
    print(f"  ✓ Activity 3: {activity3.name}")
    print(f"  ✓ Activity 4: {activity4.name}")
    
    # 5. Create Expenses (One Trip → Multiple Expenses)
    print("\n[5] Creating Expenses...")
    expense1 = Expense(
        trip_id=trip1.id,
        description="Flight to Kochi",
        amount=8000.0,
        category="transport",
        expense_date=date(2026, 6, 1),
        payment_method="card",
        status="paid",
        paid_by="Raj Patel"
    )
    
    expense2 = Expense(
        trip_id=trip1.id,
        description="Hotel in Kochi - 2 nights",
        amount=6000.0,
        category="accommodation",
        expense_date=date(2026, 6, 1),
        payment_method="online",
        status="paid",
        paid_by="Raj Patel"
    )
    
    expense3 = Expense(
        trip_id=trip1.id,
        description="Houseboat booking",
        amount=12000.0,
        category="accommodation",
        expense_date=date(2026, 6, 3),
        payment_method="card",
        status="paid",
        paid_by="Raj Patel"
    )
    
    expense4 = Expense(
        trip_id=trip1.id,
        description="Meals and snacks",
        amount=3500.0,
        category="food",
        expense_date=date(2026, 6, 5),
        payment_method="cash",
        status="paid",
        paid_by="Raj Patel"
    )
    
    session.add_all([expense1, expense2, expense3, expense4])
    session.commit()
    print(f"  ✓ Expense 1: {expense1.description} - ₹{expense1.amount}")
    print(f"  ✓ Expense 2: {expense2.description} - ₹{expense2.amount}")
    print(f"  ✓ Expense 3: {expense3.description} - ₹{expense3.amount}")
    print(f"  ✓ Expense 4: {expense4.description} - ₹{expense4.amount}")
    
    print("\n" + "=" * 60)
    print("SAMPLE DATA CREATION COMPLETE")
    print("=" * 60)
    
    return session, user1, trip1


def display_trip_details(session, trip):
    """Display complete trip information with all relationships"""
    
    print("\n" + "=" * 60)
    print(f"TRIP DETAILS: {trip.title}")
    print("=" * 60)
    
    print(f"\nTrip Info:")
    print(f"  ID: {trip.id}")
    print(f"  User: {trip.user.name}")
    print(f"  Destination: {trip.destination}")
    print(f"  Duration: {trip.start_date} to {trip.end_date}")
    print(f"  Budget: ₹{trip.budget}")
    
    print(f"\nStops ({len(trip.stops)}):")
    for stop in trip.stops:
        print(f"  - {stop.sequence_order}. {stop.location} ({stop.arrival_date} to {stop.departure_date})")
    
    print(f"\nActivities ({len(trip.activities)}):")
    for activity in trip.activities:
        stop_name = activity.stop.location if activity.stop else "Not assigned"
        print(f"  - {activity.name} ({activity.activity_type}) at {stop_name}")
        print(f"    Cost: ₹{activity.cost}, Status: {activity.status}")
    
    print(f"\nExpenses ({len(trip.expenses)}):")
    total_expense = 0
    for expense in trip.expenses:
        print(f"  - {expense.description}: ₹{expense.amount} ({expense.category})")
        total_expense += expense.amount
    print(f"  Total Expenses: ₹{total_expense}")
    print(f"  Budget vs Spent: ₹{trip.budget - total_expense}")
    
    print("\n" + "=" * 60)


def query_examples(session):
    """Examples of common queries"""
    
    print("\n" + "=" * 60)
    print("QUERY EXAMPLES")
    print("=" * 60)
    
    # Query 1: Get all trips for a user
    print("\n[Query 1] Get all trips for a user:")
    user = session.query(User).first()
    trips = user.trips
    print(f"  User '{user.name}' has {len(trips)} trip(s)")
    for trip in trips:
        print(f"    - {trip.title}")
    
    # Query 2: Get all stops for a trip
    print("\n[Query 2] Get all stops for a trip (ordered by sequence):")
    trip = session.query(Trip).first()
    stops = sorted(trip.stops, key=lambda x: x.sequence_order or 0)
    print(f"  Trip '{trip.title}' has {len(stops)} stop(s):")
    for stop in stops:
        print(f"    - {stop.location}")
    
    # Query 3: Get activities by type
    print("\n[Query 3] Get activities by type:")
    activities = session.query(Activity).filter_by(trip_id=trip.id)
    activity_types = {}
    for activity in activities:
        activity_types.setdefault(activity.activity_type, []).append(activity.name)
    for activity_type, names in activity_types.items():
        print(f"  {activity_type.upper()}: {', '.join(names)}")
    
    # Query 4: Get expenses by category
    print("\n[Query 4] Get trip expenses breakdown by category:")
    expenses = trip.expenses
    expense_categories = {}
    for expense in expenses:
        expense_categories.setdefault(expense.category, 0)
        expense_categories[expense.category] += expense.amount
    for category, amount in expense_categories.items():
        print(f"  {category}: ₹{amount}")
    
    # Query 5: Total trip cost
    print("\n[Query 5] Total trip cost calculation:")
    total_cost = sum(expense.amount for expense in expenses)
    print(f"  Total Cost: ₹{total_cost}")
    print(f"  Budget: ₹{trip.budget}")
    print(f"  Remaining: ₹{trip.budget - total_cost}")


if __name__ == '__main__':
    # Create sample data
    session, user, trip = create_sample_data()
    
    # Display trip details
    display_trip_details(session, trip)
    
    # Show query examples
    query_examples(session)
    
    print("\n✓ All examples completed!")
