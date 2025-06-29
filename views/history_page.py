from customtkinter import *
from config.booking import BookingService # Import BookingService
from config.vehicle import VehicleService # Import VehicleService

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

        self.load_history()

    def load_history(self):
        # Clear existing history display
        for widget in self.history_frame.winfo_children():
            widget.destroy()

        # For demonstration, assume a user ID (e.g., 1)
        user_id = 1 
        bookings = self.booking_service.get_user_bookings(user_id)

        if bookings:
            for i, booking in enumerate(bookings):
                # booking tuple: (id, user_id, vehicle_id, pickup_lat, pickup_lon, dropoff_lat, dropoff_lon,
                #                 pickup_address, dropoff_address, distance_km, estimated_time_minutes, fare,
                #                 status, booking_time, completion_time)
                booking_id = booking[0]
                vehicle_id = booking[2]
                pickup_addr = booking[7] if booking[7] else f"Lat: {booking[3]:.4f}, Lon: {booking[4]:.4f}"
                dropoff_addr = booking[8] if booking[8] else f"Lat: {booking[5]:.4f}, Lon: {booking[6]:.4f}"
                distance = booking[9]
                fare = booking[11]
                status = booking[12]
                booking_time = booking[13]

                vehicle_data = self.vehicle_service.get_vehicle_by_id(vehicle_id)
                vehicle_type = vehicle_data[1] if vehicle_data else "Unknown Vehicle"

                booking_details = f"Booking ID: {booking_id}\n" \
                                  f"Vehicle: {vehicle_type}\n" \
                                  f"From: {pickup_addr}\n" \
                                  f"To: {dropoff_addr}\n" \
                                  f"Distance: {distance:.2f} km\n" \
                                  f"Fare: ₱{fare:.2f}\n" \
                                  f"Status: {status.capitalize()}\n" \
                                  f"Booked On: {booking_time}"
                
                CTkLabel(self.history_frame, text=booking_details, justify="left",
                         font=("Arial", 12), wraplength=750).pack(pady=5, padx=10, anchor="w")
                CTkFrame(self.history_frame, height=1, fg_color="gray").pack(fill="x", padx=10, pady=5) # Separator
        else:
            CTkLabel(self.history_frame, text="No ride history found.", font=("Arial", 16)).pack(pady=20)

    def __del__(self):
        # Ensure connections are closed when the page is destroyed
        if hasattr(self, 'booking_service') and self.booking_service:
            self.booking_service.close_connection()
        if hasattr(self, 'vehicle_service') and self.vehicle_service:
            self.vehicle_service.close_connection()

