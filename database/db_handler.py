from config.db_config import get_connection
import sqlite3
import os
from datetime import datetime
from models.vehicle import Vehicle, Car, Motorcycle,Van

class BookingStatus:
    ACTIVE = 'active'
    CANCELLED = 'cancelled'
    COMPLETED = 'completed'
    PENDING = 'pending'
    DRIVER_ASSIGNED = 'driver_assigned'
    EN_ROUTE = 'en_route'
    ARRIVED_PICKUP = 'arrived_pickup'

class DatabaseHandler:
    _initialized = False

    def __init__(self):
        if not DatabaseHandler._initialized:
            self.initialize_database()
            self._insert_default_admin_user()
            DatabaseHandler._initialized = True


    def initialize_database(self):
        """Initialize database"""
        try:
            with get_connection() as conn: # Create a connection to the database
                conn.execute("PRAGMA foreign_keys = ON;") # Enable foreign key constraints for maintaining data integrity.

                # Create users table
                conn.execute("""
                    CREATE TABLE IF NOT EXISTS users (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        user_id INTEGER DEFAULT 0,
                        username TEXT UNIQUE NOT NULL,
                        password TEXT NOT NULL,
                        first_name TEXT NOT NULL,
                        last_name TEXT NOT NULL,
                        role TEXT NOT NULL DEFAULT 'user',
                        profile_pic TEXT DEFAULT 'assets/icons/profile.jpg'
                );
                """)
                
                # Create vehicles table
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

                # Insert default vehicles
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

                # Create messages table
                conn.execute("""
                    CREATE TABLE IF NOT EXISTS messages (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        name TEXT NOT NULL,
                        email TEXT NOT NULL,
                        message TEXT NOT NULL,
                        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
                    );
                """)

                conn.commit() # Commit the changes
                print("[DB INFO] Database tables created successfully.")
        except sqlite3.Error as e:
            print(f"[DB ERROR] Failed to initialize database: {e}")

    # Inserts a default admin user if one does not already exist
    def _insert_default_admin_user(self):
        """Inserts a default admin user if one does not already exist."""
        try:
            with get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT id FROM users WHERE username = 'admin'")
                if not cursor.fetchone():
                    conn.execute(
                        "INSERT INTO users (username, password, first_name, last_name, role) VALUES (?, ?, ?, ?, ?)",
                        ('admin', 'admin', 'Admin', 'User', 'admin')
                    )
                    conn.commit()
                    print("[DB INFO] Default admin user created.")
        except sqlite3.Error as e:
            print(f"[DB ERROR] Failed to insert default admin user: {e}")

    # Fetches all users from the database - This is used to display user information in the admin dashboard
    def get_vehicle_details_by_type(self, vehicle_type: str) -> Vehicle | None:
        """Fetch vehicle details by type and return a Vehicle object."""
        try:
            with get_connection() as conn:
                cursor = conn.execute(
                    "SELECT id, type, model, license_plate, driver_name, driver_contact, base_fare, per_km_rate FROM vehicles WHERE type = ? LIMIT 1;",
                    (vehicle_type,)
                )
                result = cursor.fetchone()
                if result:
                    # Create an instance of the specific Vehicle subclass
                    if result['type'] == "Car":
                        return Car(result['id'], result['model'], result['license_plate'], result['driver_name'], result['driver_contact'], result['base_fare'], result['per_km_rate'])
                    elif result['type'] == "Van":
                        return Van(result['id'], result['model'], result['license_plate'], result['driver_name'], result['driver_contact'], result['base_fare'], result['per_km_rate'])
                    elif result['type'] == "Motorcycle":
                        return Motorcycle(result['id'], result['model'], result['license_plate'], result['driver_name'], result['driver_contact'], result['base_fare'], result['per_km_rate'])
                    else:
                        print(f"[DB ERROR] Unknown vehicle type: {result['type']}")
                        return None
                return None
            
        except sqlite3.Error as e:
            print(f"[DB ERROR] Failed to fetch vehicle details by type: {e}")
            return None

    # Inserts a new booking record into the database - This is used when a user books a ride
    def add_booking(self,user_id: int, pickup: str, destination: str, vehicle_id: int, distance_km: float = 0.0, estimated_cost: float = 0.0) -> int | None:
        """Insert a new booking record"""
        try:
            with get_connection() as conn:
                cursor = conn.execute(
                    """INSERT INTO bookings
                       (user_id, pickup, destination, vehicle_id, distance_km, estimated_cost, status, created_at)
                       VALUES (?, ?, ?, ?, ?, ?, ?, ?);""",
                    (user_id, pickup, destination, vehicle_id, distance_km, estimated_cost, 'completed', datetime.now())
                )
                conn.commit()
                print(f"[DB INFO] Booking added successfully with ID: {cursor.lastrowid}")
                return cursor.lastrowid
        except sqlite3.Error as e:
            print(f"[DB ERROR] Failed to add booking: {e}")
            return None

    # Fetches all bookings made by a specific user - This is used to display the user's booking history
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

    # Updates the status of a booking - This is used to mark a booking as completed, cancelled, etc.
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

    # Cancels a booking by marking it as cancelled    
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

    # Completes a booking by marking it as completed - This is used when the ride is finished
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

    # Clears all bookings from the database - This is used for testing purposes
    def clear_bookings(self) -> None:
        """Delete all bookings (for testing)"""
        try:
            with get_connection() as conn:
                conn.execute("DELETE FROM bookings;")
                conn.commit()
                print("[DB INFO] All bookings cleared")
        except sqlite3.Error as e:
            print(f"[DB ERROR] Failed to clear bookings: {e}")

    # Resets the database completely (development only)
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

    # Fetches all bookings from the database
    def get_all_bookings(self) -> list:
        """Fetches all booking records from the database."""
        try:
            with get_connection() as conn:
                cursor = conn.execute(
                    """SELECT b.*, v.type as vehicle_type, v.model as vehicle_model, v.license_plate, v.driver_name, v.driver_contact
                    FROM bookings b
                    JOIN vehicles v ON b.vehicle_id = v.id
                    ORDER BY b.created_at DESC;"""
                )
                bookings = [dict(row) for row in cursor.fetchall()]
                print(f"[DB DEBUG] Found {len(bookings)} total bookings.")
                return bookings
        except sqlite3.Error as e:
            print(f"[DB ERROR] Failed to fetch all bookings: {e}")
            return []

    # Fetches all vehicles from the database
    def get_all_vehicles(self) -> list:
        try:
            with get_connection() as conn:
                cursor = conn.execute("SELECT * FROM vehicles;")
                vehicles = [dict(row) for row in cursor.fetchall()]
                print(f"[DB DEBUG] Loaded {len(vehicles)} vehicles.")
                return vehicles
        except sqlite3.Error as e:
            print(f"[DB ERROR] Failed to fetch all vehicles: {e}")
            return []
        
    # Fetches all users from the database
    def get_all_users(self) -> list:
        try:
            with get_connection() as conn:
                cursor = conn.execute("SELECT * FROM users;")
                users = [dict(row) for row in cursor.fetchall()]
                print(f"[DB DEBUG] Loaded {len(users)} users.")
                return users
        except sqlite3.Error as e:
            print(f"[DB ERROR] Failed to fetch all users: {e}")
            return []

    # Fetches all messages submitted through the Contact Us form
    def get_all_messages(self) -> list:
        """Fetch all messages submitted through the Contact Us form."""
        try:
            with get_connection() as conn:
                cursor = conn.execute("SELECT * FROM messages ORDER BY timestamp DESC;")
                messages = [dict(row) for row in cursor.fetchall()]
                print(f"[DB DEBUG] Loaded {len(messages)} messages.")
                return messages
        except sqlite3.Error as e:
            print(f"[DB ERROR] Failed to fetch messages: {e}")
            return []