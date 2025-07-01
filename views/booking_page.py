from customtkinter import *
from tkintermapview import *
from services.map_manager import MapManager

class BookingPage(CTkFrame):
    def __init__(self, master, app):
        super().__init__(master)
        self.app = app
        self.pack(fill="both", expand=True)

        # Add content to the booking page
        self.label = CTkLabel(self, text="", font=("Arial", 32))
        self.label.pack(anchor="w", padx=15, pady=15)

        self.secondary_frame = CTkFrame(self)
        self.secondary_frame.pack(fill="both", expand=True, padx=15, pady=15)

        self.display_booking_page()
    
    # User will choose pick-up and drop-off locations
    def display_booking_page(self):
        self.label.configure(text="Select your destination!")

        # ----- LEFT AND RIGHT FRAMES -----
        self.map_frame = CTkFrame(self.secondary_frame)
        self.map_frame.pack(side=RIGHT, fill="both", expand=True, padx=15, pady=15)

        self.prompts_frame = CTkFrame(self.secondary_frame)
        self.prompts_frame.pack(side=LEFT, fill="both", expand=True, padx=15, pady=15)

        # ----- CREATE THE PROMPTS -----
        self.is_prompt_active = False

        self.select_vehicle_button = CTkButton(self.prompts_frame, text="Select a vehicle", anchor="w", font=("Arial", 32), command=self.toggle_prompt)
        self.select_vehicle_button.pack(fill="x", pady=15, padx=15)

        self.select_vehicle_frame = CTkFrame(self.prompts_frame)

        self.vehicle_var = IntVar(value=0)
        self.vehicle1 = CTkRadioButton(self.select_vehicle_frame, text="Vehicle 1", variable=self.vehicle_var, value=1)
        self.vehicle2 = CTkRadioButton(self.select_vehicle_frame, text="Vehicle 2", variable=self.vehicle_var, value=2)
        self.vehicle3 = CTkRadioButton(self.select_vehicle_frame, text="Vehicle 3", variable=self.vehicle_var, value=3)
        self.vehicle1.pack(fill="x", pady=15, padx=15)
        self.vehicle2.pack(fill="x", pady=15, padx=15)
        self.vehicle3.pack(fill="x", pady=15, padx=15)

        # ----- GENERATE THE MAP -----
        self.booking_map = TkinterMapView(self.map_frame)
        self.map_manager = MapManager(self.booking_map)
        self.map_manager.initialize_map()
    
    def toggle_prompt(self):
        if self.is_prompt_active:
            self.select_vehicle_frame.pack_forget()
            self.is_prompt_active = False
        else:
            self.select_vehicle_frame.pack(fill="x", pady=5, padx=15, after=self.select_vehicle_button)
            self.is_prompt_active = True
        