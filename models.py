"""
Traveloop - Travel Data Store - Relational Database Models
Using SQLAlchemy ORM for Python
Professional-grade travel management system with multi-city itineraries, budgeting, and social features
"""

from datetime import datetime
from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime, ForeignKey, Text, Enum, Date, Boolean, JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
import enum
import uuid

Base = declarative_base()

class User(Base):
    """Users Table - Stores user information"""
    __tablename__ = 'users'
    
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    phone = Column(String(15))
    address = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationship: One user can have many trips
    trips = relationship('Trip', back_populates='user', cascade='all, delete-orphan')
    
    def __repr__(self):
        return f"<User(id={self.id}, name='{self.name}', email='{self.email}')>"


class Trip(Base):
    """Trips Table - Stores individual trip information"""
    __tablename__ = 'trips'
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    title = Column(String(150), nullable=False)
    description = Column(Text)
    start_date = Column(Date, nullable=False)
    end_date = Column(Date, nullable=False)
    destination = Column(String(150), nullable=False)
    budget = Column(Float, default=0.0)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Foreign Key Relationship
    user = relationship('User', back_populates='trips')
    
    # Relationships: One trip can have many stops, activities, and expenses
    stops = relationship('Stop', back_populates='trip', cascade='all, delete-orphan')
    activities = relationship('Activity', back_populates='trip', cascade='all, delete-orphan')
    expenses = relationship('Expense', back_populates='trip', cascade='all, delete-orphan')
    
    def __repr__(self):
        return f"<Trip(id={self.id}, title='{self.title}', destination='{self.destination}')>"


class Stop(Base):
    """Stops Table - Stores stop/location information for each trip"""
    __tablename__ = 'stops'
    
    id = Column(Integer, primary_key=True)
    trip_id = Column(Integer, ForeignKey('trips.id'), nullable=False)
    location = Column(String(200), nullable=False)
    latitude = Column(Float)
    longitude = Column(Float)
    arrival_date = Column(Date, nullable=False)
    departure_date = Column(Date)
    notes = Column(Text)
    sequence_order = Column(Integer)  # To maintain order of stops
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Foreign Key Relationship
    trip = relationship('Trip', back_populates='stops')
    
    # One stop can have many activities
    activities = relationship('Activity', back_populates='stop', cascade='all, delete-orphan')
    
    def __repr__(self):
        return f"<Stop(id={self.id}, location='{self.location}', trip_id={self.trip_id})>"


class Activity(Base):
    """Activities Table - Stores activities information"""
    __tablename__ = 'activities'
    
    id = Column(Integer, primary_key=True)
    trip_id = Column(Integer, ForeignKey('trips.id'), nullable=False)
    stop_id = Column(Integer, ForeignKey('stops.id'), nullable=True)  # Optional: can be associated with a stop
    name = Column(String(150), nullable=False)
    description = Column(Text)
    activity_type = Column(String(50))  # e.g., 'hiking', 'sightseeing', 'dining', etc.
    start_time = Column(DateTime)
    end_time = Column(DateTime)
    cost = Column(Float, default=0.0)
    status = Column(String(20), default='planned')  # planned, completed, cancelled
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Foreign Key Relationships
    trip = relationship('Trip', back_populates='activities')
    stop = relationship('Stop', back_populates='activities')
    
    def __repr__(self):
        return f"<Activity(id={self.id}, name='{self.name}', trip_id={self.trip_id})>"


class Expense(Base):
    """Expenses Table - Stores expense information"""
    __tablename__ = 'expenses'
    
    id = Column(Integer, primary_key=True)
    trip_id = Column(Integer, ForeignKey('trips.id'), nullable=False)
    description = Column(String(200), nullable=False)
    amount = Column(Float, nullable=False)
    category = Column(String(50), nullable=False)  # e.g., 'accommodation', 'food', 'transport', 'activities'
    expense_date = Column(Date, nullable=False)
    payment_method = Column(String(50))  # e.g., 'cash', 'card', 'online'
    status = Column(String(20), default='pending')  # pending, paid, reimbursed
    paid_by = Column(String(100))  # Name of person who paid
    notes = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Foreign Key Relationship
    trip = relationship('Trip', back_populates='expenses')
    
    def __repr__(self):
        return f"<Expense(id={self.id}, description='{self.description}', amount={self.amount}, category='{self.category}')>"


# ==================== ENHANCED MODELS FOR PROFESSIONAL FEATURES ====================

class SharedTrip(Base):
    """Shared Trips Table - Public sharing and collaborative features"""
    __tablename__ = 'shared_trips'
    
    id = Column(Integer, primary_key=True)
    trip_id = Column(Integer, ForeignKey('trips.id'), nullable=False)
    share_token = Column(String(100), unique=True, nullable=False, default=lambda: str(uuid.uuid4()))  # Unique public URL token
    shared_by = Column(Integer, ForeignKey('users.id'), nullable=False)  # User who shared
    is_public = Column(Boolean, default=True)
    copy_count = Column(Integer, default=0)  # Track how many times this trip was copied
    shared_on = Column(DateTime, default=datetime.utcnow)
    expires_at = Column(DateTime, nullable=True)  # Optional expiration date
    
    trip = relationship('Trip')
    
    def get_public_url(self):
        """Generate public sharing URL"""
        return f"https://traveloop.app/trips/{self.share_token}"


class PackingChecklist(Base):
    """Packing Checklist Table - Pre-trip preparation"""
    __tablename__ = 'packing_checklists'
    
    id = Column(Integer, primary_key=True)
    trip_id = Column(Integer, ForeignKey('trips.id'), nullable=False)
    category = Column(String(50), nullable=False)  # clothing, electronics, documents, toiletries
    item = Column(String(200), nullable=False)
    is_packed = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    trip = relationship('Trip')


class TripNote(Base):
    """Trip Notes Table - Digital journal for trip-specific info"""
    __tablename__ = 'trip_notes'
    
    id = Column(Integer, primary_key=True)
    trip_id = Column(Integer, ForeignKey('trips.id'), nullable=False)
    note_type = Column(String(50), nullable=False)  # hotel_info, local_contact, general_note, reminder
    title = Column(String(150), nullable=False)
    content = Column(Text, nullable=False)
    associated_stop_id = Column(Integer, ForeignKey('stops.id'), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    trip = relationship('Trip')
    stop = relationship('Stop')


class BudgetBreakdown(Base):
    """Budget Breakdown Table - Financial intelligence and analytics"""
    __tablename__ = 'budget_breakdowns'
    
    id = Column(Integer, primary_key=True)
    trip_id = Column(Integer, ForeignKey('trips.id'), nullable=False)
    category = Column(String(50), nullable=False)  # transport, accommodation, activities, food, miscellaneous
    planned_budget = Column(Float, default=0.0)
    actual_spent = Column(Float, default=0.0)
    alert_threshold = Column(Float)  # Percentage limit for spending
    last_updated = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    trip = relationship('Trip')


class UserProfile(Base):
    """Enhanced User Profile Table - Language and preference settings"""
    __tablename__ = 'user_profiles'
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False, unique=True)
    language = Column(String(10), default='en')  # en, hi, etc.
    theme = Column(String(20), default='light')  # light or dark
    preferred_currency = Column(String(10), default='INR')
    two_factor_auth = Column(Boolean, default=False)
    newsletter_subscription = Column(Boolean, default=True)
    profile_photo_url = Column(String(500))
    bio = Column(Text)
    preferences = Column(JSON)  # Additional preferences as JSON
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    user = relationship('User')


class AnalyticsEvent(Base):
    """Analytics Events Table - Platform usage tracking for admin dashboard"""
    __tablename__ = 'analytics_events'
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=True)
    event_type = Column(String(50), nullable=False)  # trip_created, trip_viewed, trip_shared, budget_updated
    event_data = Column(JSON)  # Additional event details
    timestamp = Column(DateTime, default=datetime.utcnow)


class PopularDestination(Base):
    """Popular Destinations Table - Trending cities and insights"""
    __tablename__ = 'popular_destinations'
    
    id = Column(Integer, primary_key=True)
    city_name = Column(String(100), unique=True, nullable=False)
    country = Column(String(100))
    trip_count = Column(Integer, default=0)  # How many trips include this city
    average_cost_index = Column(Float)  # Average cost per day
    popularity_score = Column(Float, default=0.0)  # Calculate based on usage
    description = Column(Text)
    image_url = Column(String(500))
    last_updated = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


# ==================== DATABASE INITIALIZATION ====================

def create_database(database_url='sqlite:///travel_database.db'):
    """
    Create database and initialize tables
    
    Parameters:
    - database_url: Connection string (default: SQLite local file)
      Examples:
        - 'sqlite:///travel_database.db' (SQLite)
        - 'postgresql://user:password@localhost/travel_db' (PostgreSQL)
        - 'mysql+pymysql://user:password@localhost/travel_db' (MySQL)
    """
    engine = create_engine(database_url, echo=True)
    Base.metadata.create_all(engine)
    return engine


def get_session(database_url='sqlite:///travel_database.db'):
    """Get a database session"""
    engine = create_engine(database_url)
    Session = sessionmaker(bind=engine)
    return Session()
    return engine


def get_session(engine):
    """Create a session for database operations"""
    Session = sessionmaker(bind=engine)
    return Session()


if __name__ == '__main__':
    # Initialize database
    engine = create_database()
    session = get_session(engine)
    
    print("✓ Database tables created successfully!")
    print("\nAvailable Models:")
    print("  - User (Users)")
    print("  - Trip (Trips)")
    print("  - Stop (Stops)")
    print("  - Activity (Activities)")
    print("  - Expense (Expenses)")
