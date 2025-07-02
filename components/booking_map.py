from tkintermapview import *
from customtkinter import *

from services.map_manager import MapManager

class BookingMap(CTkFrame):
    """
    Creates the BookingMap GUI and attaches a reference of it to the MapManager
    """

    def __init__(self, master_frame, booking_information_manager):
        super().__init__(master_frame)

        self.booking_information_manager = booking_information_manager
        self.booking_map = TkinterMapView(self)
        self.map_manager = MapManager(self.booking_map, self.booking_information_manager)
        