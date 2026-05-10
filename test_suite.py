"""
Traveloop - Comprehensive Testing Suite
Unit tests, integration tests, and test fixtures for all modules
Professional-grade testing for travel planning platform
"""

import unittest
from datetime import datetime, date, timedelta
from models import create_database, get_session, User, Trip
from trip_management_engine import TripManagementEngine
from financial_intelligence import FinancialIntelligence
from social_collaboration import SocialCollaborationEngine
from admin_analytics import AdminAnalyticsDashboard

class TestRunner:
    """Test suite for all database features"""
    
    def __init__(self, database_url='sqlite:///travel_database_test.db'):
        self.db_url = database_url
        self.engine = create_database(database_url)
        self.session = get_session(self.engine)
        self.test_results = []
    
    def run_all_tests(self):
        """Run all test suites"""
        print("╔" + "═" * 78 + "╗")
        print("║" + " " * 20 + "TRAVEL DATABASE - TEST SUITE" + " " * 30 + "║")
        print("╚" + "═" * 78 + "╝")
        
        self.test_database_initialization()
        self.test_authentication()
        self.test_city_and_activity_data()
        self.test_trip_creation()
        self.test_packing_list()
        self.test_trip_sharing()
        self.test_data_retrieval()
        
        self.print_test_summary()
    
    def test_database_initialization(self):
        """Test database table creation"""
        print("\n[1] Testing Database Initialization...")
        try:
            # Check tables exist
            tables = [
                ('users', User),
                ('trips', Trip),
                ('stops', Stop),
                ('activities', Activity),
                ('cities', City),
                ('activity_types', ActivityType),
                ('city_activities', CityActivity),
                ('packing_items', PackingItem),
                ('packing_checklists', PackingChecklist),
                ('packing_checklist_items', PackingChecklistItem),
                ('shared_trips', SharedTrip),
            ]
            
            for table_name, model in tables:
                count = self.session.query(model).count()
                print(f"  ✓ Table '{table_name}' exists")
            
            self.test_results.append(("Database Initialization", True, None))
        except Exception as e:
            print(f"  ✗ Error: {str(e)}")
            self.test_results.append(("Database Initialization", False, str(e)))
    
    def test_authentication(self):
        """Test user authentication"""
        print("\n[2] Testing Authentication...")
        auth = AuthenticationManager(self.db_url)
        
        try:
            # Test signup
            signup = auth.signup(
                "Test User",
                "testuser@example.com",
                "password123",
                "+1-234-567-8900"
            )
            assert signup['success'], f"Signup failed: {signup['message']}"
            print(f"  ✓ Signup successful")
            
            # Test login
            login = auth.login("testuser@example.com", "password123")
            assert login['success'], f"Login failed: {login['message']}"
            self.test_user_id = login['user'].id
            print(f"  ✓ Login successful (User ID: {self.test_user_id})")
            
            # Test invalid login
            invalid_login = auth.login("testuser@example.com", "wrongpassword")
            assert not invalid_login['success'], "Invalid login should fail"
            print(f"  ✓ Invalid login rejected")
            
            # Test change password
            change_pwd = auth.change_password(
                self.test_user_id,
                "password123",
                "newpassword456"
            )
            assert change_pwd['success'], f"Password change failed: {change_pwd['message']}"
            print(f"  ✓ Password change successful")
            
            # Verify new password works
            new_login = auth.login("testuser@example.com", "newpassword456")
            assert new_login['success'], "New password should work"
            print(f"  ✓ New password verified")
            
            self.test_results.append(("Authentication", True, None))
        except Exception as e:
            print(f"  ✗ Error: {str(e)}")
            traceback.print_exc()
            self.test_results.append(("Authentication", False, str(e)))
        finally:
            auth.close()
    
    def test_city_and_activity_data(self):
        """Test city and activity data"""
        print("\n[3] Testing City & Activity Data...")
        
        try:
            # Test cities exist
            cities = self.session.query(City).all()
            assert len(cities) > 0, "No cities found in database"
            print(f"  ✓ Cities loaded: {len(cities)} cities")
            
            # Test activity types exist
            activity_types = self.session.query(ActivityType).all()
            assert len(activity_types) > 0, "No activity types found"
            print(f"  ✓ Activity types loaded: {len(activity_types)} types")
            
            # Test city activities exist
            city_activities = self.session.query(CityActivity).all()
            assert len(city_activities) > 0, "No city activities found"
            print(f"  ✓ City activities loaded: {len(city_activities)} activities")
            
            # Verify city data structure
            city = cities[0]
            assert city.name is not None, "City name missing"
            assert city.country is not None, "City country missing"
            assert city.cost_index > 0, "City cost index invalid"
            print(f"  ✓ City data structure valid")
            
            # Verify activity data structure
            activity = city_activities[0]
            assert activity.activity_type_id is not None, "Activity type ID missing"
            assert activity.estimated_cost >= 0, "Activity cost invalid"
            print(f"  ✓ Activity data structure valid")
            
            self.test_results.append(("City & Activity Data", True, None))
        except Exception as e:
            print(f"  ✗ Error: {str(e)}")
            self.test_results.append(("City & Activity Data", False, str(e)))
    
    def test_trip_creation(self):
        """Test trip creation with stops and activities"""
        print("\n[4] Testing Trip Creation...")
        
        try:
            # Get test city
            city = self.session.query(City).first()
            assert city is not None, "No city found"
            
            # Create trip
            trip = Trip(
                user_id=self.test_user_id,
                title="Test Trip",
                destination=city.name,
                start_date=date(2026, 6, 1),
                end_date=date(2026, 6, 10),
                budget=50000.0
            )
            self.session.add(trip)
            self.session.commit()
            self.test_trip_id = trip.id
            print(f"  ✓ Trip created (ID: {trip.id})")
            
            # Create stop linked to city
            stop = Stop(
                trip_id=trip.id,
                location=city.name,
                city_id=city.id,
                arrival_date=date(2026, 6, 1),
                departure_date=date(2026, 6, 5),
                sequence_order=1
            )
            self.session.add(stop)
            self.session.commit()
            print(f"  ✓ Stop created linked to city")
            
            # Create activity
            activity = Activity(
                trip_id=trip.id,
                stop_id=stop.id,
                name="Test Activity",
                cost=1000.0,
                status='planned'
            )
            self.session.add(activity)
            self.session.commit()
            print(f"  ✓ Activity created")
            
            # Verify relationships
            assert len(trip.stops) == 1, "Trip should have 1 stop"
            assert len(trip.activities) == 1, "Trip should have 1 activity"
            assert trip.stops[0].city_id == city.id, "Stop should be linked to city"
            print(f"  ✓ Relationships verified")
            
            self.test_results.append(("Trip Creation", True, None))
        except Exception as e:
            print(f"  ✗ Error: {str(e)}")
            traceback.print_exc()
            self.test_results.append(("Trip Creation", False, str(e)))
    
    def test_packing_list(self):
        """Test packing checklist system"""
        print("\n[5] Testing Packing Checklist...")
        
        try:
            # Create packing checklist
            checklist = PackingChecklist(
                user_id=self.test_user_id,
                trip_id=self.test_trip_id,
                name="Test Packing List"
            )
            self.session.add(checklist)
            self.session.commit()
            print(f"  ✓ Packing checklist created")
            
            # Get packing items
            packing_items = self.session.query(PackingItem).limit(5).all()
            assert len(packing_items) > 0, "No packing items found"
            print(f"  ✓ Packing items available: {len(packing_items)} items")
            
            # Add items to checklist
            for item in packing_items:
                checklist_item = PackingChecklistItem(
                    checklist_id=checklist.id,
                    packing_item_id=item.id,
                    name=item.name,
                    category=item.category,
                    is_packed=False
                )
                self.session.add(checklist_item)
            self.session.commit()
            print(f"  ✓ Items added to checklist")
            
            # Verify checklist structure
            assert len(checklist.items) == len(packing_items), "Items not added properly"
            print(f"  ✓ Checklist has {len(checklist.items)} items")
            
            # Test marking items as packed
            checklist.items[0].is_packed = True
            self.session.commit()
            packed_count = sum(1 for item in checklist.items if item.is_packed)
            assert packed_count == 1, "Item marking failed"
            print(f"  ✓ Item marked as packed")
            
            self.test_results.append(("Packing Checklist", True, None))
        except Exception as e:
            print(f"  ✗ Error: {str(e)}")
            traceback.print_exc()
            self.test_results.append(("Packing Checklist", False, str(e)))
    
    def test_trip_sharing(self):
        """Test trip sharing functionality"""
        print("\n[6] Testing Trip Sharing...")
        sharing = TripSharingManager(self.db_url)
        
        try:
            # Generate share link
            result = sharing.generate_share_link(
                trip_id=self.test_trip_id,
                user_id=self.test_user_id,
                can_edit=True,
                expiry_days=30
            )
            assert result['success'], f"Share link generation failed: {result['message']}"
            self.public_url = result['public_url']
            print(f"  ✓ Share link generated: {result['public_url']}")
            print(f"    Full URL: {result['full_url']}")
            
            # Access shared trip
            access_result = sharing.access_shared_trip(self.public_url)
            assert access_result['success'], f"Accessing shared trip failed: {access_result['message']}"
            assert access_result['trip'].id == self.test_trip_id, "Wrong trip returned"
            print(f"  ✓ Shared trip accessed successfully")
            print(f"    View count: {access_result['view_count']}")
            
            # Test password protection
            result2 = sharing.generate_share_link(
                trip_id=self.test_trip_id,
                user_id=self.test_user_id,
                password="testpass123"
            )
            assert result2['success'], "Password-protected link generation failed"
            print(f"  ✓ Password-protected link created")
            
            # Get user's shared trips
            shared_trips = sharing.get_shared_trips_for_user(self.test_user_id)
            assert len(shared_trips) > 0, "No shared trips returned"
            print(f"  ✓ User has {len(shared_trips)} shared trip(s)")
            
            self.test_results.append(("Trip Sharing", True, None))
        except Exception as e:
            print(f"  ✗ Error: {str(e)}")
            traceback.print_exc()
            self.test_results.append(("Trip Sharing", False, str(e)))
        finally:
            sharing.close()
    
    def test_data_retrieval(self):
        """Test data retrieval methods"""
        print("\n[7] Testing Data Retrieval...")
        data_mgr = DataRetrievalManager(self.db_url)
        
        try:
            # Get all cities
            cities = data_mgr.get_all_cities()
            assert len(cities) > 0, "No cities retrieved"
            print(f"  ✓ Retrieved {len(cities)} cities")
            
            # Get cities by country
            countries = data_mgr.get_countries()
            assert len(countries) > 0, "No countries retrieved"
            print(f"  ✓ Retrieved {len(countries)} countries")
            
            cities_india = data_mgr.get_all_cities(country='India')
            if len(cities_india) > 0:
                print(f"  ✓ Retrieved {len(cities_india)} cities in India")
            
            # Get activity types
            types = data_mgr.get_activity_types()
            assert len(types) > 0, "No activity types retrieved"
            print(f"  ✓ Retrieved {len(types)} activity types")
            
            # Get city activities
            if len(cities) > 0:
                city_id = cities[0]['id']
                activities = data_mgr.get_city_activities(city_id)
                print(f"  ✓ Retrieved {len(activities)} activities for city")
            
            # Get packing items
            items = data_mgr.get_packing_items_by_category()
            assert len(items) > 0, "No packing items retrieved"
            print(f"  ✓ Retrieved packing items ({len(items)} categories)")
            
            self.test_results.append(("Data Retrieval", True, None))
        except Exception as e:
            print(f"  ✗ Error: {str(e)}")
            traceback.print_exc()
            self.test_results.append(("Data Retrieval", False, str(e)))
        finally:
            data_mgr.close()
    
    def print_test_summary(self):
        """Print test summary"""
        print("\n" + "═" * 80)
        print("TEST SUMMARY")
        print("═" * 80)
        
        passed = sum(1 for name, result, error in self.test_results if result)
        total = len(self.test_results)
        
        for name, result, error in self.test_results:
            status = "✓ PASS" if result else "✗ FAIL"
            print(f"{status:8} | {name}")
            if error:
                print(f"         | Error: {error}")
        
        print("═" * 80)
        print(f"TOTAL: {passed}/{total} tests passed ({passed/total*100:.1f}%)")
        print("═" * 80)
        
        if passed == total:
            print("✓ ALL TESTS PASSED - Database is ready for use!")
        else:
            print("✗ Some tests failed - Review errors above")


def main():
    """Run test suite"""
    print("\nInitializing test suite...\n")
    
    runner = TestRunner()
    runner.run_all_tests()
    
    print("\nTest complete. Database connection closed.")


if __name__ == '__main__':
    main()
