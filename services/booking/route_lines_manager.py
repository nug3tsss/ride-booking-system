import requests

class RouteLinesManager():
    def __init__(self, booking_map):
        self.booking_map = booking_map
        self.route_line = None
        # self.modes = ["driving", "cycling", "walking"]
    
    def get_marker_coords(self, pickup_marker, dropoff_marker):
        self.pickup_lat = pickup_marker.position[0]
        self.pickup_lon = pickup_marker.position[1]
        self.dropoff_lat = dropoff_marker.position[0]
        self.dropoff_lon = dropoff_marker.position[1]

        self.initialize_osrm()
    
    def initialize_osrm(self):
        url=f"http://router.project-osrm.org/route/v1/driving/{self.pickup_lon},{self.pickup_lat};{self.dropoff_lon},{self.dropoff_lat}?overview=full&geometries=geojson"
        response = requests.get(url)
        data = response.json()

        self.extract_coords(data)
    
    def extract_coords(self, data):
        coords = data["routes"][0]["geometry"]["coordinates"]
        path_latlon = [(lat, lon) for lon, lat in coords]

        if self.route_line is not None:
            self.route_line.delete()
        
        self.route_line = self.booking_map.set_path(path_latlon)

        