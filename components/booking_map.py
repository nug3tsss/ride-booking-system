from tkintermapview import *
from customtkinter import *
from tkinter import *

from services.map_manager import MapManager

class BookingMap(CTkFrame):
    """Contains the BookingMap GUI and passes it to the MapManager"""

    def __init__(self, master_frame, booking_information_manager):
        super().__init__(master_frame)
        self.pack(side=RIGHT, fill="both", expand=True, padx=15, pady=15)

        booking_information_manager = booking_information_manager
        booking_map = TkinterMapView(self)
        self.__map_manager = MapManager(booking_map, booking_information_manager)
    
    def get_map_manager_instance(self):
        return self.__map_manager