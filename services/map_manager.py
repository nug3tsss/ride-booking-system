import requests
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
        
        self.__booking_map.set_tile_server("https://mt0.google.com/vt/lyrs=m&hl=en&x={x}&y={y}&z={z}&s=Ga", max_zoom=22)
        #self.__booking_map.set_position(14.599036510236097, 121.00494831003196)
        self.__booking_map.set_position(self.__latitude, self.__longitude)
        self.__booking_map.set_zoom(16)
        self.__booking_map.add_right_click_menu_command(label="Select destination as pick-up", command=self.__draw_pickup_marker, pass_coords=True)
        self.__booking_map.add_right_click_menu_command(label="Select destination as drop-off", command=self.__draw_dropoff_marker, pass_coords=True)
        self.__booking_map.add_right_click_menu_command(label="Remove pick-up marker", command=self.__remove_pickup_marker)
        self.__booking_map.add_right_click_menu_command(label="Remove drop-off marker", command=self.__remove_dropoff_marker)
        self.__booking_map.pack(expand=True, fill="both", padx=15, pady=15)

        self.__restore_information_from_previous()
    
    def __draw_pickup_marker(self, coords):
        if self.__pickup_marker is not None:
            self.__pickup_marker.delete()
        
        self.__pickup_marker = self.__booking_map.set_marker(coords[0], coords[1], text="Pick-up", marker_color_circle="#4A628A", marker_color_outside="#6A9AB0")
        #self.__booking_information_manager.set_dropoff_address(self.__geolocator.reverse(coords))
        self.__booking_information_manager.set_pickup_coords(coords)
        self.__verify_markers()
    
    def __remove_pickup_marker(self):
        if self.__pickup_marker is not None:
            self.__pickup_marker.delete()
            self.__pickup_marker = None
            self.__booking_map.delete_all_path()
    
    def __draw_dropoff_marker(self, coords):
        if self.__dropoff_marker is not None:
            self.__dropoff_marker.delete()
        
        self.__dropoff_marker = self.__booking_map.set_marker(coords[0], coords[1], text="Drop-off", marker_color_circle="#16423C", marker_color_outside="#6A9C89")
        #self.__booking_information_manager.set_dropoff_address(self.__geolocator.reverse(coords))
        self.__booking_information_manager.set_dropoff_coords(coords)
        self.__verify_markers()
    
    def __remove_dropoff_marker(self):
        if self.__dropoff_marker is not None:
            self.__dropoff_marker.delete()
            self.__dropoff_marker = None
            self.__booking_map.delete_all_path()
    
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
        __url = f"http://router.project-osrm.org/route/v1/driving/{self.__pickup_lon},{self.__pickup_lat};{self.__dropoff_lon},{self.__dropoff_lat}?overview=full&geometries=geojson"
        __response = requests.get(__url)
        __data = __response.json()

        self.__draw_route_lines(__data)
    
    def __draw_route_lines(self, data):
        __coords = data["routes"][0]["geometry"]["coordinates"]
        __path_latlon = [(lat, lon) for lon, lat in __coords]

        if self.__route_line is not None:
            self.__route_line.delete()
        
        __top_left = (self.__max_lat, self.__min_lon)
        __bottom_right = (self.__min_lat, self.__max_lon)
        
        self.__route_line = self.__booking_map.set_path(__path_latlon)
        self.__booking_information_manager.set_route_line(__path_latlon)

        self.__booking_map.fit_bounding_box(__top_left, __bottom_right)
        self.__booking_information_manager.set_bounding_box(__top_left, __bottom_right)
    
    def __restore_information_from_previous(self):
        __pickup = self.__booking_information_manager.get_pickup_coords()
        __dropoff = self.__booking_information_manager.get_dropoff_coords()
        __bounding_box = self.__booking_information_manager.get_bounding_box()
        __route_line = self.__booking_information_manager.get_route_line()

        if __pickup is not None:
            self.__pickup_marker = self.__booking_map.set_marker(__pickup[0], __pickup[1], text="Pick-up", marker_color_circle="#4A628A", marker_color_outside="#6A9AB0")
        
        if __dropoff is not None:
            self.__dropoff_marker = self.__booking_map.set_marker(__dropoff[0], __dropoff[1], text="Drop-off", marker_color_circle="#16423C", marker_color_outside="#6A9C89")
        
        if __bounding_box != ():
            self.__booking_map.fit_bounding_box(__bounding_box[0], __bounding_box[1])
        
        if __route_line != []:
            self.__route_line = self.__booking_map.set_path(__route_line)
    
    def get_coords_from_address(self, address, marker_type, callback=None):
        __location = self.__geolocator.geocode(address)

        if __location:
            __coords = (__location.latitude, __location.longitude)

            if marker_type == "pickup":
                __location_obj = self.__geolocator.reverse(__coords)
                __full_address = __location_obj.address
                self.__booking_information_manager.set_pickup_address(__full_address)
                self.__booking_information_manager.set_pickup_coords(__coords)
                self.__draw_pickup_marker(__coords)

                if callback:
                    callback(__full_address, marker_type)

            elif marker_type == "dropoff":
                __location_obj = self.__geolocator.reverse(__coords)
                __full_address = __location_obj.address
                self.__booking_information_manager.set_dropoff_address(__full_address)
                self.__booking_information_manager.set_dropoff_coords(__coords)
                self.__draw_dropoff_marker(__coords)

                if callback:
                    callback(__full_address, marker_type)
