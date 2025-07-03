from tkintermapview import *
from customtkinter import *

class BookingSummaryMap(CTkFrame):
    """Displays the map details set from the BookingMap"""

    def __init__(self, master_frame, booking_information_manager):
        super().__init__(master_frame)
        self.pack(side=RIGHT, fill="both", expand=True, padx=15, pady=15)

        self.__booking_information_manager = booking_information_manager
        self.__booking_summary_map = TkinterMapView(self)

        self.__booking_summary_map.set_tile_server("https://mt0.google.com/vt/lyrs=m&hl=en&x={x}&y={y}&z={z}&s=Ga", max_zoom=22)
        self.__booking_summary_map.pack(expand=True, fill="both", padx=15, pady=15)

        self.__display_map_details()
    
    def __display_map_details(self):
        pickup = self.__booking_information_manager.get_pickup_coords()
        dropoff = self.__booking_information_manager.get_dropoff_coords()
        bounding_box = self.__booking_information_manager.get_bounding_box()
        route_line = self.__booking_information_manager.get_route_line()

        if pickup is not None:
            self.__booking_summary_map.set_marker(pickup[0], pickup[1], text="Pick-up", marker_color_circle="#4A628A", marker_color_outside="#6A9AB0")
        
        if dropoff is not None:
            self.__booking_summary_map.set_marker(dropoff[0], dropoff[1], text="Drop-off", marker_color_circle="#16423C", marker_color_outside="#6A9C89")
        
        if bounding_box != ():
            self.__booking_summary_map.fit_bounding_box(bounding_box[0], bounding_box[1])
        
        if route_line != []:
            self.__booking_summary_map.set_path(route_line)
    