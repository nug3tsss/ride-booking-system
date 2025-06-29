import sqlite3
from sqlite3 import Error

DATABASE_FILE = 'rides.db'

def create_connection():
    """ Create a database connection to the SQLite database specified by DATABASE_FILE """
    conn = None
    try:
        conn = sqlite3.connect(DATABASE_FILE)
        return conn
    except Error as e:
        print(e)
    return conn

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

if __name__ == '__main__':
    conn = create_connection()
    if conn:
        create_tables(conn)
        conn.close()
