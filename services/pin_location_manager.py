from services.route_lines_manager import RouteLinesManager

class PinLocationManager():
    def __init__(self, booking_map):
        self.booking_map = booking_map
        self.route_lines_manager = RouteLinesManager(booking_map)

        self.pickup_marker = None
        self.dropoff_marker = None
    
    def add_pickup_marker(self, coords):
        if self.pickup_marker is not None:
            self.pickup_marker.delete()

        self.pickup_marker = self.booking_map.set_marker(coords[0], coords[1], text="Pick-up destination")
        self.verify_markers()
    
    def add_dropoff_marker(self, coords):
        if self.dropoff_marker is not None:
            self.dropoff_marker.delete()

        self.dropoff_marker = self.booking_map.set_marker(coords[0], coords[1], text="Drop-off destination")
        self.verify_markers()
    
    def verify_markers(self):
        if self.pickup_marker is not None and self.dropoff_marker is not None:
            self.route_lines_manager.get_marker_coords(self.pickup_marker, self.dropoff_marker)