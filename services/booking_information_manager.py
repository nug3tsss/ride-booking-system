class BookingInformationManager():
    def __init__(self):
        self.pickup_coords = None
        self.dropoff_coords = None
        self.vehicle_type = None
        self.pickup_address = ""
        self.dropoff_address = ""
    
    def set_pickup_information(self, coords, address=""):
        self.pickup_coords = coords
        self.pickup_address = address
    
    def set_dropoff_information(self, coords, address=""):
        self.dropoff_coords = coords
        self.dropoff_address = address
    
    def set_vehicle_information(self, vehicle_type):
        self.vehicle_type = vehicle_type