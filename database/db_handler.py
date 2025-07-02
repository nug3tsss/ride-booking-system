from config.db_config import get_connection
import sqlite3
import os
from datetime import datetime


class DatabaseHandler:
    def __init__(self):
        self.initialize_database()
        self.get_connection = get_connection()

    def initialize_database(self):
        """Initialize database with proper schema"""
        try:
            with get_connection() as conn:
                conn.execute("PRAGMA foreign_keys = ON;")
                conn.execute("""
                    CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT UNIQUE NOT NULL,
                    password TEXT NOT NULL,
                    first_name TEXT NOT NULL,
                    last_name TEXT NOT NULL,
                    role TEXT NOT NULL DEFAULT 'user',
                    profile_pic TEXT DEFAULT 'assets/profile.jpg'
                );
                """)
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
                conn.execute("""
                    CREATE TABLE IF NOT EXISTS bookings (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        name TEXT NOT NULL,
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

    def add_booking(self, name: str, pickup: str, destination: str, vehicle_id: int, distance_km: float = 0.0, estimated_cost: float = 0.0) -> int | None:
        """Insert a new booking record"""
        try:
            with get_connection() as conn:
                cursor = conn.execute(
                    """INSERT INTO bookings
                       (name, pickup, destination, vehicle_id, distance_km, estimated_cost)
                       VALUES (?, ?, ?, ?, ?, ?);""",
                    (name, pickup, destination, vehicle_id, distance_km, estimated_cost)
                )
                conn.commit()
                print(f"[DB INFO] Booking added successfully with ID: {cursor.lastrowid}")
                return cursor.lastrowid
        except sqlite3.Error as e:
            print(f"[DB ERROR] Failed to add booking: {e}")
            return None

    def get_all_bookings(self) -> list:
        """Fetch all bookings with vehicle details"""
        try:
            with get_connection() as conn:
                cursor = conn.execute("""
                    SELECT
                        b.id, b.name, b.pickup, b.destination,
                        COALESCE(b.distance_km, 0.0) as distance_km,
                        COALESCE(b.estimated_cost, 0.0) as estimated_cost,
                        b.status, b.created_at, b.completed_at,
                        COALESCE(v.type, 'Unknown') AS vehicle_type,
                        COALESCE(v.model, 'Unknown') AS vehicle_model,
                        COALESCE(v.license_plate, 'N/A') AS license_plate,
                        COALESCE(v.driver_name, 'Unknown') AS driver_name,
                        COALESCE(v.driver_contact, 'N/A') AS driver_contact
                    FROM bookings b
                    LEFT JOIN vehicles v ON b.vehicle_id = v.id
                    ORDER BY b.created_at DESC;
                """)
                result = cursor.fetchall()
                print(f"[DB INFO] Retrieved {len(result)} bookings")
                return result
        except sqlite3.Error as e:
            print(f"[DB ERROR] Failed to fetch bookings: {e}")
            return []

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

    def get_booking_history(self) -> list:
        """Fetch completed and cancelled bookings"""
        try:
            with get_connection() as conn:
                cursor = conn.execute("""
                    SELECT
                        b.id, b.name, b.pickup, b.destination,
                        COALESCE(b.distance_km, 0.0) as distance_km,
                        COALESCE(b.estimated_cost, 0.0) as estimated_cost,
                        b.status, b.created_at, b.completed_at,
                        COALESCE(v.type, 'Unknown') AS vehicle_type,
                        COALESCE(v.model, 'Unknown') AS vehicle_model,
                        COALESCE(v.license_plate, 'N/A') AS license_plate,
                        COALESCE(v.driver_name, 'Unknown') AS driver_name,
                        COALESCE(v.driver_contact, 'N/A') AS driver_contact
                    FROM bookings b
                    LEFT JOIN vehicles v ON b.vehicle_id = v.id
                    WHERE b.status IN ('completed', 'cancelled')
                    ORDER BY b.completed_at DESC;
                """)
                return cursor.fetchall()
        except sqlite3.Error as e:
            print(f"[DB ERROR] Failed to fetch booking history: {e}")
            return []

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

