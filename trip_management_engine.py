"""
Traveloop - Trip Management Engine
Core module for multi-city itinerary building and management
Handles: Trip creation, stop sequencing, activity assignment, timeline management
"""

from datetime import datetime, date, timedelta
from typing import List, Dict, Optional, Tuple
from models import Trip, Stop, Activity, User, create_database, get_session
from sqlalchemy.orm import Session


class TripManagementEngine:
    """
    Core engine for managing multi-city trips and itineraries
    Professional-grade orchestration for complex travel planning
    """
    
    def __init__(self, database_url='sqlite:///travel_database.db'):
        """Initialize the trip management engine"""
        self.database_url = database_url
        self.session = get_session(database_url)
    
    # ==================== TRIP CREATION & MANAGEMENT ====================
    
    def create_trip(self, user_id: int, title: str, start_date: date, 
                   end_date: date, description: str = "", budget: float = 0.0) -> Trip:
        """
        Create a new multi-city trip
        
        Args:
            user_id: ID of the user creating the trip
            title: Trip name (e.g., "Europe Summer 2024")
            start_date: Trip start date
            end_date: Trip end date
            description: Trip description
            budget: Total budget allocated
            
        Returns:
            Trip object
        """
        trip = Trip(
            user_id=user_id,
            title=title,
            start_date=start_date,
            end_date=end_date,
            description=description,
            budget=budget,
            destination="Multi-city"  # Default for multi-city trips
        )
        self.session.add(trip)
        self.session.commit()
        return trip
    
    def get_trip(self, trip_id: int) -> Optional[Trip]:
        """Get trip by ID"""
        return self.session.query(Trip).filter(Trip.id == trip_id).first()
    
    def get_user_trips(self, user_id: int) -> List[Trip]:
        """Get all trips for a specific user"""
        return self.session.query(Trip).filter(Trip.user_id == user_id).all()
    
    def update_trip(self, trip_id: int, **kwargs) -> Trip:
        """Update trip details (title, budget, description, etc.)"""
        trip = self.get_trip(trip_id)
        if trip:
            for key, value in kwargs.items():
                if hasattr(trip, key):
                    setattr(trip, key, value)
            trip.updated_at = datetime.utcnow()
            self.session.commit()
        return trip
    
    def delete_trip(self, trip_id: int) -> bool:
        """Delete a trip and all associated data"""
        trip = self.get_trip(trip_id)
        if trip:
            self.session.delete(trip)
            self.session.commit()
            return True
        return False
    
    # ==================== STOP/CITY MANAGEMENT ====================
    
    def add_stop(self, trip_id: int, location: str, arrival_date: date, 
                departure_date: date = None, latitude: float = None, 
                longitude: float = None, notes: str = "") -> Stop:
        """
        Add a city/stop to the trip
        
        Args:
            trip_id: ID of the trip
            location: City/location name
            arrival_date: Date of arrival
            departure_date: Date of departure (optional)
            latitude: GPS latitude
            longitude: GPS longitude
            notes: Location notes
            
        Returns:
            Stop object
        """
        trip = self.get_trip(trip_id)
        if not trip:
            raise ValueError("Trip not found")
        
        # Calculate sequence order based on arrival date
        existing_stops = self.session.query(Stop).filter(Stop.trip_id == trip_id).all()
        sequence_order = len(existing_stops) + 1
        
        stop = Stop(
            trip_id=trip_id,
            location=location,
            arrival_date=arrival_date,
            departure_date=departure_date or arrival_date,
            latitude=latitude,
            longitude=longitude,
            notes=notes,
            sequence_order=sequence_order
        )
        self.session.add(stop)
        self.session.commit()
        return stop
    
    def get_trip_stops(self, trip_id: int) -> List[Stop]:
        """Get all stops for a trip in chronological order"""
        return self.session.query(Stop).filter(Stop.trip_id == trip_id).order_by(Stop.sequence_order).all()
    
    def reorder_stops(self, trip_id: int, stop_ids: List[int]) -> bool:
        """
        Reorder stops in a trip (dynamic sequencing)
        
        Args:
            trip_id: ID of the trip
            stop_ids: List of stop IDs in desired order
            
        Returns:
            Success status
        """
        try:
            for order, stop_id in enumerate(stop_ids, 1):
                stop = self.session.query(Stop).filter(Stop.id == stop_id, Stop.trip_id == trip_id).first()
                if stop:
                    stop.sequence_order = order
            self.session.commit()
            return True
        except Exception as e:
            print(f"Error reordering stops: {e}")
            return False
    
    def remove_stop(self, stop_id: int) -> bool:
        """Remove a stop from a trip"""
        stop = self.session.query(Stop).filter(Stop.id == stop_id).first()
        if stop:
            self.session.delete(stop)
            self.session.commit()
            return True
        return False
    
    # ==================== ACTIVITY MANAGEMENT ====================
    
    def add_activity(self, trip_id: int, stop_id: int, name: str, 
                    activity_type: str, start_time: datetime = None, 
                    end_time: datetime = None, cost: float = 0.0, 
                    description: str = "") -> Activity:
        """
        Add an activity to a specific stop
        
        Args:
            trip_id: ID of the trip
            stop_id: ID of the stop (city)
            name: Activity name
            activity_type: Type (hiking, sightseeing, dining, etc.)
            start_time: Activity start time
            end_time: Activity end time
            cost: Cost of the activity
            description: Description
            
        Returns:
            Activity object
        """
        activity = Activity(
            trip_id=trip_id,
            stop_id=stop_id,
            name=name,
            activity_type=activity_type,
            start_time=start_time,
            end_time=end_time,
            cost=cost,
            description=description,
            status='planned'
        )
        self.session.add(activity)
        self.session.commit()
        return activity
    
    def get_stop_activities(self, stop_id: int) -> List[Activity]:
        """Get all activities for a specific stop"""
        return self.session.query(Activity).filter(Activity.stop_id == stop_id).all()
    
    def get_trip_activities(self, trip_id: int) -> List[Activity]:
        """Get all activities for a trip"""
        return self.session.query(Activity).filter(Activity.trip_id == trip_id).all()
    
    def update_activity_status(self, activity_id: int, status: str) -> Activity:
        """Update activity status (planned, completed, cancelled)"""
        activity = self.session.query(Activity).filter(Activity.id == activity_id).first()
        if activity:
            activity.status = status
            self.session.commit()
        return activity
    
    # ==================== TIMELINE & VISUALIZATION ====================
    
    def get_day_wise_itinerary(self, trip_id: int) -> Dict:
        """
        Get itinerary organized by day
        
        Returns:
            Dictionary with dates as keys and activities as values
        """
        trip = self.get_trip(trip_id)
        if not trip:
            return {}
        
        itinerary = {}
        current_date = trip.start_date
        
        while current_date <= trip.end_date:
            itinerary[str(current_date)] = {
                'date': current_date,
                'stops': [],
                'activities': []
            }
            current_date += timedelta(days=1)
        
        # Populate with stops and activities
        for stop in self.get_trip_stops(trip_id):
            stop_date = stop.arrival_date
            while stop_date <= stop.departure_date:
                date_key = str(stop_date)
                if date_key in itinerary:
                    itinerary[date_key]['stops'].append(stop)
                stop_date += timedelta(days=1)
        
        for activity in self.get_trip_activities(trip_id):
            if activity.start_time:
                date_key = str(activity.start_time.date())
                if date_key in itinerary:
                    itinerary[date_key]['activities'].append(activity)
        
        return itinerary
    
    def get_stop_sequence(self, trip_id: int) -> List[Dict]:
        """
        Get the sequence of cities/stops in a trip
        Useful for timeline visualization
        """
        stops = self.get_trip_stops(trip_id)
        sequence = []
        
        for stop in stops:
            num_days = (stop.departure_date - stop.arrival_date).days + 1
            sequence.append({
                'stop_id': stop.id,
                'location': stop.location,
                'arrival_date': stop.arrival_date,
                'departure_date': stop.departure_date,
                'num_days': num_days,
                'latitude': stop.latitude,
                'longitude': stop.longitude,
                'activities_count': len(self.get_stop_activities(stop.id))
            })
        
        return sequence
    
    # ==================== GLOBAL SEARCH & DISCOVERY ====================
    
    def search_cities(self, query: str, limit: int = 10) -> List[Dict]:
        """
        Search for cities to add to trip
        This would integrate with external APIs or local database
        
        Returns:
            List of cities with metadata
        """
        # Placeholder for global city search
        # In production, this would query:
        # - External APIs (Google Places, OpenStreetMap)
        # - Internal popular destinations database
        # - City metadata (cost index, popularity, weather)
        
        cities = [
            {
                'name': 'Dubai',
                'country': 'UAE',
                'cost_index': 85,
                'popularity': 95,
                'description': 'Luxury shopping and desert adventures'
            },
            {
                'name': 'Goa',
                'country': 'India',
                'cost_index': 35,
                'popularity': 80,
                'description': 'Beaches and night life'
            },
            {
                'name': 'Barcelona',
                'country': 'Spain',
                'cost_index': 65,
                'popularity': 90,
                'description': 'Architecture and Mediterranean beaches'
            }
        ]
        
        return [c for c in cities if query.lower() in c['name'].lower()]
    
    # ==================== DATA EXPORT & REPORTING ====================
    
    def get_itinerary_summary(self, trip_id: int) -> Dict:
        """Get a complete summary of the trip for sharing or export"""
        trip = self.get_trip(trip_id)
        if not trip:
            return {}
        
        stops = self.get_trip_stops(trip_id)
        activities = self.get_trip_activities(trip_id)
        
        return {
            'trip_id': trip.id,
            'title': trip.title,
            'description': trip.description,
            'duration': (trip.end_date - trip.start_date).days + 1,
            'budget': trip.budget,
            'stops_count': len(stops),
            'activities_count': len(activities),
            'stops': stops,
            'activities': activities,
            'itinerary': self.get_day_wise_itinerary(trip_id)
        }


# ==================== USAGE EXAMPLE ====================

if __name__ == "__main__":
    # Initialize engine
    engine = TripManagementEngine()
    
    # Example 1: Create a trip
    # user_id = 1  # Assuming user exists
    # trip = engine.create_trip(
    #     user_id=user_id,
    #     title="Europe Summer 2024",
    #     start_date=date(2024, 6, 1),
    #     end_date=date(2024, 6, 30),
    #     description="Amazing European adventure",
    #     budget=150000
    # )
    # print(f"Trip created: {trip}")
    
    # Example 2: Add cities to the trip
    # stop1 = engine.add_stop(trip.id, "Dubai", date(2024, 6, 1), date(2024, 6, 5))
    # stop2 = engine.add_stop(trip.id, "Barcelona", date(2024, 6, 6), date(2024, 6, 15))
    # stop3 = engine.add_stop(trip.id, "Paris", date(2024, 6, 16), date(2024, 6, 30))
    
    # Example 3: Add activities to stops
    # activity1 = engine.add_activity(trip.id, stop1.id, "Desert Safari", "adventure", cost=5000)
    # activity2 = engine.add_activity(trip.id, stop2.id, "Sagrada Familia Visit", "sightseeing", cost=3000)
    
    # Example 4: Get itinerary summary
    # summary = engine.get_itinerary_summary(trip.id)
    # print(summary)
    
    print("Trip Management Engine initialized successfully!")
