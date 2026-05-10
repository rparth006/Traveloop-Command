"""
Travel Database - Extended Models with City Data, Activities, Packing, and Authentication
"""

from datetime import datetime
from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime, ForeignKey, Text, Enum, Date, Boolean, UniqueConstraint
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
import enum
import uuid
import hashlib

Base = declarative_base()

# ===================== EXISTING MODELS (from models.py) =====================

class User(Base):
    """Users Table - Stores user information"""
    __tablename__ = 'users'
    
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    password_hash = Column(String(255))  # For authentication
    phone = Column(String(15))
    address = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    trips = relationship('Trip', back_populates='user', cascade='all, delete-orphan')
    packing_checklists = relationship('PackingChecklist', back_populates='user', cascade='all, delete-orphan')
    
    def set_password(self, password):
        """Hash and set password"""
        self.password_hash = hashlib.sha256(password.encode()).hexdigest()
    
    def check_password(self, password):
        """Verify password"""
        return self.password_hash == hashlib.sha256(password.encode()).hexdigest()
    
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
    public_url = Column(String(100), unique=True, nullable=True)  # For sharing
    is_public = Column(Boolean, default=False)  # Public sharing flag
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    user = relationship('User', back_populates='trips')
    stops = relationship('Stop', back_populates='trip', cascade='all, delete-orphan')
    activities = relationship('Activity', back_populates='trip', cascade='all, delete-orphan')
    expenses = relationship('Expense', back_populates='trip', cascade='all, delete-orphan')
    packing_items = relationship('TripPackingItem', back_populates='trip', cascade='all, delete-orphan')
    shared_trip = relationship('SharedTrip', back_populates='trip', cascade='all, delete-orphan', uselist=False)
    
    def generate_public_url(self):
        """Generate a unique public URL for sharing"""
        unique_code = str(uuid.uuid4())[:8].upper()
        self.public_url = unique_code
        self.is_public = True
        return unique_code
    
    def __repr__(self):
        return f"<Trip(id={self.id}, title='{self.title}', destination='{self.destination}')>"


class Stop(Base):
    """Stops Table - Stores stop/location information"""
    __tablename__ = 'stops'
    
    id = Column(Integer, primary_key=True)
    trip_id = Column(Integer, ForeignKey('trips.id'), nullable=False)
    location = Column(String(200), nullable=False)
    city_id = Column(Integer, ForeignKey('cities.id'), nullable=True)  # Link to cities catalog
    latitude = Column(Float)
    longitude = Column(Float)
    arrival_date = Column(Date, nullable=False)
    departure_date = Column(Date)
    notes = Column(Text)
    sequence_order = Column(Integer)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    trip = relationship('Trip', back_populates='stops')
    city = relationship('City', back_populates='stops')
    activities = relationship('Activity', back_populates='stop', cascade='all, delete-orphan')
    
    def __repr__(self):
        return f"<Stop(id={self.id}, location='{self.location}', trip_id={self.trip_id})>"


class Activity(Base):
    """Activities Table - Stores activities information"""
    __tablename__ = 'activities'
    
    id = Column(Integer, primary_key=True)
    trip_id = Column(Integer, ForeignKey('trips.id'), nullable=False)
    stop_id = Column(Integer, ForeignKey('stops.id'), nullable=True)
    activity_type_id = Column(Integer, ForeignKey('activity_types.id'), nullable=True)  # Link to activity types
    name = Column(String(150), nullable=False)
    description = Column(Text)
    start_time = Column(DateTime)
    end_time = Column(DateTime)
    cost = Column(Float, default=0.0)
    status = Column(String(20), default='planned')
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    trip = relationship('Trip', back_populates='activities')
    stop = relationship('Stop', back_populates='activities')
    activity_type = relationship('ActivityType', back_populates='activities')
    
    def __repr__(self):
        return f"<Activity(id={self.id}, name='{self.name}', trip_id={self.trip_id})>"


class Expense(Base):
    """Expenses Table - Stores expense information"""
    __tablename__ = 'expenses'
    
    id = Column(Integer, primary_key=True)
    trip_id = Column(Integer, ForeignKey('trips.id'), nullable=False)
    description = Column(String(200), nullable=False)
    amount = Column(Float, nullable=False)
    category = Column(String(50), nullable=False)
    expense_date = Column(Date, nullable=False)
    payment_method = Column(String(50))
    status = Column(String(20), default='pending')
    paid_by = Column(String(100))
    notes = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationship
    trip = relationship('Trip', back_populates='expenses')
    
    def __repr__(self):
        return f"<Expense(id={self.id}, description='{self.description}', amount={self.amount})>"


# ===================== NEW MODELS FOR DATA ENRICHMENT =====================

class City(Base):
    """Cities Catalog - Popular cities with cost information"""
    __tablename__ = 'cities'
    
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    country = Column(String(100), nullable=False)
    continent = Column(String(50))
    description = Column(Text)
    latitude = Column(Float)
    longitude = Column(Float)
    cost_index = Column(Float, default=1.0)  # Relative cost (1.0 = baseline)
    currency = Column(String(10), default='USD')
    best_time_to_visit = Column(String(100))
    population = Column(Integer)
    image_url = Column(String(255))
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    stops = relationship('Stop', back_populates='city')
    recommended_activities = relationship('CityActivity', back_populates='city', cascade='all, delete-orphan')
    
    __table_args__ = (UniqueConstraint('name', 'country', name='uq_city_country'),)
    
    def __repr__(self):
        return f"<City(id={self.id}, name='{self.name}', country='{self.country}')>"


class ActivityType(Base):
    """Activity Types Catalog - Different activity categories"""
    __tablename__ = 'activity_types'
    
    id = Column(Integer, primary_key=True)
    name = Column(String(50), unique=True, nullable=False)
    description = Column(Text)
    icon = Column(String(50))
    estimated_cost_min = Column(Float)
    estimated_cost_max = Column(Float)
    average_duration_hours = Column(Float)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    activities = relationship('Activity', back_populates='activity_type')
    city_activities = relationship('CityActivity', back_populates='activity_type')
    
    def __repr__(self):
        return f"<ActivityType(id={self.id}, name='{self.name}')>"


class CityActivity(Base):
    """City Activities - What to do in each city"""
    __tablename__ = 'city_activities'
    
    id = Column(Integer, primary_key=True)
    city_id = Column(Integer, ForeignKey('cities.id'), nullable=False)
    activity_type_id = Column(Integer, ForeignKey('activity_types.id'), nullable=False)
    name = Column(String(150), nullable=False)
    description = Column(Text)
    estimated_cost = Column(Float)  # Estimated cost in local currency
    cost_in_usd = Column(Float)  # Standardized cost
    duration_hours = Column(Float)
    best_time = Column(String(100))
    ratings = Column(Float, default=0.0)  # 0-5 stars
    popularity = Column(Integer, default=0)  # Popularity score
    image_url = Column(String(255))
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    city = relationship('City', back_populates='recommended_activities')
    activity_type = relationship('ActivityType', back_populates='city_activities')
    
    def __repr__(self):
        return f"<CityActivity(id={self.id}, name='{self.name}', city_id={self.city_id})>"


class PackingItem(Base):
    """Packing Items Catalog - Default packing list items"""
    __tablename__ = 'packing_items'
    
    id = Column(Integer, primary_key=True)
    category = Column(String(50), nullable=False)  # clothing, electronics, documents, toiletries, etc.
    name = Column(String(100), nullable=False)
    description = Column(Text)
    priority = Column(String(20), default='medium')  # essential, important, optional
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    packing_checklists = relationship('PackingChecklistItem', back_populates='item')
    
    __table_args__ = (UniqueConstraint('category', 'name', name='uq_packing_item'),)
    
    def __repr__(self):
        return f"<PackingItem(id={self.id}, name='{self.name}', category='{self.category}')>"


class PackingChecklist(Base):
    """Packing Checklist - User's packing list for a trip"""
    __tablename__ = 'packing_checklists'
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    trip_id = Column(Integer, ForeignKey('trips.id'), nullable=True)
    name = Column(String(100), nullable=False)
    description = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    user = relationship('User', back_populates='packing_checklists')
    items = relationship('PackingChecklistItem', back_populates='checklist', cascade='all, delete-orphan')
    
    def __repr__(self):
        return f"<PackingChecklist(id={self.id}, name='{self.name}', user_id={self.user_id})>"


class PackingChecklistItem(Base):
    """Packing Checklist Items - Items in a packing list"""
    __tablename__ = 'packing_checklist_items'
    
    id = Column(Integer, primary_key=True)
    checklist_id = Column(Integer, ForeignKey('packing_checklists.id'), nullable=False)
    packing_item_id = Column(Integer, ForeignKey('packing_items.id'), nullable=True)
    name = Column(String(100), nullable=False)  # Can override default name
    category = Column(String(50))
    quantity = Column(Integer, default=1)
    is_packed = Column(Boolean, default=False)
    notes = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    checklist = relationship('PackingChecklist', back_populates='items')
    item = relationship('PackingItem', back_populates='packing_checklists')
    
    def __repr__(self):
        return f"<PackingChecklistItem(id={self.id}, name='{self.name}', is_packed={self.is_packed})>"


class TripPackingItem(Base):
    """Trip Packing Items - Quick link between trips and packing items"""
    __tablename__ = 'trip_packing_items'
    
    id = Column(Integer, primary_key=True)
    trip_id = Column(Integer, ForeignKey('trips.id'), nullable=False)
    checklist_id = Column(Integer, ForeignKey('packing_checklists.id'), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    trip = relationship('Trip', back_populates='packing_items')
    
    def __repr__(self):
        return f"<TripPackingItem(trip_id={self.trip_id}, checklist_id={self.checklist_id})>"


class SharedTrip(Base):
    """Shared Trips - Public sharing information for trips"""
    __tablename__ = 'shared_trips'
    
    id = Column(Integer, primary_key=True)
    trip_id = Column(Integer, ForeignKey('trips.id'), nullable=False, unique=True)
    public_url = Column(String(100), unique=True, nullable=False)
    shared_by_user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    shared_at = Column(DateTime, default=datetime.utcnow)
    expires_at = Column(DateTime, nullable=True)  # Optional expiration
    view_count = Column(Integer, default=0)
    is_active = Column(Boolean, default=True)
    can_edit = Column(Boolean, default=False)  # Allow viewers to edit
    password_protected = Column(Boolean, default=False)
    password_hash = Column(String(255), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    trip = relationship('Trip', back_populates='shared_trip')
    shared_by = relationship('User')
    
    def set_password(self, password):
        """Hash and set password"""
        if password:
            self.password_hash = hashlib.sha256(password.encode()).hexdigest()
            self.password_protected = True
    
    def check_password(self, password):
        """Verify password"""
        if not self.password_protected:
            return True
        return self.password_hash == hashlib.sha256(password.encode()).hexdigest()
    
    def __repr__(self):
        return f"<SharedTrip(id={self.id}, trip_id={self.trip_id}, public_url='{self.public_url}')>"


# ===================== DATABASE INITIALIZATION =====================

def create_database(database_url='sqlite:///travel_database.db'):
    """
    Create database and initialize tables
    
    Parameters:
    - database_url: Connection string (default: SQLite local file)
    """
    engine = create_engine(database_url, echo=False)
    Base.metadata.create_all(engine)
    return engine


def get_session(engine):
    """Create a session for database operations"""
    Session = sessionmaker(bind=engine)
    return Session()


if __name__ == '__main__':
    # Initialize database
    engine = create_database()
    
    print("✓ Database tables created successfully!")
    print("\nAvailable Models:")
    print("  ========== CORE MODELS ==========")
    print("  - User (Users)")
    print("  - Trip (Trips)")
    print("  - Stop (Stops)")
    print("  - Activity (Activities)")
    print("  - Expense (Expenses)")
    print()
    print("  ========== NEW DATA MODELS ==========")
    print("  - City (Popular cities catalog)")
    print("  - ActivityType (Activity categories)")
    print("  - CityActivity (What to do in each city)")
    print("  - PackingItem (Default packing items)")
    print("  - PackingChecklist (User packing lists)")
    print("  - PackingChecklistItem (Items in packing list)")
    print("  - TripPackingItem (Trip packing links)")
    print("  - SharedTrip (Public trip sharing)")
    print()
    print("✓ Database ready for use!")
