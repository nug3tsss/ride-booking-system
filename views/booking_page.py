from customtkinter import *
from tkintermapview import *

from components.booking_form import BookingForm
from components.booking_map import BookingMap

class BookingPage(CTkFrame):
    def __init__(self, master, app, booking_information_manager):
        # Initialize booking page
        super().__init__(master)
        self.app = app
        self.booking_information_manager = booking_information_manager
        self.pack(fill="both", expand=True)

        # Add content to the booking page
        self.label = CTkLabel(self, text="", font=("Arial", 32))
        self.label.pack(anchor="w", padx=15, pady=15)

        self.inner_frame = CTkFrame(self)
        self.inner_frame.pack(fill="both", expand=True, padx=15, pady=15)

        self.display_booking_page()
    
    # User will choose pick-up and drop-off locations
    def display_booking_page(self):
        self.label.configure(text="Book your ride!")

        # Create the form
        self.booking_form = BookingForm(self.inner_frame)
        self.booking_form.pack(side=LEFT, fill="both", expand=True, padx=15, pady=15)

        # Create the map
        self.booking_map = BookingMap(self.inner_frame, self.booking_information_manager)
        self.booking_map.pack(side=RIGHT, fill="both", expand=True, padx=15, pady=15)
