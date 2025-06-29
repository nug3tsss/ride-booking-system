# Database handler for managing bookings in a SQLite database. The below snippet are necessary for the database connection.
# IFF IT DOES NOT EXIST IN THE FILES

# THIS IS NEEDED FOR main.py to work properly [from database.db_handler import initialize_database initialize_database()]
# FOR THE BOOKING FORM [from database.db_handler import add_bookingbooking_id = add_booking(user_name, pickup_loc, dropoff_loc)]
# FOR THE DASHHBOARD [from database.db_handler import get_all_bookings all_rides = get_all_bookings()]
# also this one [from database.db_handler import cancel_booking cancel_booking(some_booking_id)]

from config.db_config import get_connection
import sqlite3


def initialize_database():
    try:
        with get_connection() as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS bookings (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    pickup TEXT NOT NULL,
                    destination TEXT NOT NULL,
                    status TEXT NOT NULL DEFAULT 'active',
                    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
                );
            """)
            conn.commit()
    except sqlite3.Error as e:
        print(f"[DB ERROR] Failed to initialize database: {e}")


def add_booking(name: str, pickup: str, destination: str) -> int | None:
    """
    Insert a new booking record.
    Returns the new booking's ID, or None on failure.
    """
    try:
        with get_connection() as conn:
            cursor = conn.execute(
                "INSERT INTO bookings (name, pickup, destination) VALUES (?, ?, ?);",
                (name, pickup, destination)
            )
            conn.commit()
            return cursor.lastrowid
    except sqlite3.Error as e:
        print(f"[DB ERROR] Failed to add booking: {e}")
        return None


def get_all_bookings() -> list:
    """
    Fetch all bookings.
    """
    try:
        with get_connection() as conn:
            cursor = conn.execute("SELECT * FROM bookings;")
            return cursor.fetchall()
    except sqlite3.Error as e:
        print(f"[DB ERROR] Failed to fetch bookings: {e}")
        return []


def get_booking_by_id(booking_id: int):
    """
    Fetch a single booking by its ID.
    Returns a sqlite3.Row or None if not found or on failure.
    """
    try:
        with get_connection() as conn:
            cursor = conn.execute(
                "SELECT * FROM bookings WHERE id = ?;",
                (booking_id,)
            )
            return cursor.fetchone()
    except sqlite3.Error as e:
        print(f"[DB ERROR] Failed to fetch booking by ID: {e}")
        return None


def cancel_booking(booking_id: int) -> int:
    """
    Mark a booking's status as 'cancelled'.
    """
    try:
        with get_connection() as conn:
            cursor = conn.execute(
                "UPDATE bookings SET status = 'cancelled' WHERE id = ?;",
                (booking_id,)
            )
            conn.commit()
            return cursor.rowcount
    except sqlite3.Error as e:
        print(f"[DB ERROR] Failed to cancel booking: {e}")
        return 0


def clear_bookings() -> None:
    """
    Delete all records from bookings.
    """
    try:
        with get_connection() as conn:
            conn.execute("DELETE FROM bookings;")
            conn.commit()
    except sqlite3.Error as e:
        print(f"[DB ERROR] Failed to clear bookings: {e}")
