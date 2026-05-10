"""
Travel Database - Data Seeding with Cities, Activities, and Packing Items
Populates the database with realistic sample data
"""

from models_extended import (
    create_database, get_session, City, ActivityType, CityActivity,
    PackingItem, User, Trip, Stop, Activity, Expense, PackingChecklist,
    PackingChecklistItem
)
from datetime import date, datetime, timedelta

def seed_activity_types(session):
    """Create activity type categories"""
    print("\n[1] Seeding Activity Types...")
    
    activity_types = [
        {
            'name': 'Sightseeing',
            'description': 'Visit popular landmarks and tourist attractions',
            'icon': '🏛️',
            'estimated_cost_min': 10,
            'estimated_cost_max': 100,
            'average_duration_hours': 3
        },
        {
            'name': 'Food Tour',
            'description': 'Local cuisine and food experiences',
            'icon': '🍽️',
            'estimated_cost_min': 20,
            'estimated_cost_max': 150,
            'average_duration_hours': 2.5
        },
        {
            'name': 'Hiking',
            'description': 'Outdoor trekking and mountain activities',
            'icon': '⛰️',
            'estimated_cost_min': 0,
            'estimated_cost_max': 100,
            'average_duration_hours': 4
        },
        {
            'name': 'Water Sports',
            'description': 'Beach and water activities',
            'icon': '🏄',
            'estimated_cost_min': 50,
            'estimated_cost_max': 200,
            'average_duration_hours': 2
        },
        {
            'name': 'Museum Visit',
            'description': 'Art galleries and museums',
            'icon': '🎨',
            'estimated_cost_min': 10,
            'estimated_cost_max': 50,
            'average_duration_hours': 3
        },
        {
            'name': 'Shopping',
            'description': 'Markets and shopping centers',
            'icon': '🛍️',
            'estimated_cost_min': 20,
            'estimated_cost_max': 500,
            'average_duration_hours': 3
        },
        {
            'name': 'Adventure Sports',
            'description': 'Adrenaline-pumping activities',
            'icon': '🎢',
            'estimated_cost_min': 50,
            'estimated_cost_max': 300,
            'average_duration_hours': 1.5
        },
        {
            'name': 'Relaxation',
            'description': 'Spa, wellness, and relaxation',
            'icon': '🧘',
            'estimated_cost_min': 30,
            'estimated_cost_max': 200,
            'average_duration_hours': 2
        }
    ]
    
    existing_types = set(t.name for t in session.query(ActivityType).all())
    
    for at in activity_types:
        if at['name'] not in existing_types:
            activity_type = ActivityType(**at)
            session.add(activity_type)
            print(f"  ✓ {at['icon']} {at['name']}")
    
    session.commit()
    print(f"  ✓ Total Activity Types: {session.query(ActivityType).count()}")


def seed_cities(session):
    """Create popular cities"""
    print("\n[2] Seeding Cities...")
    
    cities_data = [
        # India
        {'name': 'Delhi', 'country': 'India', 'continent': 'Asia', 
         'latitude': 28.7041, 'longitude': 77.1025, 'cost_index': 1.2,
         'currency': 'INR', 'best_time_to_visit': 'Oct-Mar',
         'description': 'India\'s capital and historic cultural center'},
        
        {'name': 'Mumbai', 'country': 'India', 'continent': 'Asia',
         'latitude': 19.0760, 'longitude': 72.8777, 'cost_index': 1.3,
         'currency': 'INR', 'best_time_to_visit': 'Nov-Feb',
         'description': 'Financial capital with beaches and Bollywood culture'},
        
        {'name': 'Goa', 'country': 'India', 'continent': 'Asia',
         'latitude': 15.2993, 'longitude': 73.8243, 'cost_index': 0.9,
         'currency': 'INR', 'best_time_to_visit': 'Nov-May',
         'description': 'Tropical beaches and Portuguese heritage'},
        
        {'name': 'Kerala', 'country': 'India', 'continent': 'Asia',
         'latitude': 10.8505, 'longitude': 76.2711, 'cost_index': 1.0,
         'currency': 'INR', 'best_time_to_visit': 'Oct-May',
         'description': 'Backwater paradise with tea plantations'},
        
        {'name': 'Jaipur', 'country': 'India', 'continent': 'Asia',
         'latitude': 26.9124, 'longitude': 75.7873, 'cost_index': 0.8,
         'currency': 'INR', 'best_time_to_visit': 'Oct-Mar',
         'description': 'Pink city with Rajasthani architecture'},
        
        # Europe
        {'name': 'Paris', 'country': 'France', 'continent': 'Europe',
         'latitude': 48.8566, 'longitude': 2.3522, 'cost_index': 2.5,
         'currency': 'EUR', 'best_time_to_visit': 'Apr-Jun, Sep-Oct',
         'description': 'City of light with iconic monuments'},
        
        {'name': 'Amsterdam', 'country': 'Netherlands', 'continent': 'Europe',
         'latitude': 52.3676, 'longitude': 4.9041, 'cost_index': 2.2,
         'currency': 'EUR', 'best_time_to_visit': 'Apr-Oct',
         'description': 'Charming canals and tulip gardens'},
        
        {'name': 'Barcelona', 'country': 'Spain', 'continent': 'Europe',
         'latitude': 41.3851, 'longitude': 2.1734, 'cost_index': 2.0,
         'currency': 'EUR', 'best_time_to_visit': 'May-Jun, Sep-Oct',
         'description': 'Mediterranean beach city with Gaudí architecture'},
        
        {'name': 'Rome', 'country': 'Italy', 'continent': 'Europe',
         'latitude': 41.9028, 'longitude': 12.4964, 'cost_index': 2.0,
         'currency': 'EUR', 'best_time_to_visit': 'Apr-May, Sep-Oct',
         'description': 'Ancient history and Renaissance art'},
        
        # Southeast Asia
        {'name': 'Bangkok', 'country': 'Thailand', 'continent': 'Asia',
         'latitude': 13.7563, 'longitude': 100.5018, 'cost_index': 1.1,
         'currency': 'THB', 'best_time_to_visit': 'Nov-Feb',
         'description': 'Bustling metropolis with temples and street food'},
        
        {'name': 'Bali', 'country': 'Indonesia', 'continent': 'Asia',
         'latitude': -8.6705, 'longitude': 115.2126, 'cost_index': 0.7,
         'currency': 'IDR', 'best_time_to_visit': 'Apr-Oct',
         'description': 'Island paradise with temples and beaches'},
        
        {'name': 'Hanoi', 'country': 'Vietnam', 'continent': 'Asia',
         'latitude': 21.0285, 'longitude': 105.8542, 'cost_index': 0.6,
         'currency': 'VND', 'best_time_to_visit': 'Oct-Apr',
         'description': 'Ancient capital with centuries-old culture'},
        
        # Japan
        {'name': 'Tokyo', 'country': 'Japan', 'continent': 'Asia',
         'latitude': 35.6762, 'longitude': 139.6503, 'cost_index': 2.5,
         'currency': 'JPY', 'best_time_to_visit': 'Mar-May, Sep-Nov',
         'description': 'Modern mega-city blending tradition and innovation'},
        
        {'name': 'Kyoto', 'country': 'Japan', 'continent': 'Asia',
         'latitude': 35.0116, 'longitude': 135.7681, 'cost_index': 2.2,
         'currency': 'JPY', 'best_time_to_visit': 'Mar-May, Sep-Nov',
         'description': 'Temples and traditional gardens'},
    ]
    
    existing_cities = set((c.name, c.country) for c in session.query(City).all())
    
    for city_data in cities_data:
        key = (city_data['name'], city_data['country'])
        if key not in existing_cities:
            city = City(**city_data)
            session.add(city)
            print(f"  ✓ {city_data['name']}, {city_data['country']} (Cost Index: {city_data['cost_index']})")
    
    session.commit()
    print(f"  ✓ Total Cities: {session.query(City).count()}")


def seed_city_activities(session):
    """Create activities for each city"""
    print("\n[3] Seeding City Activities...")
    
    # Get activity types and cities
    activity_types = {at.name: at.id for at in session.query(ActivityType).all()}
    cities = {(c.name, c.country): c.id for c in session.query(City).all()}
    
    activities_by_city = {
        ('Paris', 'France'): [
            {'name': 'Eiffel Tower Visit', 'activity_type': 'Sightseeing', 'cost': 25, 'duration': 2, 'ratings': 4.8},
            {'name': 'Louvre Museum', 'activity_type': 'Museum Visit', 'cost': 17, 'duration': 3.5, 'ratings': 4.7},
            {'name': 'Michelin Star Dining', 'activity_type': 'Food Tour', 'cost': 150, 'duration': 3, 'ratings': 4.9},
            {'name': 'Seine River Cruise', 'activity_type': 'Sightseeing', 'cost': 15, 'duration': 1, 'ratings': 4.6},
        ],
        ('Goa', 'India'): [
            {'name': 'Beach Resort Relaxation', 'activity_type': 'Relaxation', 'cost': 40, 'duration': 8, 'ratings': 4.5},
            {'name': 'Water Sports', 'activity_type': 'Water Sports', 'cost': 50, 'duration': 2, 'ratings': 4.4},
            {'name': 'Seafood Feast', 'activity_type': 'Food Tour', 'cost': 25, 'duration': 2, 'ratings': 4.6},
            {'name': 'Fort Aguada Visit', 'activity_type': 'Sightseeing', 'cost': 5, 'duration': 2, 'ratings': 4.3},
        ],
        ('Kerala', 'India'): [
            {'name': 'Houseboat Backwater Cruise', 'activity_type': 'Relaxation', 'cost': 60, 'duration': 12, 'ratings': 4.8},
            {'name': 'Tea Plantation Trek', 'activity_type': 'Hiking', 'cost': 20, 'duration': 4, 'ratings': 4.5},
            {'name': 'Ayurvedic Spa', 'activity_type': 'Relaxation', 'cost': 50, 'duration': 2, 'ratings': 4.7},
            {'name': 'Local Kerala Food Tour', 'activity_type': 'Food Tour', 'cost': 15, 'duration': 2.5, 'ratings': 4.6},
        ],
        ('Bangkok', 'Thailand'): [
            {'name': 'Grand Palace Tour', 'activity_type': 'Sightseeing', 'cost': 15, 'duration': 2.5, 'ratings': 4.6},
            {'name': 'Street Food Market', 'activity_type': 'Food Tour', 'cost': 10, 'duration': 2, 'ratings': 4.8},
            {'name': 'Muay Thai Fight Show', 'activity_type': 'Adventure Sports', 'cost': 20, 'duration': 2, 'ratings': 4.5},
            {'name': 'Temple Shopping', 'activity_type': 'Shopping', 'cost': 50, 'duration': 3, 'ratings': 4.4},
        ],
        ('Tokyo', 'Japan'): [
            {'name': 'Senso-ji Temple', 'activity_type': 'Sightseeing', 'cost': 5, 'duration': 1.5, 'ratings': 4.7},
            {'name': 'Sushi Making Class', 'activity_type': 'Food Tour', 'cost': 80, 'duration': 2, 'ratings': 4.8},
            {'name': 'Shibuya Crossing & Shopping', 'activity_type': 'Shopping', 'cost': 100, 'duration': 4, 'ratings': 4.6},
            {'name': 'Art Museum', 'activity_type': 'Museum Visit', 'cost': 15, 'duration': 2.5, 'ratings': 4.5},
        ],
        ('Barcelona', 'Spain'): [
            {'name': 'Sagrada Familia', 'activity_type': 'Sightseeing', 'cost': 26, 'duration': 2, 'ratings': 4.8},
            {'name': 'Park Güell', 'activity_type': 'Sightseeing', 'cost': 14, 'duration': 1.5, 'ratings': 4.7},
            {'name': 'Spanish Tapas Tour', 'activity_type': 'Food Tour', 'cost': 40, 'duration': 2.5, 'ratings': 4.6},
            {'name': 'Beach Day', 'activity_type': 'Water Sports', 'cost': 0, 'duration': 5, 'ratings': 4.5},
        ],
    }
    
    count = 0
    for (city_name, country), activities in activities_by_city.items():
        if (city_name, country) not in cities:
            continue
        
        city_id = cities[(city_name, country)]
        
        for activity_data in activities:
            activity_type_name = activity_data['activity_type']
            if activity_type_name not in activity_types:
                continue
            
            # Check if already exists
            existing = session.query(CityActivity).filter_by(
                city_id=city_id,
                name=activity_data['name']
            ).first()
            
            if not existing:
                city_activity = CityActivity(
                    city_id=city_id,
                    activity_type_id=activity_types[activity_type_name],
                    name=activity_data['name'],
                    description=f"Experience {activity_data['name']} in {city_name}",
                    estimated_cost=activity_data['cost'],
                    cost_in_usd=activity_data['cost'],
                    duration_hours=activity_data['duration'],
                    ratings=activity_data['ratings'],
                    popularity=5
                )
                session.add(city_activity)
                count += 1
                print(f"  ✓ {city_name}: {activity_data['name']}")
    
    session.commit()
    print(f"  ✓ Total City Activities: {session.query(CityActivity).count()}")


def seed_packing_items(session):
    """Create default packing items"""
    print("\n[4] Seeding Packing Items...")
    
    packing_items_data = {
        'Clothing': [
            ('Casual T-Shirts', 'Short-sleeve comfortable shirts', 'essential'),
            ('Jeans/Pants', 'Comfortable daily wear', 'essential'),
            ('Undergarments', 'Socks and underwear', 'essential'),
            ('Light Jacket', 'For cool evenings or flights', 'important'),
            ('Formal Outfit', 'For dinner or special occasions', 'optional'),
            ('Swimwear', 'For beach/pool activities', 'important'),
            ('Comfortable Shoes', 'Walking and daily activities', 'essential'),
            ('Flip-flops/Sandals', 'Casual footwear', 'important'),
        ],
        'Electronics': [
            ('Phone Charger', 'Essential for communication', 'essential'),
            ('Power Bank', 'Backup battery for devices', 'important'),
            ('Headphones', 'Music and audio', 'optional'),
            ('Camera', 'Photography equipment', 'optional'),
            ('Laptop/Tablet', 'Work or entertainment', 'optional'),
            ('Universal Power Adapter', 'For different outlets', 'essential'),
            ('Phone/Camera Cables', 'Data and charging cables', 'essential'),
        ],
        'Documents': [
            ('Passport', 'Essential travel document', 'essential'),
            ('Travel Insurance', 'Health and trip insurance documents', 'important'),
            ('Flight Tickets', 'Booking confirmations', 'essential'),
            ('Hotel Reservations', 'Accommodation bookings', 'important'),
            ('Visa Documents', 'If required', 'essential'),
            ('Driver License', 'For car rentals', 'optional'),
            ('Medical Prescriptions', 'If applicable', 'important'),
        ],
        'Toiletries': [
            ('Toothbrush/Toothpaste', 'Dental hygiene', 'essential'),
            ('Deodorant', 'Personal care', 'important'),
            ('Shampoo/Soap', 'Bathing essentials', 'essential'),
            ('Moisturizer/Sunscreen', 'Skin protection', 'important'),
            ('Medications', 'Personal medications', 'essential'),
            ('First Aid Kit', 'Basic medical supplies', 'important'),
            ('Feminine Hygiene Products', 'If required', 'essential'),
        ],
        'Accessories': [
            ('Hat/Cap', 'Sun protection', 'important'),
            ('Sunglasses', 'Eye protection', 'important'),
            ('Scarf/Wrap', 'Versatile clothing', 'optional'),
            ('Belt', 'For pants', 'optional'),
            ('Watch', 'Timekeeping', 'optional'),
            ('Jewelry', 'Accessories', 'optional'),
            ('Backpack/Day Bag', 'Day exploration bag', 'important'),
        ],
        'Recreation': [
            ('Book', 'Reading material', 'optional'),
            ('Travel Guide', 'Destination information', 'optional'),
            ('Notebook', 'Travel journal', 'optional'),
            ('Pen', 'Writing', 'optional'),
            ('Cards/Games', 'Entertainment', 'optional'),
        ]
    }
    
    existing_items = set((pi.category, pi.name) for pi in session.query(PackingItem).all())
    
    for category, items in packing_items_data.items():
        for name, description, priority in items:
            if (category, name) not in existing_items:
                packing_item = PackingItem(
                    category=category,
                    name=name,
                    description=description,
                    priority=priority
                )
                session.add(packing_item)
                print(f"  ✓ {category}: {name}")
    
    session.commit()
    print(f"  ✓ Total Packing Items: {session.query(PackingItem).count()}")


def seed_sample_user_data(session):
    """Create sample user with trip and packing checklist"""
    print("\n[5] Seeding Sample User Data...")
    
    # Check if sample user exists
    sample_user = session.query(User).filter_by(email='sample@travelapp.com').first()
    if sample_user:
        print("  ✓ Sample user already exists")
        return
    
    # Create user (without password for demo)
    user = User(
        name="Priya Demo",
        email="sample@travelapp.com",
        phone="+91-9876543210",
        address="Ahmedabad, Gujarat"
    )
    user.set_password("demo123")
    session.add(user)
    session.commit()
    print(f"  ✓ Sample user created: {user.name}")
    
    # Create trip
    trip = Trip(
        user_id=user.id,
        title="Kerala Backwater Holiday",
        description="Relaxing 10-day trip to Kerala",
        destination="Kerala",
        start_date=date(2026, 6, 1),
        end_date=date(2026, 6, 10),
        budget=50000.0
    )
    session.add(trip)
    session.commit()
    trip.generate_public_url()
    session.commit()
    print(f"  ✓ Sample trip created: {trip.title}")
    print(f"    Public URL: {trip.public_url}")
    
    # Add packing checklist
    checklist = PackingChecklist(
        user_id=user.id,
        trip_id=trip.id,
        name="Kerala Trip Packing List"
    )
    session.add(checklist)
    session.commit()
    print(f"  ✓ Packing checklist created")
    
    # Add packing items to checklist
    essential_items = session.query(PackingItem).filter_by(priority='essential').limit(5).all()
    for item in essential_items:
        checklist_item = PackingChecklistItem(
            checklist_id=checklist.id,
            packing_item_id=item.id,
            name=item.name,
            category=item.category,
            is_packed=False
        )
        session.add(checklist_item)
    session.commit()
    print(f"  ✓ Added {len(essential_items)} items to packing list")


def seed_all_data(database_url='sqlite:///travel_database.db'):
    """Run all seeding functions"""
    print("╔═══════════════════════════════════════════════════════════════╗")
    print("║        SEEDING TRAVEL DATABASE WITH SAMPLE DATA              ║")
    print("╚═══════════════════════════════════════════════════════════════╝")
    
    engine = create_database(database_url)
    session = get_session(engine)
    
    try:
        seed_activity_types(session)
        seed_cities(session)
        seed_city_activities(session)
        seed_packing_items(session)
        seed_sample_user_data(session)
        
        print("\n" + "═" * 67)
        print("✓ DATA SEEDING COMPLETE!")
        print("═" * 67)
        print(f"\n✓ Activity Types: {session.query(ActivityType).count()}")
        print(f"✓ Cities: {session.query(City).count()}")
        print(f"✓ City Activities: {session.query(CityActivity).count()}")
        print(f"✓ Packing Items: {session.query(PackingItem).count()}")
        print(f"✓ Users: {session.query(User).count()}")
        print(f"✓ Trips: {session.query(Trip).count()}")
        
    except Exception as e:
        print(f"\n✗ Error during seeding: {str(e)}")
        session.rollback()
    finally:
        session.close()


if __name__ == '__main__':
    seed_all_data()
