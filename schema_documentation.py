"""
Travel Database - SQL Schema Documentation
"""

# SQL Schema for Travel Data Store

SQL_SCHEMA = """
-- Users Table
CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    phone VARCHAR(15),
    address TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_email (email)
);

-- Trips Table
CREATE TABLE trips (
    id INTEGER PRIMARY KEY AUTO_INCREMENT,
    user_id INTEGER NOT NULL,
    title VARCHAR(150) NOT NULL,
    description TEXT,
    start_date DATE NOT NULL,
    end_date DATE NOT NULL,
    destination VARCHAR(150) NOT NULL,
    budget FLOAT DEFAULT 0.0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    INDEX idx_user_id (user_id),
    INDEX idx_destination (destination)
);

-- Stops Table (One Trip → Many Stops)
CREATE TABLE stops (
    id INTEGER PRIMARY KEY AUTO_INCREMENT,
    trip_id INTEGER NOT NULL,
    location VARCHAR(200) NOT NULL,
    latitude FLOAT,
    longitude FLOAT,
    arrival_date DATE NOT NULL,
    departure_date DATE,
    notes TEXT,
    sequence_order INTEGER,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (trip_id) REFERENCES trips(id) ON DELETE CASCADE,
    INDEX idx_trip_id (trip_id),
    INDEX idx_sequence (trip_id, sequence_order)
);

-- Activities Table (One Trip → Many Activities, One Stop → Many Activities)
CREATE TABLE activities (
    id INTEGER PRIMARY KEY AUTO_INCREMENT,
    trip_id INTEGER NOT NULL,
    stop_id INTEGER,
    name VARCHAR(150) NOT NULL,
    description TEXT,
    activity_type VARCHAR(50),
    start_time DATETIME,
    end_time DATETIME,
    cost FLOAT DEFAULT 0.0,
    status VARCHAR(20) DEFAULT 'planned',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (trip_id) REFERENCES trips(id) ON DELETE CASCADE,
    FOREIGN KEY (stop_id) REFERENCES stops(id) ON DELETE SET NULL,
    INDEX idx_trip_id (trip_id),
    INDEX idx_stop_id (stop_id),
    INDEX idx_activity_type (activity_type),
    INDEX idx_status (status)
);

-- Expenses Table (One Trip → Many Expenses)
CREATE TABLE expenses (
    id INTEGER PRIMARY KEY AUTO_INCREMENT,
    trip_id INTEGER NOT NULL,
    description VARCHAR(200) NOT NULL,
    amount FLOAT NOT NULL,
    category VARCHAR(50) NOT NULL,
    expense_date DATE NOT NULL,
    payment_method VARCHAR(50),
    status VARCHAR(20) DEFAULT 'pending',
    paid_by VARCHAR(100),
    notes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (trip_id) REFERENCES trips(id) ON DELETE CASCADE,
    INDEX idx_trip_id (trip_id),
    INDEX idx_category (category),
    INDEX idx_expense_date (expense_date),
    INDEX idx_status (status)
);
"""

# Database Relationships Documentation
RELATIONSHIPS = """
╔════════════════════════════════════════════════════════════════════╗
║         TRAVEL DATABASE - RELATIONAL STRUCTURE & FLOWS            ║
╚════════════════════════════════════════════════════════════════════╝

1. USER → TRIP RELATIONSHIP (One-to-Many)
   ┌──────────────────┐
   │    USERS         │
   ├──────────────────┤
   │ id (PK)          │
   │ name             │
   │ email (UNIQUE)   │
   │ phone            │
   │ address          │
   └──────────────────┘
          │
          │ (1 User can have many Trips)
          │
          ▼
   ┌──────────────────┐
   │    TRIPS         │
   ├──────────────────┤
   │ id (PK)          │
   │ user_id (FK) ◄───┼─── References Users(id)
   │ title            │
   │ destination      │
   │ start_date       │
   │ end_date         │
   │ budget           │
   └──────────────────┘


2. TRIP → STOPS RELATIONSHIP (One-to-Many)
   ┌──────────────────┐
   │    TRIPS         │
   ├──────────────────┤
   │ id (PK)          │
   └──────────────────┘
          │
          │ (1 Trip can have multiple Stops)
          │
          ▼
   ┌──────────────────┐
   │    STOPS         │
   ├──────────────────┤
   │ id (PK)          │
   │ trip_id (FK) ◄───┼─── References Trips(id)
   │ location         │
   │ latitude         │
   │ longitude        │
   │ arrival_date     │
   │ departure_date   │
   │ sequence_order   │
   └──────────────────┘


3. TRIP → ACTIVITIES RELATIONSHIP (One-to-Many)
4. STOP → ACTIVITIES RELATIONSHIP (One-to-Many, Optional)
   ┌──────────────────┐
   │    TRIPS         │
   ├──────────────────┤
   │ id (PK)          │
   └──────────────────┘
          │
          │ (1 Trip can have many Activities)
          │
          ▼
   ┌──────────────────────┐           ┌──────────────────┐
   │   ACTIVITIES         │           │    STOPS         │
   ├──────────────────────┤           ├──────────────────┤
   │ id (PK)              │           │ id (PK)          │
   │ trip_id (FK) ◄───────┼───────┐───┼ references       │
   │ stop_id (FK, optional)◄──────┼───┼ Trips(id)        │
   │ name                 │       │   └──────────────────┘
   │ activity_type        │       │
   │ cost                 │       └─── Can be assigned to
   │ status               │            one Stop per Activity
   └──────────────────────┘


5. TRIP → EXPENSES RELATIONSHIP (One-to-Many)
   ┌──────────────────┐
   │    TRIPS         │
   ├──────────────────┤
   │ id (PK)          │
   └──────────────────┘
          │
          │ (1 Trip can have many Expenses)
          │
          ▼
   ┌──────────────────┐
   │   EXPENSES       │
   ├──────────────────┤
   │ id (PK)          │
   │ trip_id (FK) ◄───┼─── References Trips(id)
   │ description      │
   │ amount           │
   │ category         │
   │ expense_date     │
   │ payment_method   │
   │ status           │
   └──────────────────┘


COMPLETE ENTITY RELATIONSHIP DIAGRAM (ERD):
═════════════════════════════════════════════

                          ┌─────────────────────┐
                          │      USERS          │
                          ├─────────────────────┤
                          │ • id (PK)           │
                          │ • name              │
                          │ • email (UNIQUE)    │
                          │ • phone             │
                          │ • address           │
                          └──────────┬──────────┘
                                     │
                            1 : Many │
                                     │
                    ┌────────────────▼────────────────┐
                    │        TRIPS (1:N with User)    │
                    ├────────────────────────────────┤
                    │ • id (PK)                      │
                    │ • user_id (FK)                 │
                    │ • title                        │
                    │ • destination                  │
                    │ • start_date, end_date         │
                    │ • budget                       │
                    └────┬───────────────────┬────────┘
                         │                   │
                    1:Many│              1:Many│
                         │                   │
        ┌────────────────▼─────┐   ┌─────────▼─────────────────┐
        │      STOPS           │   │      ACTIVITIES           │
        ├──────────────────────┤   ├───────────────────────────┤
        │ • id (PK)            │   │ • id (PK)                 │
        │ • trip_id (FK)       │   │ • trip_id (FK)            │
        │ • location           │   │ • stop_id (FK, optional)  │
        │ • arrival_date       │   │ • name                    │
        │ • departure_date     │   │ • activity_type           │
        │ • sequence_order     │   │ • cost                    │
        └──────────────────────┘   │ • status                  │
                    ▲               └───────────────────────────┘
                    │
              0:Many│ (optional)
                    │
                    └──────────────────────────┘
                    
                    ┌────────────────────┐
                    │   EXPENSES         │
                    ├────────────────────┤
                    │ • id (PK)          │
                    │ • trip_id (FK)     │
                    │ • description      │
                    │ • amount           │
                    │ • category         │
                    │ • expense_date     │
                    │ • payment_method   │
                    │ • status           │
                    └──────────┬─────────┘
                               │
                          1:Many│
                               │
                      ┌─────────▼────────┐
                      │ (belongs to TRIP)│
                      └──────────────────┘


KEY RELATIONSHIPS SUMMARY:
════════════════════════════════════════

Relationship Type          | Description
─────────────────────────────────────────────────────────────
Users → Trips             | 1:Many (One user, many trips)
Trips → Stops             | 1:Many (One trip, many stops)
Trips → Activities        | 1:Many (One trip, many activities)
Stops → Activities        | 1:Many (One stop, many activities)
Trips → Expenses          | 1:Many (One trip, many expenses)

CASCADE DELETES:
- Deleting a User cascades to all Trips
- Deleting a Trip cascades to all Stops, Activities, Expenses
- Deleting a Stop sets stop_id to NULL in Activities (not deleted)


QUERY EXAMPLES:
════════════════════════════════════════

1. Get all trips for a user:
   SELECT * FROM trips WHERE user_id = ?

2. Get all stops for a trip (in order):
   SELECT * FROM stops WHERE trip_id = ? ORDER BY sequence_order

3. Get all activities for a trip:
   SELECT * FROM activities WHERE trip_id = ?

4. Get activities for a specific stop:
   SELECT * FROM activities WHERE stop_id = ?

5. Get total expenses for a trip:
   SELECT SUM(amount) FROM expenses WHERE trip_id = ?

6. Get expenses by category:
   SELECT category, SUM(amount) FROM expenses WHERE trip_id = ? GROUP BY category

7. Get trip budget vs actual spending:
   SELECT t.budget, SUM(e.amount) as spent 
   FROM trips t 
   LEFT JOIN expenses e ON t.id = e.trip_id 
   WHERE t.id = ? 
   GROUP BY t.id

"""

# Print the schema
if __name__ == '__main__':
    print("=" * 70)
    print("TRAVEL DATABASE - SCHEMA & RELATIONSHIPS")
    print("=" * 70)
    print(RELATIONSHIPS)
    print("\n" + "=" * 70)
    print("SQL SCHEMA")
    print("=" * 70)
    print(SQL_SCHEMA)
