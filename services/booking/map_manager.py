from services.booking.pin_location_manager import PinLocationManager

class MapManager():
    def __init__(self, booking_map):
        self.booking_map = booking_map
        self.pin_location_manager = PinLocationManager(booking_map)

        # self.booking_map.set_tile_server("https://mt0.google.com/vt/lyrs=m&hl=en&x={x}&y={y}&z={z}&s=Ga", max_zoom=22)
        self.booking_map.set_tile_server("https://a.tile.openstreetmap.org/{z}/{x}/{y}.png")

    def initialize_map(self):
        

        self.booking_map.set_position(14.599036510236097, 121.00494831003196)
        self.booking_map.set_zoom(16)

        self.add_marker_of_type()

        self.booking_map.pack(expand=True, fill="both", padx=15, pady=15)
    
    def test(self, coords):
        self.booking_map.set_marker(coords[0], coords[1], text="Pick-up destination")
    
    def add_marker_of_type(self):
        self.booking_map.add_right_click_menu_command(label="Select destination as pick-up", command=self.pin_location_manager.add_pickup_marker, pass_coords=True)
        self.booking_map.add_right_click_menu_command(label="Select destination as drop-off", command=self.pin_location_manager.add_dropoff_marker, pass_coords=True)