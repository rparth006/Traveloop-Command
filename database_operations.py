"""
Travel Database - Helper Functions for Common Operations
"""

from models import User, Trip, Stop, Activity, Expense, get_session, create_database
from datetime import date, datetime
from typing import List, Dict, Optional

class TravelDatabaseHelper:
    """Helper class for common travel database operations"""
    
    def __init__(self, database_url='sqlite:///travel_database.db'):
        """Initialize database connection"""
        self.engine = create_database(database_url)
        self.session = get_session(self.engine)
    
    # ===================== USER OPERATIONS =====================
    
    def create_user(self, name: str, email: str, phone: str = None, address: str = None) -> User:
        """Create a new user"""
        user = User(name=name, email=email, phone=phone, address=address)
        self.session.add(user)
        self.session.commit()
        return user
    
    def get_user(self, user_id: int) -> Optional[User]:
        """Get user by ID"""
        return self.session.query(User).filter_by(id=user_id).first()
    
    def get_user_by_email(self, email: str) -> Optional[User]:
        """Get user by email"""
        return self.session.query(User).filter_by(email=email).first()
    
    def get_all_users(self) -> List[User]:
        """Get all users"""
        return self.session.query(User).all()
    
    def update_user(self, user_id: int, **kwargs) -> User:
        """Update user information"""
        user = self.get_user(user_id)
        if user:
            for key, value in kwargs.items():
                if hasattr(user, key):
                    setattr(user, key, value)
            self.session.commit()
        return user
    
    def delete_user(self, user_id: int) -> bool:
        """Delete user and all associated data"""
        user = self.get_user(user_id)
        if user:
            self.session.delete(user)
            self.session.commit()
            return True
        return False
    
    # ===================== TRIP OPERATIONS =====================
    
    def create_trip(self, user_id: int, title: str, destination: str,
                   start_date: date, end_date: date, description: str = None,
                   budget: float = 0.0) -> Trip:
        """Create a new trip"""
        trip = Trip(
            user_id=user_id,
            title=title,
            destination=destination,
            start_date=start_date,
            end_date=end_date,
            description=description,
            budget=budget
        )
        self.session.add(trip)
        self.session.commit()
        return trip
    
    def get_trip(self, trip_id: int) -> Optional[Trip]:
        """Get trip by ID"""
        return self.session.query(Trip).filter_by(id=trip_id).first()
    
    def get_user_trips(self, user_id: int) -> List[Trip]:
        """Get all trips for a user"""
        user = self.get_user(user_id)
        return user.trips if user else []
    
    def get_trips_by_destination(self, destination: str) -> List[Trip]:
        """Get all trips to a destination"""
        return self.session.query(Trip).filter_by(destination=destination).all()
    
    def update_trip(self, trip_id: int, **kwargs) -> Trip:
        """Update trip information"""
        trip = self.get_trip(trip_id)
        if trip:
            for key, value in kwargs.items():
                if hasattr(trip, key):
                    setattr(trip, key, value)
            self.session.commit()
        return trip
    
    def delete_trip(self, trip_id: int) -> bool:
        """Delete trip and all associated data"""
        trip = self.get_trip(trip_id)
        if trip:
            self.session.delete(trip)
            self.session.commit()
            return True
        return False
    
    # ===================== STOP OPERATIONS =====================
    
    def create_stop(self, trip_id: int, location: str, arrival_date: date,
                   departure_date: date = None, latitude: float = None,
                   longitude: float = None, notes: str = None,
                   sequence_order: int = None) -> Stop:
        """Create a new stop for a trip"""
        stop = Stop(
            trip_id=trip_id,
            location=location,
            arrival_date=arrival_date,
            departure_date=departure_date,
            latitude=latitude,
            longitude=longitude,
            notes=notes,
            sequence_order=sequence_order
        )
        self.session.add(stop)
        self.session.commit()
        return stop
    
    def get_stop(self, stop_id: int) -> Optional[Stop]:
        """Get stop by ID"""
        return self.session.query(Stop).filter_by(id=stop_id).first()
    
    def get_trip_stops(self, trip_id: int, ordered: bool = False) -> List[Stop]:
        """Get all stops for a trip"""
        trip = self.get_trip(trip_id)
        if trip:
            stops = trip.stops
            if ordered:
                stops = sorted(stops, key=lambda x: x.sequence_order or 0)
            return stops
        return []
    
    def update_stop(self, stop_id: int, **kwargs) -> Stop:
        """Update stop information"""
        stop = self.get_stop(stop_id)
        if stop:
            for key, value in kwargs.items():
                if hasattr(stop, key):
                    setattr(stop, key, value)
            self.session.commit()
        return stop
    
    def delete_stop(self, stop_id: int) -> bool:
        """Delete stop"""
        stop = self.get_stop(stop_id)
        if stop:
            self.session.delete(stop)
            self.session.commit()
            return True
        return False
    
    # ===================== ACTIVITY OPERATIONS =====================
    
    def create_activity(self, trip_id: int, name: str, activity_type: str,
                       stop_id: int = None, description: str = None,
                       start_time: datetime = None, end_time: datetime = None,
                       cost: float = 0.0, status: str = 'planned') -> Activity:
        """Create a new activity"""
        activity = Activity(
            trip_id=trip_id,
            stop_id=stop_id,
            name=name,
            description=description,
            activity_type=activity_type,
            start_time=start_time,
            end_time=end_time,
            cost=cost,
            status=status
        )
        self.session.add(activity)
        self.session.commit()
        return activity
    
    def get_activity(self, activity_id: int) -> Optional[Activity]:
        """Get activity by ID"""
        return self.session.query(Activity).filter_by(id=activity_id).first()
    
    def get_trip_activities(self, trip_id: int) -> List[Activity]:
        """Get all activities for a trip"""
        trip = self.get_trip(trip_id)
        return trip.activities if trip else []
    
    def get_stop_activities(self, stop_id: int) -> List[Activity]:
        """Get all activities for a stop"""
        stop = self.get_stop(stop_id)
        return stop.activities if stop else []
    
    def get_activities_by_type(self, trip_id: int, activity_type: str) -> List[Activity]:
        """Get activities of a specific type"""
        return self.session.query(Activity).filter_by(
            trip_id=trip_id,
            activity_type=activity_type
        ).all()
    
    def get_activities_by_status(self, trip_id: int, status: str) -> List[Activity]:
        """Get activities with specific status"""
        return self.session.query(Activity).filter_by(
            trip_id=trip_id,
            status=status
        ).all()
    
    def update_activity(self, activity_id: int, **kwargs) -> Activity:
        """Update activity information"""
        activity = self.get_activity(activity_id)
        if activity:
            for key, value in kwargs.items():
                if hasattr(activity, key):
                    setattr(activity, key, value)
            self.session.commit()
        return activity
    
    def delete_activity(self, activity_id: int) -> bool:
        """Delete activity"""
        activity = self.get_activity(activity_id)
        if activity:
            self.session.delete(activity)
            self.session.commit()
            return True
        return False
    
    # ===================== EXPENSE OPERATIONS =====================
    
    def create_expense(self, trip_id: int, description: str, amount: float,
                      category: str, expense_date: date, payment_method: str = None,
                      status: str = 'pending', paid_by: str = None,
                      notes: str = None) -> Expense:
        """Create a new expense"""
        expense = Expense(
            trip_id=trip_id,
            description=description,
            amount=amount,
            category=category,
            expense_date=expense_date,
            payment_method=payment_method,
            status=status,
            paid_by=paid_by,
            notes=notes
        )
        self.session.add(expense)
        self.session.commit()
        return expense
    
    def get_expense(self, expense_id: int) -> Optional[Expense]:
        """Get expense by ID"""
        return self.session.query(Expense).filter_by(id=expense_id).first()
    
    def get_trip_expenses(self, trip_id: int) -> List[Expense]:
        """Get all expenses for a trip"""
        trip = self.get_trip(trip_id)
        return trip.expenses if trip else []
    
    def get_expenses_by_category(self, trip_id: int, category: str) -> List[Expense]:
        """Get expenses of a specific category"""
        return self.session.query(Expense).filter_by(
            trip_id=trip_id,
            category=category
        ).all()
    
    def get_expenses_by_status(self, trip_id: int, status: str) -> List[Expense]:
        """Get expenses with specific status"""
        return self.session.query(Expense).filter_by(
            trip_id=trip_id,
            status=status
        ).all()
    
    def update_expense(self, expense_id: int, **kwargs) -> Expense:
        """Update expense information"""
        expense = self.get_expense(expense_id)
        if expense:
            for key, value in kwargs.items():
                if hasattr(expense, key):
                    setattr(expense, key, value)
            self.session.commit()
        return expense
    
    def delete_expense(self, expense_id: int) -> bool:
        """Delete expense"""
        expense = self.get_expense(expense_id)
        if expense:
            self.session.delete(expense)
            self.session.commit()
            return True
        return False
    
    # ===================== ANALYTICS & REPORTS =====================
    
    def get_trip_cost_analysis(self, trip_id: int) -> Dict:
        """Get detailed cost analysis for a trip"""
        trip = self.get_trip(trip_id)
        if not trip:
            return {}
        
        expenses = trip.expenses
        total_expenses = sum(e.amount for e in expenses)
        remaining = trip.budget - total_expenses
        
        expenses_by_category = {}
        for expense in expenses:
            expenses_by_category.setdefault(expense.category, 0)
            expenses_by_category[expense.category] += expense.amount
        
        return {
            'trip_id': trip.id,
            'title': trip.title,
            'budget': trip.budget,
            'total_expenses': total_expenses,
            'remaining': remaining,
            'percentage_used': (total_expenses / trip.budget * 100) if trip.budget > 0 else 0,
            'by_category': expenses_by_category,
            'expense_count': len(expenses)
        }
    
    def get_trip_itinerary(self, trip_id: int) -> Dict:
        """Get complete trip itinerary"""
        trip = self.get_trip(trip_id)
        if not trip:
            return {}
        
        stops = sorted(trip.stops, key=lambda x: x.sequence_order or 0)
        
        itinerary = {
            'trip_id': trip.id,
            'title': trip.title,
            'destination': trip.destination,
            'start_date': trip.start_date,
            'end_date': trip.end_date,
            'stops': []
        }
        
        for stop in stops:
            stop_data = {
                'location': stop.location,
                'arrival': stop.arrival_date,
                'departure': stop.departure_date,
                'activities': [
                    {
                        'name': a.name,
                        'type': a.activity_type,
                        'cost': a.cost,
                        'status': a.status
                    } for a in stop.activities
                ]
            }
            itinerary['stops'].append(stop_data)
        
        return itinerary
    
    def get_user_stats(self, user_id: int) -> Dict:
        """Get statistics for a user"""
        user = self.get_user(user_id)
        if not user:
            return {}
        
        trips = user.trips
        total_trips = len(trips)
        total_budget = sum(t.budget for t in trips)
        total_spent = sum(sum(e.amount for e in t.expenses) for t in trips)
        total_activities = sum(len(t.activities) for t in trips)
        total_stops = sum(len(t.stops) for t in trips)
        
        return {
            'user_id': user.id,
            'name': user.name,
            'email': user.email,
            'total_trips': total_trips,
            'total_budget': total_budget,
            'total_spent': total_spent,
            'total_activities': total_activities,
            'total_stops': total_stops,
            'average_trip_budget': (total_budget / total_trips) if total_trips > 0 else 0
        }
    
    def get_expense_summary(self, trip_id: int) -> Dict:
        """Get expense summary by category and status"""
        expenses = self.get_trip_expenses(trip_id)
        
        by_category = {}
        by_status = {}
        
        for expense in expenses:
            # By category
            by_category.setdefault(expense.category, {
                'count': 0,
                'amount': 0.0
            })
            by_category[expense.category]['count'] += 1
            by_category[expense.category]['amount'] += expense.amount
            
            # By status
            by_status.setdefault(expense.status, {
                'count': 0,
                'amount': 0.0
            })
            by_status[expense.status]['count'] += 1
            by_status[expense.status]['amount'] += expense.amount
        
        return {
            'by_category': by_category,
            'by_status': by_status,
            'total_expenses': len(expenses),
            'total_amount': sum(e.amount for e in expenses)
        }
    
    def close(self):
        """Close database session"""
        self.session.close()


# Usage Example
if __name__ == '__main__':
    # Initialize helper
    db = TravelDatabaseHelper()
    
    print("✓ Travel Database Helper Initialized")
    print("\nAvailable Operations:")
    print("  - User Operations: create, get, update, delete")
    print("  - Trip Operations: create, get, update, delete")
    print("  - Stop Operations: create, get, update, delete")
    print("  - Activity Operations: create, get, update, delete")
    print("  - Expense Operations: create, get, update, delete")
    print("  - Analytics: cost analysis, itinerary, statistics, summaries")
    
    db.close()
