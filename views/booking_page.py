from customtkinter import *
from components.navbar import Navbar
from components.booking_map import BookingMap
from services.booking.map_manager import MapManager

# from components.booking_form import BookingForm

class BookingPage(CTkFrame):
    def __init__(self, master, app):
        super().__init__(master)
        self.app = app
        self.pack(fill="both", expand=True)

        # Set up the navbar
        self.navbar = Navbar(self, app)
        self.navbar.pack(side="top", fill="x")

        # Add content to the booking page
        self.label = CTkLabel(self, text="Welcome to the Booking Page!")
        self.label.pack(fill="x", pady=(10, 0), padx=15)

        self.book_destination()
    
    # User will choose pick-up and drop-off locations
    def book_destination(self):
        self.label.configure(text="Select your destination!", anchor=W, font=("Arial", 32))

        # ADD CHANGE TILE SERVER
        
        self.booking_map = BookingMap(self)
        self.map_manager = MapManager(self.booking_map)
        self.map_manager.initialize_map()
        