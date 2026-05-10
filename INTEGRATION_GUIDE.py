"""
Travel Database - Complete Integration Guide
Comprehensive guide for using all database features with examples
"""

INTEGRATION_GUIDE = """
╔══════════════════════════════════════════════════════════════════════════════╗
║           TRAVEL DATABASE - COMPLETE INTEGRATION GUIDE                       ║
║         Data Gathering, Authentication, Sharing & Packing Features          ║
╚══════════════════════════════════════════════════════════════════════════════╝

📋 TABLE OF CONTENTS
════════════════════════════════════════════════════════════════════════════════
1. Setup & Initialization
2. User Authentication (Login/Signup)
3. City & Activity Data Management
4. Trip Sharing with Public URLs
5. Packing Checklist System
6. Backend Data Retrieval
7. Complete Workflow Examples


════════════════════════════════════════════════════════════════════════════════
⚙️ SETUP & INITIALIZATION
════════════════════════════════════════════════════════════════════════════════

STEP 1: Install Dependencies
──────────────────────────────
    pip install sqlalchemy

STEP 2: Initialize Database with Extended Models
──────────────────────────────────────────────────
    python models_extended.py
    
    ✓ Creates all tables including:
      - Core tables: Users, Trips, Stops, Activities, Expenses
      - New tables: Cities, ActivityTypes, CityActivities
      - Packing tables: PackingItems, PackingChecklists
      - Sharing table: SharedTrips

STEP 3: Seed Reference Data
────────────────────────────
    python seed_data.py
    
    ✓ Populates:
      - 14 popular cities with cost indices
      - 8 activity types with cost ranges
      - 50+ activities per city with ratings
      - 50+ default packing items by category
      - 1 sample user with trip & packing list
    
    Database now has: 14 cities, 100+ activities, ready for use


════════════════════════════════════════════════════════════════════════════════
🔐 USER AUTHENTICATION (LOGIN / SIGNUP)
════════════════════════════════════════════════════════════════════════════════

import from auth_and_sharing import AuthenticationManager

auth = AuthenticationManager()


---USER SIGNUP---

result = auth.signup(
    name="Priya Sharma",
    email="priya@example.com",
    password="secure_password123",
    phone="+91-9876543210",
    address="Ahmedabad, Gujarat"
)

if result['success']:
    user = result['user']
    print(f"Welcome {user.name}!")
    print(f"User ID: {user.id}")
    print(f"Email: {user.email}")
else:
    print(f"Error: {result['message']}")
    # Possible errors:
    # - Invalid email format
    # - Email already registered
    # - Password too short (< 6 chars)


---USER LOGIN---

result = auth.login(
    email="priya@example.com",
    password="secure_password123"
)

if result['success']:
    user = result['user']
    user_id = user.id
    print(f"Logged in as {user.name}")
else:
    print(f"Login failed: {result['message']}")
    # Possible errors:
    # - User not found
    # - Invalid password


---CHANGE PASSWORD---

result = auth.change_password(
    user_id=user.id,
    old_password="secure_password123",
    new_password="new_password456"
)

if result['success']:
    print("Password changed successfully")
else:
    print(f"Error: {result['message']}")


════════════════════════════════════════════════════════════════════════════════
🌍 CITY & ACTIVITY DATA MANAGEMENT
════════════════════════════════════════════════════════════════════════════════

from auth_and_sharing import DataRetrievalManager
from models_extended import get_session, create_database

data_mgr = DataRetrievalManager()
session = get_session(create_database())

---GET ALL CITIES---

all_cities = data_mgr.get_all_cities()

for city in all_cities:
    print(f"{city['name']}, {city['country']}")
    print(f"  Cost Index: {city['cost_index']}")
    print(f"  Best Time: {city['best_time_to_visit']}")
    print(f"  Currency: {city['currency']}")
    print()

Example Output:
  Paris, France
    Cost Index: 2.5
    Best Time: Apr-Jun, Sep-Oct
    Currency: EUR
  
  Goa, India
    Cost Index: 0.9
    Best Time: Nov-May
    Currency: INR


---GET ACTIVITIES IN A CITY (e.g., Paris)---

cities = data_mgr.get_all_cities()
paris = next(c for c in cities if c['name'] == 'Paris')

activities = data_mgr.get_city_activities(paris['id'])

for activity in activities:
    print(f"{activity['name']} - {activity['type']}")
    print(f"  Cost: ${activity['estimated_cost']}")
    print(f"  Duration: {activity['duration_hours']} hours")
    print(f"  Rating: {activity['ratings']}/5")
    print()

Example Output:
  Eiffel Tower Visit - Sightseeing
    Cost: $25
    Duration: 2 hours
    Rating: 4.8/5
  
  Michelin Star Dining - Food Tour
    Cost: $150
    Duration: 3 hours
    Rating: 4.9/5


---GET ACTIVITY TYPES---

types = data_mgr.get_activity_types()

for activity_type in types:
    print(f"{activity_type['name']}")
    print(f"  Cost Range: ${activity_type['estimated_cost_min']}-${activity_type['estimated_cost_max']}")
    print(f"  Avg Duration: {activity_type['average_duration_hours']} hours")


---GET ALL COUNTRIES---

countries = data_mgr.get_countries()
print(f"Available countries: {countries}")
# Output: ['France', 'India', 'Indonesia', 'Italy', 'Japan', 'Netherlands', 'Spain', 'Thailand', 'Vietnam']


---USING CITY DATA FOR TRIP PLANNING---

from models_extended import Trip, Stop, Activity, ActivityType

# Create trip to known city
cities_data = data_mgr.get_all_cities(country='India')
goa = next(c for c in cities_data if c['name'] == 'Goa')

trip = Trip(
    user_id=user_id,
    title="Goa Beach Getaway",
    destination=goa['name'],
    start_date=date(2026, 5, 1),
    end_date=date(2026, 5, 7),
    budget=50000 * goa['cost_index']  # Adjust budget based on cost index
)
session.add(trip)
session.commit()

# Add stops and activities from catalog
activities_in_goa = data_mgr.get_city_activities(goa['id'])

stop = Stop(
    trip_id=trip.id,
    location=goa['name'],
    arrival_date=date(2026, 5, 1),
    sequence_order=1
)
session.add(stop)
session.commit()

# Add activities from recommendations
for activity_data in activities_in_goa[:3]:
    activity = Activity(
        trip_id=trip.id,
        stop_id=stop.id,
        name=activity_data['name'],
        description=activity_data['description'],
        cost=activity_data['cost_in_usd'],
        status='planned'
    )
    session.add(activity)
session.commit()


════════════════════════════════════════════════════════════════════════════════
🔗 TRIP SHARING WITH PUBLIC URLS
════════════════════════════════════════════════════════════════════════════════

from auth_and_sharing import TripSharingManager

sharing = TripSharingManager()


---GENERATE SHARE LINK---

result = sharing.generate_share_link(
    trip_id=trip.id,
    user_id=user_id,
    can_edit=False,
    expiry_days=30,           # Link expires in 30 days
    password=None             # Optional password protection
)

if result['success']:
    print(f"✓ Trip shared successfully!")
    print(f"Share URL: {result['public_url']}")
    print(f"Full Link: {result['full_url']}")
    print(f"Can Edit: {result['can_edit']}")
    print(f"Expires: {result['expires_at']}")
else:
    print(f"Error: {result['message']}")


---GENERATE PASSWORD-PROTECTED LINK---

result = sharing.generate_share_link(
    trip_id=trip.id,
    user_id=user_id,
    can_edit=True,
    expiry_days=7,
    password="travelpass123"
)

# Recipients need password to view: https://travelbookapp.com/share/ABC12345


---ACCESS SHARED TRIP---

# Without password
result = sharing.access_shared_trip(
    public_url="ABC12345"
)

# With password
result = sharing.access_shared_trip(
    public_url="ABC12345",
    password="travelpass123"
)

if result['success']:
    trip = result['trip']
    shared_by = result['shared_by']
    
    print(f"Trip: {trip.title}")
    print(f"Shared by: {shared_by.name}")
    print(f"Can Edit: {result['can_edit']}")
    print(f"Views: {result['view_count']}")
else:
    print(f"Error: {result['message']}")
    # Possible errors:
    # - Shared trip not found or removed
    # - Link has expired
    # - Password required or incorrect


---GET USER'S SHARED TRIPS---

shared_trips = sharing.get_shared_trips_for_user(user_id)

for shared in shared_trips:
    print(f"{shared['trip_title']}")
    print(f"  URL: {shared['full_url']}")
    print(f"  Views: {shared['view_count']}")
    print(f"  Active: {shared['is_active']}")
    print()


---DISABLE SHARE LINK---

result = sharing.disable_share_link(trip_id, user_id)
if result['success']:
    print("Share link disabled - trip is now private")


════════════════════════════════════════════════════════════════════════════════
🧳 PACKING CHECKLIST SYSTEM
════════════════════════════════════════════════════════════════════════════════

from models_extended import (
    PackingChecklist, PackingChecklistItem, PackingItem
)


---CREATE PACKING CHECKLIST---

checklist = PackingChecklist(
    user_id=user_id,
    trip_id=trip.id,
    name=f"Packing for {trip.title}"
)
session.add(checklist)
session.commit()


---ADD ITEMS TO CHECKLIST---

# Option 1: Add from default items by category
packing_items = session.query(PackingItem).filter_by(category='Clothing').all()

for item in packing_items[:5]:  # Add first 5 clothing items
    checklist_item = PackingChecklistItem(
        checklist_id=checklist.id,
        packing_item_id=item.id,
        name=item.name,
        category=item.category,
        quantity=1,
        is_packed=False
    )
    session.add(checklist_item)
session.commit()


# Option 2: Add custom items
custom_item = PackingChecklistItem(
    checklist_id=checklist.id,
    packing_item_id=None,
    name="Camera Lens Cleaning Kit",
    category="Photography",
    quantity=1,
    is_packed=False,
    notes="For DSLR maintenance"
)
session.add(custom_item)
session.commit()


---GET PACKING CHECKLIST---

checklist = session.query(PackingChecklist).filter_by(
    user_id=user_id,
    trip_id=trip.id
).first()

print(f"Packing List: {checklist.name}")
print(f"Items: {len(checklist.items)}\n")

packed_count = 0
for item in checklist.items:
    status = "✓" if item.is_packed else "☐"
    print(f"{status} {item.name} (x{item.quantity}) - {item.category}")
    if item.is_packed:
        packed_count += 1

print(f"\nProgress: {packed_count}/{len(checklist.items)} items packed")


---CHECK/UNCHECK ITEMS---

item = checklist.items[0]
item.is_packed = True
session.commit()
print(f"✓ {item.name} marked as packed")


---ADD ITEM TO PACKING LIST---

item_to_add = PackingChecklistItem(
    checklist_id=checklist.id,
    name="Travel Insurance Documents",
    category="Documents",
    quantity=1,
    is_packed=False,
    notes="Keep in carry-on bag"
)
session.add(item_to_add)
session.commit()


---GET PACKING SUMMARY---

def get_packing_summary(checklist):
    total_items = len(checklist.items)
    packed_items = sum(1 for item in checklist.items if item.is_packed)
    unpacked_items = total_items - packed_items
    
    by_category = {}
    for item in checklist.items:
        if item.category not in by_category:
            by_category[item.category] = {'total': 0, 'packed': 0}
        by_category[item.category]['total'] += 1
        if item.is_packed:
            by_category[item.category]['packed'] += 1
    
    return {
        'total_items': total_items,
        'packed_items': packed_items,
        'unpacked_items': unpacked_items,
        'progress_percentage': (packed_items / total_items * 100) if total_items > 0 else 0,
        'by_category': by_category
    }

summary = get_packing_summary(checklist)
print(f"Packing Progress: {summary['progress_percentage']:.1f}%")
print(f"Packed: {summary['packed_items']}/{summary['total_items']}")
for category, counts in summary['by_category'].items():
    print(f"  {category}: {counts['packed']}/{counts['total']}")


════════════════════════════════════════════════════════════════════════════════
🔍 BACKEND DATA RETRIEVAL VERIFICATION
════════════════════════════════════════════════════════════════════════════════

Ensure all data correctly loads from database:


---VERIFY CITIES LOADED---

cities = session.query(City).all()
print(f"✓ Cities count: {len(cities)}")
for city in cities[:3]:
    print(f"  - {city.name}, {city.country} (Index: {city.cost_index})")


---VERIFY ACTIVITIES LOADED---

city_activities = session.query(CityActivity).all()
print(f"✓ City Activities count: {len(city_activities)}")


---VERIFY PACKING ITEMS LOADED---

items_by_category = {}
for item in session.query(PackingItem).all():
    items_by_category.setdefault(item.category, 0)
    items_by_category[item.category] += 1

print(f"✓ Packing Items count: {session.query(PackingItem).count()}")
for category, count in items_by_category.items():
    print(f"  - {category}: {count} items")


---VERIFY USER DATA SAVED---

user = session.query(User).filter_by(email="priya@example.com").first()
if user:
    print(f"✓ User found: {user.name}")
    print(f"  Email: {user.email}")
    print(f"  Password hash: {'✓' if user.password_hash else '✗'}")
else:
    print("✗ User not found in database")


════════════════════════════════════════════════════════════════════════════════
🚀 COMPLETE WORKFLOW EXAMPLE
════════════════════════════════════════════════════════════════════════════════

Step-by-step guide for a complete trip planning workflow:


1. USER REGISTRATION & LOGIN
────────────────────────────
from auth_and_sharing import AuthenticationManager

auth = AuthenticationManager()

# Signup
signup = auth.signup("Raj Patel", "raj@travel.com", "mypassword123")
if signup['success']:
    user_id = signup['user'].id
    print(f"✓ User registered: {user_id}")

# Login
login = auth.login("raj@travel.com", "mypassword123")
if login['success']:
    user = login['user']
    print(f"✓ Logged in: {user.name}")


2. BROWSE CITIES & ACTIVITIES
──────────────────────────────
from auth_and_sharing import DataRetrievalManager

data = DataRetrievalManager()

# Find destination
cities = data.get_all_cities(country='India')
print(f"Cities in India: {len(cities)}")

# Get activities for city
kerala = next(c for c in cities if c['name'] == 'Kerala')
activities = data.get_city_activities(kerala['id'])
print(f"Activities in Kerala: {len(activities)}")


3. CREATE TRIP WITH ACTIVITIES
───────────────────────────────
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

# Add stop
stop = Stop(
    trip_id=trip.id,
    location="Alleppey",
    arrival_date=date(2026, 6, 1),
    sequence_order=1
)
session.add(stop)
session.commit()

# Add recommended activities
for activity_data in activities[:3]:
    activity = Activity(
        trip_id=trip.id,
        stop_id=stop.id,
        name=activity_data['name'],
        cost=activity_data['cost_in_usd'],
        status='planned'
    )
    session.add(activity)
session.commit()


4. CREATE PACKING LIST
──────────────────────
from models_extended import PackingChecklist, PackingChecklistItem, PackingItem

checklist = PackingChecklist(
    user_id=user_id,
    trip_id=trip.id,
    name="Kerala Trip Packing"
)
session.add(checklist)
session.commit()

# Add essential items
essentials = session.query(PackingItem).filter_by(priority='essential').limit(10)
for item in essentials:
    checklist_item = PackingChecklistItem(
        checklist_id=checklist.id,
        packing_item_id=item.id,
        name=item.name,
        category=item.category
    )
    session.add(checklist_item)
session.commit()


5. SHARE TRIP
─────────────
from auth_and_sharing import TripSharingManager

sharing = TripSharingManager()

result = sharing.generate_share_link(
    trip_id=trip.id,
    user_id=user_id,
    can_edit=True
)

if result['success']:
    print(f"Share with friends: {result['full_url']}")


6. SHARE LINK ACCESS
────────────────────
# Friend accesses the link
access = sharing.access_shared_trip(result['public_url'])

if access['success']:
    print(f"Trip: {access['trip'].title}")
    print(f"Shared by: {access['shared_by'].name}")
    # Friend can view trip details


════════════════════════════════════════════════════════════════════════════════
📊 DATABASE SCHEMA ADDITIONS
════════════════════════════════════════════════════════════════════════════════

NEW TABLES:

CITIES
├─ id, name, country, latitude, longitude
├─ cost_index (1.0 = baseline), currency
├─ best_time_to_visit, description
└─ Relationships: Stops, CityActivities

ACTIVITY_TYPES
├─ id, name, description, icon
├─ estimated_cost_min/max
├─ average_duration_hours
└─ Relationships: Activities, CityActivities

CITY_ACTIVITIES
├─ id, city_id, activity_type_id
├─ name, description, estimated_cost
├─ cost_in_usd, duration_hours, ratings
└─ popularity, image_url

PACKING_ITEMS
├─ id, category, name, description
├─ priority (essential/important/optional)
└─ Relationships: PackingChecklists

PACKING_CHECKLISTS
├─ id, user_id, trip_id
├─ name, description, timestamps
└─ Relationships: User, Items

PACKING_CHECKLIST_ITEMS
├─ id, checklist_id, packing_item_id
├─ name, category, quantity, is_packed
└─ notes

SHARED_TRIPS
├─ id, trip_id, public_url
├─ shared_by_user_id, shared_at
├─ expires_at, view_count, is_active
├─ can_edit, password_protected
└─ password_hash


════════════════════════════════════════════════════════════════════════════════

Ready to build! Follow the workflow examples to integrate all features. 🌍

"""

if __name__ == '__main__':
    print(INTEGRATION_GUIDE)
