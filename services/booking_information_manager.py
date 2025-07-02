class BookingInformationManager():
    """
    Gets data from MapManager for database and data persistence
    """

    def __init__(self):
        self.__pickup_coords = None
        self.__dropoff_coords = None
        self.__vehicle_type_str = ""
        self.__vehicle_type_int = None
        self.__pickup_address = ""
        self.__dropoff_address = ""
        self.__route_line = []
        self.__bounding_box = ()

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
    
    def set_route_line(self, route_line=[]):
        self.__route_line = route_line
    
    def set_bounding_box(self, top_left, bottom_right):
        self.__bounding_box = (top_left, bottom_right)
    
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
    
    def get_current_booking_section(self):
        return self.__current_booking_section
    
    def clear_booking_information(self):
        print("BOOKING INFO HAS BEEN CLEARED")

        self.__pickup_coords = None
        self.__dropoff_coords = None
        self.__vehicle_type_str = ""
        self.__vehicle_type_int = None
        self.__pickup_address = ""
        self.__dropoff_address = ""
        self.__route_line = []
        self.__bounding_box = ()

        self.__current_booking_section = "Booking"