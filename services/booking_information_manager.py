#from database.db_handler import DatabaseHandler
class BookingInformationManager:
    """Saves all of the booking informations from the current session"""

    def __init__(self, db_handler):
        self.__db = db_handler
        self.__pickup_coords = None
        self.__dropoff_coords = None
        self.__vehicle_type_str = ""
        self.__vehicle_type_int = None
        self.__pickup_address = ""
        self.__dropoff_address = ""
        self.__route_line = []
        self.__bounding_box = ()
        self.__distance_km = 0.0
        self.__estimated_time_seconds = 0.0
        self.__estimated_cost_pesos = 0.0
        self.__current_booking_section = "Booking"
    
    def set_pickup_coords(self, coords=None):
        self.__pickup_coords = coords
    
    def set_pickup_address(self, address=""):
        self.__pickup_address = address
    
    def set_dropoff_coords(self, coords=None):
        self.__dropoff_coords = coords
    
    def set_dropoff_address(self, address=""):
        self.__dropoff_address = address
    
    def set_vehicle_type_str(self, vehicle_type_str=""):
        self.__vehicle_type_str = vehicle_type_str
    
    def set_vehicle_type_int(self, vehicle_type_int=None):
        self.__vehicle_type_int = vehicle_type_int
        
        if vehicle_type_int is not None:
            vehicle_type_map = {
                1: "Car",
                2: "Van",
                3: "Motorcycle"
            }
            vehicle_type_db = vehicle_type_map.get(vehicle_type_int)
            if vehicle_type_db:
                self.__vehicle_details = self.__db.get_vehicle_details_by_type(vehicle_type_db)
            else:
                self.__vehicle_details = None
        else:
            self.__vehicle_details = None
    
    def set_route_line(self, route_line=[]):
        self.__route_line = route_line
    
    def set_bounding_box(self, top_left, bottom_right):
        self.__bounding_box = (top_left, bottom_right)

    def set_distance_km(self, distance_km: float):
        self.__distance_km = distance_km

    def set_estimated_time_seconds(self, estimated_time_seconds: float):
        self.__estimated_time_seconds = estimated_time_seconds
    
    def set_estimated_cost_pesos(self, estimated_cost_pesos: float):
        self.__estimated_cost_pesos = estimated_cost_pesos

    def set_current_booking_section(self, booking_section):
        self.__current_booking_section = booking_section

    def get_pickup_coords(self):
        return self.__pickup_coords
    
    def get_pickup_address(self):
        return self.__pickup_address
        
    def get_dropoff_coords(self):
        return self.__dropoff_coords
        
    def get_dropoff_address(self):
        return self.__dropoff_address
        
    def get_vehicle_type_str(self):
        return self.__vehicle_type_str
    
    def get_vehicle_type_int(self):
        return self.__vehicle_type_int
    
    def get_route_line(self):
        return self.__route_line

    def get_bounding_box(self):
        return self.__bounding_box
    
    def get_distance_km(self):
        return self.__distance_km
    
    def get_estimated_time_seconds(self):
        return self.__estimated_time_seconds
    
    def get_estimated_cost_pesos(self):
        return self.__estimated_cost_pesos
     
    def get_current_booking_section(self):
        return self.__current_booking_section
    
    def get_vehicle_details(self):
        return self.__vehicle_details

    def get_estimated_cost(self):
        if self.__vehicle_type_int is None or self.__distance_km == 0.0:
            self.__estimated_cost_pesos = 0.0
            return self.__estimated_cost_pesos
        
        vehicle_type_map = {
            1: "Car",
            2: "Van",
            3: "Motorcycle"
        }
        vehicle_type_db = vehicle_type_map.get(self.__vehicle_type_int)
        if vehicle_type_db:
            vehicle_details = self.__db.get_vehicle_details_by_type(vehicle_type_db)
            if vehicle_details:
                base_fare = vehicle_details["base_fare"]
                per_km_rate = vehicle_details["per_km_rate"]
                self.__estimated_cost_pesos = base_fare + (per_km_rate * self.__distance_km)
                return self.__estimated_cost_pesos # Return the calculated value
    
    def clear_booking_information(self):
        self.__pickup_coords = None
        self.__dropoff_coords = None
        self.__vehicle_type_str = ""
        self.__vehicle_type_int = None
        self.__pickup_address = ""
        self.__dropoff_address = ""
        self.__route_line = []
        self.__bounding_box = ()
        self.__distance_km = 0.0
        self.__estimated_cost_pesos = 0.0
        self.__current_booking_section = "Booking"