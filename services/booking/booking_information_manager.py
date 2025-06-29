from geopy.geocoders import Nominatim

class BookingInformationManager():
    def __init__(self, pin_location_manager, route_lines_manager):
        self.pin_location_manager = pin_location_manager
        self.route_lines_manager = route_lines_manager
        self.geolocator = Nominatim(user_agent="ride-booking-system")
    
    def get_coordinates(self):
        pickup_coords = self.pin_location_manager.get_pickup_coords_position()
        dropoff_coords = self.pin_location_manager.get_dropoff_coords_position()

        return {
            "pickup": {"lat": pickup_coords[0], "lon": pickup_coords[1]},
            "dropoff": {"lat": dropoff_coords[0], "lon": dropoff_coords[1]}
        }
    
    def get_addresses(self):
        pass
        # marker_coordinates = self.get_coordinates
        # pickup_address = self.geolocator.