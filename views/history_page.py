from customtkinter import *

class HistoryPage(CTkFrame):
    def __init__(self, master, app):
        super().__init__(master)
        self.app = app
        self.pack(fill="both", expand=True)

        self.booking_service = BookingService()
        self.vehicle_service = VehicleService()

        CTkLabel(self, text="Your Ride History", font=("Arial", 24)).pack(pady=20)

        self.history_frame = CTkScrollableFrame(self, width=800, height=400)
        self.history_frame.pack(pady=10, padx=20, fill="both", expand=True)


