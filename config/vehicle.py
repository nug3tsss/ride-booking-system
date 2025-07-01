from .db_config import get_connection

class VehicleService:
    def __init__(self):
        self.conn = get_connection()
        if self.conn:
            self.cursor = self.conn.cursor()
        else:
            raise Exception("Failed to connect to database for VehicleService.")

    def add_vehicle(self, vehicle_type, base_fare, fare_per_km, capacity=None, description=None):
        try:
            self.cursor.execute("""
                INSERT INTO vehicles (type, base_fare, fare_per_km, capacity, description)
                VALUES (?, ?, ?, ?, ?)
            """, (vehicle_type, base_fare, fare_per_km, capacity, description))
            self.conn.commit()
            return self.cursor.lastrowid
        except Exception as e:
            print(f"Error adding vehicle: {e}")
            return None

    def get_vehicle_by_id(self, vehicle_id):
        try:
            self.cursor.execute("SELECT * FROM vehicles WHERE id = ?", (vehicle_id,))
            return self.cursor.fetchone()
        except Exception as e:
            print(f"Error getting vehicle by ID: {e}")
            return None

    def get_all_vehicles(self):
        try:
            self.cursor.execute("SELECT * FROM vehicles")
            return self.cursor.fetchall()
        except Exception as e:
            print(f"Error getting all vehicles: {e}")
            return None

    def get_vehicle_by_type(self, vehicle_type):
        try:
            self.cursor.execute("SELECT * FROM vehicles WHERE type = ?", (vehicle_type,))
            return self.cursor.fetchone()
        except Exception as e:
            print(f"Error getting vehicle by type: {e}")
            return None

    def close_connection(self):
        if self.conn:
            self.conn.close()

