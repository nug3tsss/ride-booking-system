import requests
from geopy import geocoders

class MapManager():
    def __init__(self, booking_map, booking_information_manager):
        self._booking_map = booking_map
        self._booking_information_manager = booking_information_manager

        self._pickup_marker = None
        self._dropoff_marker = None
        self._route_line = None

        self._booking_map.set_tile_server("https://mt0.google.com/vt/lyrs=m&hl=en&x={x}&y={y}&z={z}&s=Ga", max_zoom=22)
        self._booking_map.set_position(14.599036510236097, 121.00494831003196)
        self._booking_map.set_zoom(16)
        self._booking_map.add_right_click_menu_command(label="Select destination as pick-up", command=self._draw_pickup_marker, pass_coords=True)
        self._booking_map.add_right_click_menu_command(label="Select destination as drop-off", command=self._draw_dropoff_marker, pass_coords=True)
        self._booking_map.pack(expand=True, fill="both", padx=15, pady=15)

        self._restore_information_from_previous()
    
    def _draw_pickup_marker(self, coords):
        if self._pickup_marker is not None:
            self._pickup_marker.delete()
        
        self._pickup_marker = self._booking_map.set_marker(coords[0], coords[1], text="Pick-up destination")
        self._booking_information_manager.set_pickup_information(coords)
        self._verify_markers()
    
    def _draw_dropoff_marker(self, coords):
        if self._dropoff_marker is not None:
            self._dropoff_marker.delete()
        
        self._dropoff_marker = self._booking_map.set_marker(coords[0], coords[1], text="Drop-off destination")
        self._booking_information_manager.set_dropoff_information(coords)
        self._verify_markers()
    
    def _verify_markers(self):
        if self._pickup_marker is not None and self._dropoff_marker is not None:
            self._set_marker_coords()
            self._set_marker_minmax_coords()
            self._calculate_route_lines()
    
    def _set_marker_coords(self):
        self._pickup_lat = self._pickup_marker.position[0]
        self._pickup_lon = self._pickup_marker.position[1]
        self._dropoff_lat = self._dropoff_marker.position[0]
        self._dropoff_lon = self._dropoff_marker.position[1]
    
    def _set_marker_minmax_coords(self):
        self._min_lat = min(self._pickup_lat, self._dropoff_lat)
        self._max_lat = max(self._pickup_lat, self._dropoff_lat)
        self._min_lon = min(self._pickup_lon, self._dropoff_lon)
        self._max_lon = max(self._pickup_lon, self._dropoff_lon)
    
    def _calculate_route_lines(self):
        _url = f"http://router.project-osrm.org/route/v1/driving/{self._pickup_lon},{self._pickup_lat};{self._dropoff_lon},{self._dropoff_lat}?overview=full&geometries=geojson"
        _response = requests.get(_url)
        _data = _response.json()

        self._draw_route_lines(_data)
    
    def _draw_route_lines(self, data):
        _coords = data["routes"][0]["geometry"]["coordinates"]
        _path_latlon = [(lat, lon) for lon, lat in _coords]

        if self._route_line is not None:
            self._route_line.delete()
        
        self._route_line = self._booking_map.set_path(_path_latlon)
        self._booking_map.fit_bounding_box((self._max_lat, self._min_lon), (self._min_lat, self._max_lon))
    
    def _restore_information_from_previous(self):
        if self._booking_information_manager.pickup_coords is not None:
            self._draw_pickup_marker(self._booking_information_manager.pickup_coords)
        
        if self._booking_information_manager.dropoff_coords is not None:
            self._draw_dropoff_marker(self._booking_information_manager.dropoff_coords)
