from customtkinter import *
from tkinter import *
from tkinter import messagebox
from database.db_handler import DatabaseHandler

class BookingSummaryForm(CTkFrame):
    """Contains booking summary from BookingForm with confirmation button"""

    def __init__(self, master_frame, app, booking_information_manager):
        super().__init__(master_frame, corner_radius=15, fg_color="#2d4059")
        self.pack(side=LEFT, fill="both", expand=True, padx=15, pady=15)

        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure(2, weight=1)

        self.__booking_information_manager = booking_information_manager
        self.__app = app
        self.__db_handler = DatabaseHandler()

        self.__booking_after_ids = []
        
        self.__is_booking_in_progress = False

        self.__current_booking_id = None

        self.__retrieve_booking_informations()
        self.__calculate_time_in_mins()

        self.__create_booking_summary_label()
        self.__create_pickup_section()
        self.__create_dropoff_section()
        self.__create_ride_details_section()
        self.__create_trip_details_section()
        self.__create_costs_section()
        self.__create_confirm_button()

    def __retrieve_booking_informations(self):
        self.__pickup_address = (self.__booking_information_manager.get_pickup_address())
        self.__dropoff_address = (self.__booking_information_manager.get_dropoff_address())
        self.__vehicle_type_str = self.__booking_information_manager.get_vehicle_type_str()
        self.__vehicle_type_int = self.__booking_information_manager.get_vehicle_type_int()
        self.__vehicle_details = self.__booking_information_manager.get_vehicle_details()
        self.__distance_km = self.__booking_information_manager.get_distance_km()
        self.__estimated_time_seconds = self.__booking_information_manager.get_estimated_time_seconds()
        self.__estimated_cost_pesos = self.__booking_information_manager.get_estimated_cost()

    def __calculate_time_in_mins(self):
        self.__estimated_time_minutes = int(self.__estimated_time_seconds // 60)

    def __create_booking_summary_label(self):
        self.__title_label = CTkLabel(self, text="Booking Summary", font=("Arial", 30, "bold"), text_color="#F6D55C")
        self.__title_label.grid(row=0, column=0, columnspan=3, pady=30, sticky="ew")

    def __create_pickup_section(self):
        pickup_frame = CTkFrame(self, corner_radius=10, fg_color="#1e1b18")
        pickup_frame.grid(row=1, column=0, columnspan=3, sticky="ew", padx=20, pady=10)
        pickup_frame.grid_columnconfigure(1, weight=1)

        CTkLabel(pickup_frame, text="Pickup Location:", font=("Arial", 16, "bold"), text_color="#70d6ff").grid(row=0, column=0, sticky="w", padx=15, pady=15)
        CTkLabel(pickup_frame, text=self.__pickup_address, font=("Arial", 14), wraplength=600).grid(row=0, column=1, sticky="w", padx=(10, 15), pady=15)

    def __create_dropoff_section(self):
        dropoff_frame = CTkFrame(self, corner_radius=10, fg_color="#1e1b18")
        dropoff_frame.grid(row=2, column=0, columnspan=3, sticky="ew", padx=20, pady=10)
        dropoff_frame.grid_columnconfigure(1, weight=1)

        CTkLabel(dropoff_frame, text="Dropoff Location:", font=("Arial", 16, "bold"), text_color="#70d6ff").grid(row=0, column=0, sticky="w", padx=15, pady=15)
        CTkLabel(dropoff_frame, text=self.__dropoff_address, font=("Arial", 14), wraplength=600).grid(row=0, column=1, sticky="w", padx=(10, 15), pady=15)

    def __create_ride_details_section(self):
        self.__vehicle_frame = CTkFrame(self, corner_radius=10, fg_color="#1e1b18")
        self.__vehicle_frame.grid_columnconfigure(0, weight=1)
        self.__vehicle_frame.grid_columnconfigure(1, weight=1)
        self.__vehicle_frame.grid_columnconfigure(2, weight=1)
        self.__vehicle_frame.grid_columnconfigure(3, weight=1)

        CTkLabel(self.__vehicle_frame, text="Ride Information:", font=("Arial", 16, "bold"), text_color="#70d6ff").grid(row=0, column=0, columnspan=4, sticky="w", padx=15, pady=(15, 10))

        if self.__vehicle_details:
            CTkLabel(self.__vehicle_frame, text="Type:", font=("Arial", 14, "bold")).grid(row=1, column=0, sticky="w", padx=(30, 10), pady=2)
            CTkLabel(self.__vehicle_frame, text=self.__vehicle_details.get('type', 'N/A'), font=("Arial", 14)).grid(row=1, column=1, sticky="w", padx=(0, 20), pady=2)
            
            CTkLabel(self.__vehicle_frame, text="Model:", font=("Arial", 14, "bold")).grid(row=1, column=2, sticky="w", padx=(20, 10), pady=2)
            CTkLabel(self.__vehicle_frame, text=self.__vehicle_details.get('model', 'N/A'), font=("Arial", 14)).grid(row=1, column=3, sticky="w", pady=2)
            
            CTkLabel(self.__vehicle_frame, text="License Plate:", font=("Arial", 14, "bold")).grid(row=2, column=0, sticky="w", padx=(30, 10), pady=2)
            CTkLabel(self.__vehicle_frame, text=self.__vehicle_details.get('license_plate', 'N/A'), font=("Arial", 14)).grid(row=2, column=1, sticky="w", padx=(0, 20), pady=2)
            
            CTkLabel(self.__vehicle_frame, text="Driver:", font=("Arial", 14, "bold")).grid(row=2, column=2, sticky="w", padx=(20, 10), pady=(2, 15))
            CTkLabel(self.__vehicle_frame, text=self.__vehicle_details.get('driver_name', 'N/A'), font=("Arial", 14)).grid(row=2, column=3, sticky="w", pady=(2, 15))

    def __create_trip_details_section(self):
        # Distance Frame (Column 0)
        distance_frame = CTkFrame(self, corner_radius=10, fg_color="#1e1b18")
        distance_frame.grid(row=3, column=0, sticky="nsew", padx=20, pady=15)
        distance_frame.grid_columnconfigure(0, weight=1)

        CTkLabel(distance_frame, text="Distance", font=("Arial", 14, "bold"), text_color="#70d6ff", anchor="center").grid(row=0, column=0, pady=(15, 5), padx=10, sticky="ew")
        CTkLabel(distance_frame, text=f"{self.__distance_km:.2f} km", font=("Arial", 16, "bold"), anchor="center").grid(row=1, column=0, pady=(5, 15), padx=10, sticky="ew")

        # ETA Frame (Column 1)
        eta_frame = CTkFrame(self, corner_radius=10, fg_color="#1e1b18")
        eta_frame.grid(row=3, column=1, sticky="nsew", padx=20, pady=15)
        eta_frame.grid_columnconfigure(0, weight=1)

        CTkLabel(eta_frame, text="ETA", font=("Arial", 14, "bold"), text_color="#70d6ff", anchor="center").grid(row=0, column=0, pady=(15, 5), padx=10, sticky="ew")
        CTkLabel(eta_frame, text=f"{self.__estimated_time_minutes} min", font=("Arial", 16, "bold"), anchor="center").grid(row=1, column=0, pady=(5, 15), padx=10, sticky="ew")

    def __create_costs_section(self):
        cost_frame = CTkFrame(self, corner_radius=15, fg_color="#d8315b")
        cost_frame.grid(row=3, column=2, sticky="nsew", padx=20, pady=15)
        cost_frame.grid_columnconfigure(0, weight=1)

        CTkLabel(cost_frame, text="Total Estimated Cost", font=("Arial", 18, "bold"), text_color="#70d6ff", anchor="center").grid(row=0, column=0, pady=(15, 5), sticky="ew")
        CTkLabel(cost_frame, text=f"₱ {self.__estimated_cost_pesos:.2f}", font=("Arial", 28, "bold"), text_color="#70d6ff", anchor="center").grid(row=1, column=0, pady=(0, 15), sticky="ew")

    def __create_confirm_button(self):
        self.__confirm_button = CTkButton(self, text="Confirm Booking", command=self.__confirm_booking, corner_radius=15, fg_color="#d8315b", width=150, height=100)
        self.__confirm_button.grid(row=5, column=0, columnspan=3, pady=(20, 20), padx=20, sticky="ew")

    def __confirm_booking(self):
        if self.__is_booking_in_progress:
            return
        
        pickup = self.__booking_information_manager.get_pickup_address()
        destination = self.__booking_information_manager.get_dropoff_address()
        vehicle_details = self.__booking_information_manager.get_vehicle_details()
        distance_km = self.__booking_information_manager.get_distance_km()
        estimated_cost = self.__booking_information_manager.get_estimated_cost()
        
        vehicle_id = vehicle_details.get('id')

        user_name = "Guest"
        if hasattr(self.master.master.master, 'app') and self.master.master.master.app.current_user:
            user_name = self.master.master.master.app.current_user.get('username', 'Guest')

        self.__current_booking_id = self.__db_handler.add_booking(
            name=user_name,
            pickup=pickup,
            destination=destination,
            vehicle_id=vehicle_id,
            distance_km=distance_km,
            estimated_cost=estimated_cost
        )

        if self.__current_booking_id is None:
            print("Error", "Failed to create booking in the database.")
            return
        
        print("Booking Initiated", f"Booking ID {self.__current_booking_id} has been initiated.")
        
        self.__is_booking_in_progress = True
        self.__confirm_button.configure(text="Cancel Booking", command=self.__cancel_booking_process)

        self.__title_label.configure(text="Booking your ride...")
        confirm_id = self.after(5000, self.__finding_driver)
        self.__booking_after_ids.append(confirm_id)

    def __finding_driver(self):
        self.__title_label.configure(text="Finding a driver...")
        finding_id = self.after(5000, self.__driver_found)
        self.__booking_after_ids.append(finding_id)

    def __driver_found(self):
        if self.__current_booking_id:
            self.__db_handler.complete_booking(self.__current_booking_id)
            print("Booking Complete", f"Booking ID {self.__current_booking_id} is now completed!")
        self.__title_label.configure(text="Driver found!")
        self.__vehicle_frame.grid(row=4, column=0, columnspan=3, sticky="ew", padx=20, pady=85)

        self.__confirm_button.grid_forget()

        self.__cancel_button = CTkButton(self, text="Cancel Booking", command=self.__cancel_booking, corner_radius=15, fg_color="#d8315b", width=150, height=100)
        self.__cancel_button.grid(row=6, column=0, columnspan=1, pady=(20, 20), padx=20, sticky="ew")

        self.__go_to_bookings_button = CTkButton(self, text="Go to your bookings", command=self.__go_to_your_bookings, corner_radius=15, fg_color="#d8315b", width=150, height=100)
        self.__go_to_bookings_button.grid(row=6, column=1, columnspan=2, pady=(20, 20), padx=20, sticky="ew")

        self.__is_booking_in_progress = False
        self.__booking_after_ids.clear()
        self.__current_booking_id = None

    def __cancel_booking_process(self):
        for after_id in self.__booking_after_ids:
            self.after_cancel(after_id)

        self.__booking_after_ids.clear()
        self.__is_booking_in_progress = False


        #Mark ooking as cancelled in the database
        if self.__current_booking_id:
            self.__db_handler.cancel_booking(self.__current_booking_id)
            print("Booking Cancelled", f"Booking ID {self.__current_booking_id} has been cancelled.")
            self.__current_booking_id = None # Reset current booking ID

        self.__title_label.configure(text="Booking summary")
        self.__confirm_button.configure(text="Confirm Booking", command=self.__confirm_booking)

    def __cancel_booking(self):
        if self.__current_booking_id:
            self.__db_handler.cancel_booking(self.__current_booking_id)
            messagebox.showinfo("Booking Cancelled", f"Booking ID {self.__current_booking_id} has been cancelled.")
            self.__current_booking_id = None

    def __go_to_your_bookings(self):
        print("Navigating to your bookings.")
        self.__app.show_page("History")
