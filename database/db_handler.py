from config.db_config import get_connection
import sqlite3
import os
from datetime import datetime

class BookingStatus:
    ACTIVE = 'active'
    CANCELLED = 'cancelled'
    COMPLETED = 'completed'
    PENDING = 'pending'
    DRIVER_ASSIGNED = 'driver_assigned'
    EN_ROUTE = 'en_route'
    ARRIVED_PICKUP = 'arrived_pickup'

class DatabaseHandler:
    def __init__(self):
        self.initialize_database()
        self.get_connection = get_connection()

    def initialize_database(self):
        """Initialize database with proper schema"""
        try:
            #Users table
            with get_connection() as conn:
                conn.execute("PRAGMA foreign_keys = ON;")

                conn.execute("""
                    CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER DEFAULT 0,
                    username TEXT UNIQUE NOT NULL,
                    password TEXT NOT NULL,
                    first_name TEXT NOT NULL,
                    last_name TEXT NOT NULL,
                    role TEXT NOT NULL DEFAULT 'user',
                    profile_pic TEXT DEFAULT 'assets/profile.jpg'
                );
                """)
            #vehicle table
                conn.execute("""
                    CREATE TABLE IF NOT EXISTS vehicles (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        type TEXT NOT NULL,
                        model TEXT,
                        license_plate TEXT UNIQUE NOT NULL,
                        driver_name TEXT NOT NULL,
                        driver_contact TEXT,
                        base_fare REAL NOT NULL,
                        per_km_rate REAL NOT NULL
                    );
                """)
                #booking Table
                conn.execute("""
                    CREATE TABLE IF NOT EXISTS bookings (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        user_id INTEGER NOT NULL,
                        pickup TEXT NOT NULL,
                        destination TEXT NOT NULL,
                        vehicle_id INTEGER,
                        distance_km REAL DEFAULT 0.0,
                        estimated_cost REAL DEFAULT 0.0,
                        status TEXT NOT NULL DEFAULT 'active',
                        created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
                        completed_at TIMESTAMP,
                        FOREIGN KEY (vehicle_id) REFERENCES vehicles(id)
                    );
                """)
                conn.commit()
                print("[DB INFO] Database tables created successfully.")
                self.populate_initial_vehicles()
        except sqlite3.Error as e:
            print(f"[DB ERROR] Failed to initialize database: {e}")

    def populate_initial_vehicles(self):
        """Populate initial vehicle data if the table is empty."""
        try:
            with get_connection() as conn:
                cursor = conn.execute("SELECT COUNT(*) FROM vehicles;")
                if cursor.fetchone()[0] == 0:
                    vehicles_to_add = [
                        ("Car", "Sedan", "ABC-123", "John Doe", "09171234567", 50.0, 15.0),
                        ("Van", "Cargo Van", "DEF-456", "Jane Smith", "09187654321", 100.0, 25.0),
                        ("Motorcycle", "Scooter", "GHI-789", "Peter Jones", "09191122334", 30.0, 10.0)
                    ]
                    conn.executemany("""
                        INSERT INTO vehicles (type, model, license_plate, driver_name, driver_contact, base_fare, per_km_rate)
                        VALUES (?, ?, ?, ?, ?, ?, ?);
                    """, vehicles_to_add)
                    conn.commit()
                    print("[DB INFO] Initial vehicle data populated.")
                else:
                    print("[DB INFO] Vehicles table already contains data. Skipping initial population.")
        except sqlite3.Error as e:
            print(f"[DB ERROR] Failed to populate initial vehicles: {e}")

    def get_vehicle_details_by_type(self, vehicle_type: str) -> dict | None:
        """Fetch vehicle details (base_fare, per_km_rate) by type."""
        try:
            with get_connection() as conn:
                cursor = conn.execute(
                    "SELECT id, type, model, license_plate, driver_name, driver_contact, base_fare, per_km_rate FROM vehicles WHERE type = ? LIMIT 1;",
                    (vehicle_type,)
                )
                result = cursor.fetchone()
                if result:
                    return dict(result)
                return None
        except sqlite3.Error as e:
            print(f"[DB ERROR] Failed to fetch vehicle details by type: {e}")
            return None

    def add_booking(self,user_id: int, pickup: str, destination: str, vehicle_id: int, distance_km: float = 0.0, estimated_cost: float = 0.0) -> int | None:
        """Insert a new booking record"""
        try:
            with get_connection() as conn:
                cursor = conn.execute(
                    """INSERT INTO bookings
                       (user_id, pickup, destination, vehicle_id, distance_km, estimated_cost)
                       VALUES (?, ?, ?, ?, ?, ?);""",
                    (user_id, pickup, destination, vehicle_id, distance_km, estimated_cost)
                )
                conn.commit()
                print(f"[DB INFO] Booking added successfully with ID: {cursor.lastrowid}")
                return cursor.lastrowid
        except sqlite3.Error as e:
            print(f"[DB ERROR] Failed to add booking: {e}")
            return None
        
    def get_bookings_by_user(self, user_id: int) -> list:
        try:
            with get_connection() as conn:
                cursor = conn.execute(
                    """SELECT b.*, v.type as vehicle_type, v.model as vehicle_model, v.license_plate, v.driver_name, v.driver_contact
                    FROM bookings b
                    JOIN vehicles v ON b.vehicle_id = v.id
                    WHERE b.user_id = ?
                    ORDER BY b.created_at DESC;""",
                    (user_id,)
                )
                bookings = [dict(row) for row in cursor.fetchall()]

                print(f"[DB DEBUG] Found {len(bookings)} bookings for user_id {user_id}")

                return bookings
        except sqlite3.Error as e:
            print(f"[DB ERROR] Failed to fetch bookings for user: {e}")
            return []

    def update_booking_status(self, booking_id: int, status: str) -> int:
        try:
            with get_connection() as conn:
                cursor = conn.execute(
                    "UPDATE bookings SET status = ? WHERE id = ?;",
                    (status, booking_id)
                )
                conn.commit()
                return cursor.rowcount
        except sqlite3.Error as e:
            print(f"[DB ERROR] Failed to update booking status: {e}")
            return 0
        


    def cancel_booking(self, booking_id: int) -> int:
        """Mark a booking as cancelled"""
        try:
            with get_connection() as conn:
                cursor = conn.execute(
                    "UPDATE bookings SET status = 'cancelled', completed_at = ? WHERE id = ?;",
                    (datetime.now(), booking_id)
                )
                conn.commit()
                return cursor.rowcount
        except sqlite3.Error as e:
            print(f"[DB ERROR] Failed to cancel booking: {e}")
            return 0

    def complete_booking(self, booking_id: int) -> int:
        """Mark a booking as completed"""
        try:
            with get_connection() as conn:
                cursor = conn.execute(
                    "UPDATE bookings SET status = 'completed', completed_at = ? WHERE id = ?;",
                    (datetime.now(), booking_id)
                )
                conn.commit()
                return cursor.rowcount
        except sqlite3.Error as e:
            print(f"[DB ERROR] Failed to complete booking: {e}")
            return 0

    def clear_bookings(self) -> None:
        """Delete all bookings (for testing)"""
        try:
            with get_connection() as conn:
                conn.execute("DELETE FROM bookings;")
                conn.commit()
                print("[DB INFO] All bookings cleared")
        except sqlite3.Error as e:
            print(f"[DB ERROR] Failed to clear bookings: {e}")

    def reset_database_completely(self) -> None:
        """Reset database completely (development only)"""
        try:
            with get_connection() as conn:
                conn.execute("DROP TABLE IF EXISTS bookings;")
                conn.execute("DROP TABLE IF EXISTS vehicles;")
                conn.execute("DROP TABLE IF EXISTS users;")
                conn.commit()
                print("[DB INFO] Database reset completely")
            self.initialize_database()
        except sqlite3.Error as e:
            print(f"[DB ERROR] Failed to reset database: {e}")

