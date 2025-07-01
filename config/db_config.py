# It connects to the SQLite database and Initialize the database if it does not exist.

import sqlite3
from sqlite3 import Error
import os

def get_connection():
    """
    Return a sqlite3 Connection to the rides.db file,
    with row_factory set to sqlite3.Row for dictionary data type access.
    """
    try: # Handle any errors that may occur during the connection process
        base_dir = os.path.dirname(os.path.dirname(__file__))  # Determine path to project root
    
        db_path = os.path.join(base_dir, 'database', 'rides.db')  # Build path to the database file

        conn = sqlite3.connect(db_path, detect_types=sqlite3.PARSE_DECLTYPES | sqlite3.PARSE_COLNAMES) # Connect (creates the file if it doesn't exist)

        conn.row_factory = sqlite3.Row   # Return rows as sqlite3.Row for attribute or key access
       
        return conn

    except sqlite3.Error as e:
        print(f"[Database ERROR] It failed to connect to the database: {e}")
        return None 
    
def create_tables(conn):
    """ Create tables if they do not exist """
    try:
        cursor = conn.cursor()

        # Vehicles table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS vehicles (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                type TEXT UNIQUE NOT NULL,
                base_fare REAL NOT NULL,
                fare_per_km REAL NOT NULL,
                capacity INTEGER,
                description TEXT
            );
        """)

        # Bookings table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS bookings (
                booking_id INTEGER PRIMARY KEY AUTOINCREMENT,,
                user_id INTEGER NOT NULL,
                vehicle_id INTEGER NOT NULL,
                pickup_latitude REAL NOT NULL,
                pickup_longitude REAL NOT NULL,
                dropoff_latitude REAL NOT NULL,
                dropoff_longitude REAL NOT NULL,
                pickup_address TEXT,
                dropoff_address TEXT,
                distance_km REAL,
                estimated_time_minutes REAL,
                fare REAL,
                status TEXT NOT NULL DEFAULT 'pending',
                booking_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                completion_time TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(id),
                FOREIGN KEY (vehicle_id) REFERENCES vehicles(id)
            );
        """)
        conn.commit()
        print("Tables created successfully or already exist.")
    except Error as e:
        print(e)