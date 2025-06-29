from .db_config import create_connection

class BookingService:
    def __init__(self):
        self.conn = create_connection()
        if self.conn:
            self.cursor = self.conn.cursor()
        else:
            raise Exception("Failed to connect to database for BookingService.")

    def add_booking(self, user_id, vehicle_id, pickup_lat, pickup_lon, dropoff_lat, dropoff_lon,
                    pickup_address=None, dropoff_address=None, distance_km=None,
                    estimated_time_minutes=None, fare=None):
        try:
            self.cursor.execute("""
                INSERT INTO bookings (booking_id, user_id, vehicle_id, pickup_latitude, pickup_longitude,
                                      dropoff_latitude, dropoff_longitude, pickup_address,
                                      dropoff_address, distance_km, estimated_time_minutes, fare)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (user_id, vehicle_id, pickup_lat, pickup_lon, dropoff_lat, dropoff_lon,
                  pickup_address, dropoff_address, distance_km, estimated_time_minutes, fare))
            
            booking_id = self.cursor.lastrowid
            self.conn.commit()
            return booking_id
        
        except Exception as e:
            print(f"Error adding booking: {e}")
        self.conn.rollback()
        return None
    
    def get_booking_by_id(self, booking_id):
        try:
            self.cursor.execute("SELECT * FROM bookings WHERE id = ?", (booking_id,))
            return self.cursor.fetchone()
        except Exception as e:
            print(f"Error getting booking by ID: {e}")
            return None

    def get_user_bookings(self, user_id):
        try:
            self.cursor.execute("SELECT * FROM bookings WHERE user_id = ?", (user_id,))
            return self.cursor.fetchall()
        except Exception as e:
            print(f"Error getting user bookings: {e}")
            return None

    def update_booking_status(self, booking_id, status):
        try:
            self.cursor.execute("UPDATE bookings SET status = ? WHERE id = ?", (status, booking_id))
            self.conn.commit()
            return True
        except Exception as e:
            print(f"Error updating booking status: {e}")
            return False

    def close_connection(self):
        if self.conn:
            self.conn.close()

