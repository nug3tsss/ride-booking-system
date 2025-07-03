from customtkinter import *

class BookingSummaryForm(CTkFrame):
    """Contains booking summary from BookingForm with confirmation button"""

    def __init__(self, master_frame, booking_information_manager):
        super().__init__(master_frame, corner_radius=15, fg_color=("#2d4059"))
        self.pack(side=LEFT, fill="both", expand=True, padx=15, pady=15)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=2)

        self.__booking_information_manager = booking_information_manager

        # if vehicle_type_int is not None:
        #     vehicle_category = ""
        #     if vehicle_type_int == 1:
        #         vehicle_category = "Car"
        #     elif vehicle_type_int == 2:
        #         vehicle_category = "Van"
        #     elif vehicle_type_int == 3:
        #         vehicle_category = "Motorcycle"

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
        self.__pickup_address = self.__booking_information_manager.get_pickup_address()
        self.__dropoff_address = self.__booking_information_manager.get_dropoff_address()
        self.__vehicle_type_str = self.__booking_information_manager.get_vehicle_type_str()
        self.__vehicle_type_int = self.__booking_information_manager.get_vehicle_type_int()
        self.__vehicle_details = self.__booking_information_manager.get_vehicle_details()
        self.__distance_km = self.__booking_information_manager.get_distance_km()
        self.__estimated_time_seconds = self.__booking_information_manager.get_estimated_time_seconds()
        self.__estimated_cost_pesos = self.__booking_information_manager.get_estimated_cost()
    
    def __calculate_time_in_mins(self):
        self.__estimated_time_minutes = int(self.__estimated_time_seconds // 60)
    
    def __create_booking_summary_label(self):
        title_label = CTkLabel(self, text="Booking Summary", font=("Arial", 30, "bold"), text_color="#F6D55C")
        title_label.grid(row=0, column=0, columnspan=2, pady=(20, 30), sticky="ew")
    
    def __create_pickup_section(self):
        pickup_frame = CTkFrame(self, corner_radius=10, fg_color=("#1e1b18"))
        pickup_frame.grid(row=1, column=0, columnspan=2, sticky="ew", padx=20, pady=(0, 15))
        pickup_frame.grid_columnconfigure(1, weight=1)

        CTkLabel(pickup_frame, text="Pickup Location:", font=("Arial", 16, "bold"), text_color="#70d6ff").grid(row=0, column=0, sticky="w", padx=15, pady=(15, 5))
        CTkLabel(pickup_frame, text=self.__pickup_address, font=("Arial", 14), wraplength=600).grid(row=0, column=1, sticky="w", padx=(10, 15), pady=(15, 5))

    def __create_dropoff_section(self):
        dropoff_frame = CTkFrame(self, corner_radius=10, fg_color=("#1e1b18"))
        dropoff_frame.grid(row=2, column=0, columnspan=2, sticky="ew", padx=20, pady=(0, 15))
        dropoff_frame.grid_columnconfigure(1, weight=1)

        CTkLabel(dropoff_frame, text="Dropoff Location:", font=("Arial", 16, "bold"), text_color="#70d6ff").grid(row=0, column=0, sticky="w", padx=15, pady=(15, 5))
        CTkLabel(dropoff_frame, text=self.__dropoff_address, font=("Arial", 14), wraplength=600).grid(row=0, column=1, sticky="w", padx=(10, 15), pady=(15, 5))

    def __create_ride_details_section(self):
        vehicle_frame = CTkFrame(self, corner_radius=10, fg_color=("#1e1b18"))
        vehicle_frame.grid(row=3, column=0, columnspan=2, sticky="ew", padx=20, pady=(0, 15))
        vehicle_frame.grid_columnconfigure(0, weight=1)
        vehicle_frame.grid_columnconfigure(1, weight=1)
        vehicle_frame.grid_columnconfigure(2, weight=1)
        vehicle_frame.grid_columnconfigure(3, weight=1)

        CTkLabel(vehicle_frame, text="Ride Information:", font=("Arial", 16, "bold"), text_color="#70d6ff").grid(row=0, column=0, columnspan=4, sticky="w", padx=15, pady=(15, 10))

        if self.__vehicle_details:
            # Vehicle info in a 2x4 grid within the vehicle frame
            CTkLabel(vehicle_frame, text="Type:", font=("Arial", 14, "bold")).grid(row=1, column=0, sticky="w", padx=(30, 10), pady=2)
            CTkLabel(vehicle_frame, text=self.__vehicle_details.get('type', 'N/A'), font=("Arial", 14)).grid(row=1, column=1, sticky="w", padx=(0, 20), pady=2)
            
            CTkLabel(vehicle_frame, text="Model:", font=("Arial", 14, "bold")).grid(row=1, column=2, sticky="w", padx=(20, 10), pady=2)
            CTkLabel(vehicle_frame, text=self.__vehicle_details.get('model', 'N/A'), font=("Arial", 14)).grid(row=1, column=3, sticky="w", pady=2)
            
            CTkLabel(vehicle_frame, text="License Plate:", font=("Arial", 14, "bold")).grid(row=2, column=0, sticky="w", padx=(30, 10), pady=2)
            CTkLabel(vehicle_frame, text=self.__vehicle_details.get('license_plate', 'N/A'), font=("Arial", 14)).grid(row=2, column=1, sticky="w", padx=(0, 20), pady=2)
            
            CTkLabel(vehicle_frame, text="Driver:", font=("Arial", 14, "bold")).grid(row=2, column=2, sticky="w", padx=(20, 10), pady=(2, 15))
            CTkLabel(vehicle_frame, text=self.__vehicle_details.get('driver_name', 'N/A'), font=("Arial", 14)).grid(row=2, column=3, sticky="w", pady=(2, 15))

    def __create_trip_details_section(self): 
        trip_frame = CTkFrame(self, corner_radius=10, fg_color=("#1e1b18"))
        trip_frame.grid(row=4, column=0,columnspan =1, sticky="ew", padx=(20, 30), pady=(0, 15))

        CTkLabel(trip_frame, text="  Distance  ", font=("Arial", 14, "bold"), text_color="#70d6ff").grid(row=0, column=0, pady=(15, 5))
        CTkLabel(trip_frame, text=f"{self.__distance_km:.2f} km", font=("Arial", 16, "bold")).grid(row=1, column=0, pady=(0, 15))

        CTkLabel(trip_frame, text="Est. Time ", font=("Arial", 14, "bold"), text_color="#70d6ff").grid(row=0, column=1, pady=(15, 5))
        CTkLabel(trip_frame, text=f"{self.__estimated_time_minutes} min", font=("Arial", 16, "bold")).grid(row=1, column=1, pady=(0, 15))

    def __create_costs_section(self):
        cost_frame = CTkFrame(self, corner_radius=15, fg_color=("#d8315b"))
        cost_frame.grid(row=4, column=1, sticky="ew", padx=20, pady=(0, 5))

        CTkLabel(cost_frame, text="  Total Estimated Cost", font=("Arial", 18, "bold"), text_color="#70d6ff").grid(row=0, column=0, pady=(15, 5))
        CTkLabel(cost_frame, text=f"₱ {self.__estimated_cost_pesos:.2f}", font=("Arial", 28, "bold"), text_color="#70d6ff").grid(row=1, column=0, pady=(0, 15))

    def __create_confirm_button(self):
        confirm_button = CTkButton(self, text="Confirm Booking", command=self.__confirm_booking, corner_radius=15, fg_color=("#d8315b"), width=150, height=100)
        confirm_button.grid(row=6, column=0, columnspan=2, pady=(20, 20), padx=20, sticky="ew")
    
    def __confirm_booking(self):
        print("Booking confirmed!")