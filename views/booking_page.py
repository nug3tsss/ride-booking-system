from customtkinter import *
from tkintermapview import *

from components.booking_form import BookingForm
from components.booking_map import BookingMap
from components.booking_summary_map import BookingSummaryMap

class BookingPage(CTkFrame):
    """
    Stores booking form, booking map, and booking summary and confirmation
    """

    def __init__(self, master, app):
        super().__init__(master)
        self.pack(fill="both", expand=True)

        self.__booking_information_manager = app.booking_information_manager
        self.__booking_label = CTkLabel(self, text="", font=("Arial", 32))
        self.__booking_label.pack(anchor="w", padx=15, pady=15)

        self.__booking_inner_frame = CTkFrame(self)
        self.__booking_inner_frame.pack(fill="both", expand=True, padx=15)

        self.__current_section = self.__booking_information_manager.get_current_booking_section()
        self.__button = CTkButton(self, command=self.__change_section)
        self.__button.pack(side=LEFT, padx=15, pady=15)

        self.__display_current_section()
    
    def __display_booking_section(self):
        self.__booking_label.configure(text="Book your ride!")
        self.__current_section = "Booking"
        self.__booking_information_manager.set_current_booking_section(self.__current_section)
        
        self.__button.configure(text="Next")

        self.__booking_map = BookingMap(self.__booking_inner_frame, self.__booking_information_manager)
        self.__booking_form = BookingForm(self.__booking_inner_frame, self.__booking_map.get_map_manager_instance(), self.__booking_information_manager)
    
    def __display_summary_section(self):
        self.__booking_label.configure(text="")
        self.__current_section = "Summary"
        self.__booking_information_manager.set_current_booking_section(self.__current_section)
        self.__button.configure(text="Go Back")

        self.__summary_form = CTkFrame(self.__booking_inner_frame, corner_radius=15, fg_color=("#2d4059"))
        self.__summary_form.pack(side=LEFT, fill="x", expand=True, padx=15, pady=15)

        self.__summary_form.grid_columnconfigure(0, weight=1)
        self.__summary_form.grid_columnconfigure(1, weight=2)

        title_label = CTkLabel(self.__summary_form, text="Booking Summary", 
                            font=("Arial", 30, "bold"), text_color="#F6D55C")
        title_label.grid(row=0, column=0, columnspan=2, pady=(20, 30), sticky="ew")

        self.__summary_map = BookingSummaryMap(self.__booking_inner_frame, self.__booking_information_manager)

        # Retrieve booking information
        pickup_address = self.__booking_information_manager.get_pickup_address()
        dropoff_address = self.__booking_information_manager.get_dropoff_address()

        vehicle_type_str = self.__booking_information_manager.get_vehicle_type_str()
        vehicle_type_int = self.__booking_information_manager.get_vehicle_type_int()
        vehicle_details = self.__booking_information_manager.get_vehicle_details()

        distance_km = self.__booking_information_manager.get_distance_km()

        estimated_time_seconds = self.__booking_information_manager.get_estimated_time_seconds()
        estimated_time_minutes = int(estimated_time_seconds // 60)
        estimated_cost_pesos = self.__booking_information_manager.get_estimated_cost_pesos()

        if vehicle_type_int is not None:
            vehicle_category = ""
            if vehicle_type_int == 1:
                vehicle_category = "Car"
            elif vehicle_type_int == 2:
                vehicle_category = "Van"
            elif vehicle_type_int == 3:
                vehicle_category = "Motorcycle"
                
        # Pickup Section
        pickup_frame = CTkFrame(self.__summary_form, corner_radius=10, fg_color=("#1e1b18"))
        pickup_frame.grid(row=1, column=0, columnspan=2, sticky="ew", padx=20, pady=(0, 15))
        pickup_frame.grid_columnconfigure(1, weight=1)

        CTkLabel(pickup_frame, text="Pickup Location:", 
                font=("Arial", 16, "bold"), text_color="#70d6ff").grid(row=0, column=0, sticky="w", padx=15, pady=(15, 5))
        CTkLabel(pickup_frame, text=pickup_address, 
                font=("Arial", 14), wraplength=600).grid(row=0, column=1, sticky="w", padx=(10, 15), pady=(15, 5))

        # Dropoff Section
        dropoff_frame = CTkFrame(self.__summary_form, corner_radius=10, fg_color=("#1e1b18"))
        dropoff_frame.grid(row=2, column=0, columnspan=2, sticky="ew", padx=20, pady=(0, 15))
        dropoff_frame.grid_columnconfigure(1, weight=1)

        CTkLabel(dropoff_frame, text="Dropoff Location:", 
                font=("Arial", 16, "bold"), text_color="#70d6ff").grid(row=0, column=0, sticky="w", padx=15, pady=(15, 5))
        CTkLabel(dropoff_frame, text=dropoff_address, 
                font=("Arial", 14), wraplength=600).grid(row=0, column=1, sticky="w", padx=(10, 15), pady=(15, 5))

        # Ride Details Section
        vehicle_frame = CTkFrame(self.__summary_form, corner_radius=10, fg_color=("#1e1b18"))
        vehicle_frame.grid(row=3, column=0, columnspan=2, sticky="ew", padx=20, pady=(0, 15))
        vehicle_frame.grid_columnconfigure(0, weight=1)
        vehicle_frame.grid_columnconfigure(1, weight=1)
        vehicle_frame.grid_columnconfigure(2, weight=1)
        vehicle_frame.grid_columnconfigure(3, weight=1)

        CTkLabel(vehicle_frame, text="Ride Information:", 
                font=("Arial", 16, "bold"), text_color="#70d6ff").grid(row=0, column=0, columnspan=4, sticky="w", padx=15, pady=(15, 10))

        if vehicle_details:
            # Vehicle info in a 2x4 grid within the vehicle frame
            CTkLabel(vehicle_frame, text="Type:", font=("Arial", 14, "bold")).grid(row=1, column=0, sticky="w", padx=(30, 10), pady=2)
            CTkLabel(vehicle_frame, text=vehicle_details.get('type', 'N/A'), font=("Arial", 14)).grid(row=1, column=1, sticky="w", padx=(0, 20), pady=2)
            
            CTkLabel(vehicle_frame, text="Model:", font=("Arial", 14, "bold")).grid(row=1, column=2, sticky="w", padx=(20, 10), pady=2)
            CTkLabel(vehicle_frame, text=vehicle_details.get('model', 'N/A'), font=("Arial", 14)).grid(row=1, column=3, sticky="w", pady=2)
            
            CTkLabel(vehicle_frame, text="License Plate:", font=("Arial", 14, "bold")).grid(row=2, column=0, sticky="w", padx=(30, 10), pady=2)
            CTkLabel(vehicle_frame, text=vehicle_details.get('license_plate', 'N/A'), font=("Arial", 14)).grid(row=2, column=1, sticky="w", padx=(0, 20), pady=2)
            
            CTkLabel(vehicle_frame, text="Driver:", font=("Arial", 14, "bold")).grid(row=2, column=2, sticky="w", padx=(20, 10), pady=(2, 15))
            CTkLabel(vehicle_frame, text=vehicle_details.get('driver_name', 'N/A'), font=("Arial", 14)).grid(row=2, column=3, sticky="w", pady=(2, 15))
        else:
            CTkLabel(vehicle_frame, text="  No vehicle selected", 
                    font=("Arial", 12), text_color="#70d6ff").grid(row=1, column=0, columnspan=4, sticky="w", padx=30, pady=(0, 15))

        # Trip Details Section 
        trip_frame = CTkFrame(self.__summary_form, corner_radius=10, fg_color=("#1e1b18"))
        trip_frame.grid(row=4, column=0,columnspan =1, sticky="ew", padx=(20, 30), pady=(0, 15))

        CTkLabel(trip_frame, text="  Distance  ", 
                font=("Arial", 14, "bold"), text_color="#70d6ff").grid(row=0, column=0, pady=(15, 5))
        CTkLabel(trip_frame, text=f"{distance_km:.2f} km", 
                font=("Arial", 16, "bold")).grid(row=1, column=0, pady=(0, 15))

        CTkLabel(trip_frame, text="Est. Time ", 
                font=("Arial", 14, "bold"), text_color="#70d6ff").grid(row=0, column=1, pady=(15, 5))
        CTkLabel(trip_frame, text=f"{estimated_time_minutes} min", 
                font=("Arial", 16, "bold")).grid(row=1, column=1, pady=(0, 15))

        # Cost Section 
        cost_frame = CTkFrame(self.__summary_form, corner_radius=15, fg_color=("#d8315b"))
        cost_frame.grid(row=4, column=1, sticky="ew", padx=20, pady=(0, 5))

        CTkLabel(cost_frame, text="  Total Estimated Cost", font=("Arial", 18, "bold"), text_color="#70d6ff").grid(row=0, column=0, pady=(15, 5))
        CTkLabel(cost_frame, text=f"₱ {estimated_cost_pesos:.2f}", font=("Arial", 28, "bold"), text_color="#70d6ff").grid(row=1, column=0, pady=(0, 15))

        #Confirm Button Section
        confirm_button = CTkButton(self.__summary_form, text="Confirm Booking", corner_radius=15, fg_color=("#d8315b"), width=150, height=100)
        confirm_button.grid(row=6, column=0, columnspan=2, pady=(20, 20), padx=20, sticky="ew")
    def __display_current_section(self):

        if self.__current_section == "Booking":
            self.__display_booking_section()
        elif self.__current_section == "Summary":
            self.__display_summary_section()

    def __change_section(self):
        if self.__current_section == "Booking":
            if self.__can_go_next_page():
               #self.__booking_information_manager.get_estimated_cost()
                self.__remove_current_section()
                self.__display_summary_section()

        elif self.__current_section == "Summary":
            self.__remove_current_section()
            self.__display_booking_section()

    def __remove_current_section(self):
        for widget in self.__booking_inner_frame.winfo_children():
            widget.destroy()
    
    def __can_go_next_page(self):
        __pickup = self.__booking_information_manager.get_pickup_coords()
        __dropoff = self.__booking_information_manager.get_dropoff_coords()
        __vehicle_type = self.__booking_information_manager.get_vehicle_type_int()

        if __pickup is not None and __dropoff is not None and __vehicle_type is not None:
            return True
        else:
            return False
