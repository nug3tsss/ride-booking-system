from tkintermapview import *
from customtkinter import *

class BookingSummaryMap(CTkFrame):
    """
    Displays the map details set from the BookingMap
    """

    def __init__(self, master_frame, booking_information_manager):
        super().__init__(master_frame)
        self.pack(side=RIGHT, fill="both", expand=True, padx=15, pady=15)

        self.__booking_summary_map = TkinterMapView(self)
        self.__booking_information_manager = booking_information_manager
        self.__booking_summary_map.set_tile_server("https://mt0.google.com/vt/lyrs=m&hl=en&x={x}&y={y}&z={z}&s=Ga", max_zoom=22)
        self.__booking_summary_map.pack(expand=True, fill="both", padx=15, pady=15)

        self.__display_map_details()
    
    def __display_map_details(self):
        __pickup = self.__booking_information_manager.get_pickup_coords()
        __dropoff = self.__booking_information_manager.get_dropoff_coords()
        __bounding_box = self.__booking_information_manager.get_bounding_box()
        __route_line = self.__booking_information_manager.get_route_line()

        if __pickup is not None:
            self.__pickup_marker = self.__booking_summary_map.set_marker(__pickup[0], __pickup[1], text="Pick-up destination")
        
        if __dropoff is not None:
            self.__dropoff_marker = self.__booking_summary_map.set_marker(__dropoff[0], __dropoff[1], text="Pick-up destination")
        
        if __bounding_box != ():
            self.__booking_summary_map.fit_bounding_box(__bounding_box[0], __bounding_box[1])
        
        if __route_line != []:
            self.__route_line = self.__booking_summary_map.set_path(__route_line)
    