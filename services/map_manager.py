import requests
import threading
from geopy.geocoders import Nominatim
from utils.helpers import get_current_location

class MapManager():
    """
    Handles everything tkintermapview-related:
    - marker placements for pickup and dropoff locations
    - route calculation and placement between two locations using OSRM
    - supply and get information to/from BookingInformationManager for data persistence
    """

    def __init__(self, booking_map, booking_information_manager):
        self.__booking_map = booking_map
        self.__booking_information_manager = booking_information_manager
        self.__geolocator = Nominatim(user_agent="ride-booking-system")
        
        self.__latitude, self.__longitude = get_current_location()
        self.__pickup_marker = None
        self.__dropoff_marker = None
        self.__route_line = None
        
        self.__initialize_map()

        self.__restore_information_from_previous()
    
    def __initialize_map(self):
        self.__booking_map.set_tile_server("https://mt0.google.com/vt/lyrs=m&hl=en&x={x}&y={y}&z={z}&s=Ga", max_zoom=22)
        self.__booking_map.set_position(self.__latitude, self.__longitude)
        self.__booking_map.set_zoom(16)
        self.__booking_map.add_right_click_menu_command(label="Select destination as pick-up", command=self.__draw_pickup_marker, pass_coords=True)
        self.__booking_map.add_right_click_menu_command(label="Select destination as drop-off", command=self.__draw_dropoff_marker, pass_coords=True)
        self.__booking_map.add_right_click_menu_command(label="Remove pick-up marker", command=self.__remove_pickup_marker)
        self.__booking_map.add_right_click_menu_command(label="Remove drop-off marker", command=self.__remove_dropoff_marker)
        self.__booking_map.pack(expand=True, fill="both", padx=15, pady=15)
    
    def __draw_pickup_marker(self, coords):
        if self.__pickup_marker is not None:
            self.__pickup_marker.delete()
        
        self.__pickup_marker = self.__booking_map.set_marker(coords[0], coords[1], text="Pick-up", marker_color_circle="#4A628A", marker_color_outside="#6A9AB0")
        self.__booking_information_manager.set_pickup_coords(coords)
        threading.Thread(target=self.__reverse_geocode_pickup, args=(coords,)).start()

        self.__verify_markers()
    
    def __remove_pickup_marker(self):
        if self.__pickup_marker is not None:
            self.__pickup_marker.delete()
            self.__pickup_marker = None
            self.__booking_map.delete_all_path()
    
    def __reverse_geocode_pickup(self, coords):
        location_obj = self.__geolocator.reverse(coords)
        if location_obj:
            full_address = location_obj.address
            self.__booking_information_manager.set_pickup_address(full_address)

    def __draw_dropoff_marker(self, coords):
        if self.__dropoff_marker is not None:
            self.__dropoff_marker.delete()
        
        self.__dropoff_marker = self.__booking_map.set_marker(coords[0], coords[1], text="Drop-off", marker_color_circle="#16423C", marker_color_outside="#6A9C89")
        self.__booking_information_manager.set_dropoff_coords(coords)
        threading.Thread(target=self.__reverse_geocode_dropoff, args=(coords,)).start()
        self.__verify_markers()
    
    def __remove_dropoff_marker(self):
        if self.__dropoff_marker is not None:
            self.__dropoff_marker.delete()
            self.__dropoff_marker = None
            self.__booking_map.delete_all_path()
    
    def __reverse_geocode_dropoff(self, coords):
        location_obj = self.__geolocator.reverse(coords) # This returns a geopy.Location object
        if location_obj:
            # Extract the string address from the geopy.Location object
            full_address = location_obj.address
            self.__booking_information_manager.set_dropoff_address(full_address)

    def __verify_markers(self):
        if self.__pickup_marker is not None and self.__dropoff_marker is None:
            self.__booking_map.set_position(self.__pickup_marker.position[0], self.__pickup_marker.position[1])
        elif self.__dropoff_marker is not None and self.__pickup_marker is None:
            self.__booking_map.set_position(self.__dropoff_marker.position[0], self.__dropoff_marker.position[1])

        if self.__pickup_marker is not None and self.__dropoff_marker is not None:
            self.__organize_marker_coords()
            self.__calculate_marker_minmax_coords()
            self.__calculate_route_lines()
    
    def __organize_marker_coords(self):
        self.__pickup_lat = self.__pickup_marker.position[0]
        self.__pickup_lon = self.__pickup_marker.position[1]
        self.__dropoff_lat = self.__dropoff_marker.position[0]
        self.__dropoff_lon = self.__dropoff_marker.position[1]
    
    def __calculate_marker_minmax_coords(self):
        self.__min_lat = min(self.__pickup_lat, self.__dropoff_lat)
        self.__max_lat = max(self.__pickup_lat, self.__dropoff_lat)
        self.__min_lon = min(self.__pickup_lon, self.__dropoff_lon)
        self.__max_lon = max(self.__pickup_lon, self.__dropoff_lon)
    
    def __calculate_route_lines(self):
        threading.Thread(target=self.__calculate_route_lines_thread).start()
    
    def __calculate_route_lines_thread(self):
        url = f"http://router.project-osrm.org/route/v1/driving/{self.__pickup_lon},{self.__pickup_lat};{self.__dropoff_lon},{self.__dropoff_lat}?overview=full&geometries=geojson"
        response = requests.get(url)
        data = response.json()

        self.__booking_map.after(0, lambda: self.__draw_route_lines(data))
    
    def __draw_route_lines(self, data):
        if not data or "routes" not in data or not data["routes"]:
            print("No route found or invalid OSRM response.")
            self.__booking_information_manager.set_route_line([])
            self.__booking_information_manager.set_bounding_box((), ())
            self.__booking_information_manager.set_distance_km(0.0)
            self.__booking_information_manager.set_estimated_time_seconds(0.0)
            return
        
        coords = data["routes"][0]["geometry"]["coordinates"]
        path_latlon = [(lat, lon) for lon, lat in coords]

        distance_meters = data["routes"][0]["distance"]
        duration_seconds = data["routes"][0]["duration"]

        distance_km = distance_meters / 1000.0
        
        if self.__route_line is not None:
            self.__route_line.delete()
        
        __top_left = (self.__max_lat, self.__min_lon)
        __bottom_right = (self.__min_lat, self.__max_lon)
        
        self.__route_line = self.__booking_map.set_path(path_latlon)
        self.__booking_information_manager.set_route_line(path_latlon)
        self.__booking_information_manager.set_distance_km(distance_km)
        self.__booking_information_manager.set_estimated_time_seconds(duration_seconds)

        self.__booking_map.fit_bounding_box(__top_left, __bottom_right)
        self.__booking_information_manager.set_bounding_box(__top_left, __bottom_right)

    def __restore_information_from_previous(self):
        pickup = self.__booking_information_manager.get_pickup_coords()
        dropoff = self.__booking_information_manager.get_dropoff_coords()
        bounding_box = self.__booking_information_manager.get_bounding_box()
        route_line = self.__booking_information_manager.get_route_line()

        if pickup is not None:
            self.__pickup_marker = self.__booking_map.set_marker(pickup[0], pickup[1], text="Pick-up", marker_color_circle="#4A628A", marker_color_outside="#6A9AB0")
        
        if dropoff is not None:
            self.__dropoff_marker = self.__booking_map.set_marker(dropoff[0], dropoff[1], text="Drop-off", marker_color_circle="#16423C", marker_color_outside="#6A9C89")
        
        if bounding_box != ():
            self.__booking_map.fit_bounding_box(bounding_box[0], bounding_box[1])
        
        if route_line != []:
            self.__route_line = self.__booking_map.set_path(route_line)
    
    def get_coords_from_address(self, address, marker_type, callback=None):
        location = self.__geolocator.geocode(address)

        if location:
            coords = (location.latitude, location.longitude)

            if marker_type == "pickup":
                location_obj = self.__geolocator.reverse(coords)
                full_address = location_obj.address
                self.__booking_information_manager.set_pickup_address(full_address)
                self.__booking_information_manager.set_pickup_coords(coords)
                self.__draw_pickup_marker(coords)

                if callback:
                    callback(full_address, marker_type)

            elif marker_type == "dropoff":
                location_obj = self.__geolocator.reverse(coords)
                full_address = location_obj.address
                self.__booking_information_manager.set_dropoff_address(full_address)
                self.__booking_information_manager.set_dropoff_coords(coords)
                self.__draw_dropoff_marker(coords)

                if callback:
                    callback(full_address, marker_type)
    
    def set_map_markers_from_file(self, pickup_coords, dropoff_coords):
        self.__draw_pickup_marker(pickup_coords)
        self.__draw_dropoff_marker(dropoff_coords)
