from customtkinter import *
from tkinter import *
from tkinter import messagebox
from database.db_handler import DatabaseHandler


class BookingSummaryForm(CTkScrollableFrame):
    """Contains booking summary from BookingForm with confirmation button"""

    def __init__(self, master, app, booking_information_manager):
        super().__init__(master)
        
        f = app.styles
        c = app.styles.colors

        self.configure(scrollbar_button_color=c["card_accent"], scrollbar_button_hover_color=c["scrollbar"])
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
        c = self.__app.styles.colors
        f = self.__app.styles

        self.__title_label = CTkLabel(self, text="Booking Summary", font=f.font_h1, text_color=c["text"])
        self.__title_label.grid(row=0, column=0, columnspan=3, pady=30, sticky="ew")

    def __create_pickup_section(self):
        c = self.__app.styles.colors
        f = self.__app.styles

        pickup_frame = CTkFrame(self, corner_radius=10, fg_color=c["card_light"])
        pickup_frame.grid(row=1, column=0, columnspan=3, sticky="ew", padx=20, pady=10)
        pickup_frame.grid_columnconfigure(1, weight=1)

        CTkLabel(pickup_frame, text="Pickup Location:", font=f.font_h4, text_color=c["text"]).grid(row=0, column=0, sticky="w", padx=15, pady=15)
        CTkLabel(pickup_frame, text=self.__pickup_address, font=f.font_p, wraplength=350).grid(row=0, column=1, sticky="w", padx=(10, 15), pady=15)

    def __create_dropoff_section(self):
        c = self.__app.styles.colors
        f = self.__app.styles

        dropoff_frame = CTkFrame(self, corner_radius=10, fg_color=c["card_light"])
        dropoff_frame.grid(row=2, column=0, columnspan=3, sticky="ew", padx=20, pady=10)
        dropoff_frame.grid_columnconfigure(1, weight=1)

        CTkLabel(dropoff_frame, text="Dropoff Location:", font=f.font_h4, text_color=c["text"]).grid(row=0, column=0, sticky="w", padx=15, pady=15)
        CTkLabel(dropoff_frame, text=self.__dropoff_address, font=f.font_p, wraplength=350).grid(row=0, column=1, sticky="w", padx=(10, 15), pady=15)

    def __create_ride_details_section(self):
        c = self.__app.styles.colors
        f = self.__app.styles

        self.__vehicle_frame = CTkFrame(self, corner_radius=10, fg_color=c["card_light"])
        self.__vehicle_frame.grid_columnconfigure(0, weight=1)
        self.__vehicle_frame.grid_columnconfigure(1, weight=1)
        self.__vehicle_frame.grid_columnconfigure(2, weight=1)
        self.__vehicle_frame.grid_columnconfigure(3, weight=1)

        CTkLabel(self.__vehicle_frame, text="Ride Information:", font=f.font_h4, text_color=c["text"]).grid(row=0, column=0, columnspan=4, sticky="w", padx=15, pady=(15, 10))

        if self.__vehicle_details:
            CTkLabel(self.__vehicle_frame, text="Type:", font=f.font_h5).grid(row=1, column=0, sticky="w", padx=(30, 10), pady=2)
            CTkLabel(self.__vehicle_frame, text=self.__vehicle_details.get('type', 'N/A'), font=f.font_p).grid(row=1, column=1, sticky="w", padx=(0, 20), pady=2)

            CTkLabel(self.__vehicle_frame, text="Model:", font=f.font_h5).grid(row=1, column=2, sticky="w", padx=(20, 10), pady=2)
            CTkLabel(self.__vehicle_frame, text=self.__vehicle_details.get('model', 'N/A'), font=f.font_p).grid(row=1, column=3, sticky="w", pady=2)

            CTkLabel(self.__vehicle_frame, text="License Plate:", font=f.font_h5).grid(row=2, column=0, sticky="w", padx=(30, 10), pady=2)
            CTkLabel(self.__vehicle_frame, text=self.__vehicle_details.get('license_plate', 'N/A'), font=f.font_p).grid(row=2, column=1, sticky="w", padx=(0, 20), pady=2)

            CTkLabel(self.__vehicle_frame, text="Driver:", font=f.font_h5).grid(row=2, column=2, sticky="w", padx=(20, 10), pady=(2, 15))
            CTkLabel(self.__vehicle_frame, text=self.__vehicle_details.get('driver_name', 'N/A'), font=f.font_p).grid(row=2, column=3, sticky="w", pady=(2, 15))

    def __create_trip_details_section(self):
        c = self.__app.styles.colors
        f = self.__app.styles

        distance_frame = CTkFrame(self, corner_radius=10, fg_color=c["card_light"])
        distance_frame.grid(row=3, column=0, sticky="nsew", padx=20, pady=15)
        distance_frame.grid_columnconfigure(0, weight=1)

        CTkLabel(distance_frame, text="Distance", font=f.font_h4, text_color=c["text"], anchor="center").grid(row=0, column=0, pady=(15, 5), padx=10, sticky="ew")
        CTkLabel(distance_frame, text=f"{self.__distance_km:.2f} km", font=f.font_h5, anchor="center").grid(row=1, column=0, pady=(5, 15), padx=10, sticky="ew")

        eta_frame = CTkFrame(self, corner_radius=10, fg_color=c["card_light"])
        eta_frame.grid(row=3, column=1, sticky="nsew", padx=20, pady=15)
        eta_frame.grid_columnconfigure(0, weight=1)

        CTkLabel(eta_frame, text="ETA", font=f.font_h4, text_color=c["text"], anchor="center").grid(row=0, column=0, pady=(15, 5), padx=10, sticky="ew")
        CTkLabel(eta_frame, text=f"{self.__estimated_time_minutes} min", font=f.font_h5, anchor="center").grid(row=1, column=0, pady=(5, 15), padx=10, sticky="ew")

    def __create_costs_section(self):
        c = self.__app.styles.colors
        f = self.__app.styles

        cost_frame = CTkFrame(self, corner_radius=15, fg_color=c["card_light"])
        cost_frame.grid(row=3, column=2, sticky="nsew", padx=20, pady=15)
        cost_frame.grid_columnconfigure(0, weight=1)

        CTkLabel(cost_frame, text="Total Estimated Cost", font=f.font_h4, text_color=c["text"], anchor="center").grid(row=0, column=0, pady=(15, 5), sticky="ew")
        CTkLabel(cost_frame, text=f"₱ {self.__estimated_cost_pesos:.2f}", font=f.font_h1, text_color=c["text"], anchor="center").grid(row=1, column=0, pady=(0, 15), sticky="ew")

    def __create_confirm_button(self):
        c = self.__app.styles.colors
        f = self.__app.styles

        self.__confirm_button = CTkButton(self, text="Confirm Booking", command=self.__confirm_booking, corner_radius=15, fg_color=c["green"], hover_color=c["green_hover"], width=150, height=40)
        self.__confirm_button.grid(row=5, column=0, columnspan=3, pady=(20, 20), padx=20)

    def __confirm_booking(self):
        if self.__is_booking_in_progress:
            return

        pickup = self.__booking_information_manager.get_pickup_address()
        destination = self.__booking_information_manager.get_dropoff_address()
        vehicle_details = self.__booking_information_manager.get_vehicle_details()
        distance_km = self.__booking_information_manager.get_distance_km()
        estimated_cost = self.__booking_information_manager.get_estimated_cost()

        vehicle_id = vehicle_details.get('id')
        user_id = self.__app.current_user.get('user_id')

        self.__current_booking_id = self.__db_handler.add_booking(
            user_id=user_id,
            pickup=pickup,
            destination=destination,
            vehicle_id=vehicle_id,
            distance_km=distance_km,
            estimated_cost=estimated_cost
        )

        if self.__current_booking_id is None:
            print("Error", "Failed to create booking in the database.")
            return

        self.__is_booking_in_progress = True
        self.__confirm_button.configure(text="Cancel Booking", command=self.__cancel_booking_process)
        self.__title_label.configure(text="Booking your ride...")

        confirm_id = self.after(5000, self.__finding_driver)
        self.__booking_after_ids.append(confirm_id)

    def __finding_driver(self):
        self.__title_label.configure(text="Finding you a driver...")
        finding_id = self.after(5000, self.__driver_found)
        self.__booking_after_ids.append(finding_id)

    def __driver_found(self):
        c = self.__app.styles.colors

        if self.__current_booking_id:
            self.__db_handler.complete_booking(self.__current_booking_id)

        self.__title_label.configure(text="Driver found!")
        self.__vehicle_frame.grid(row=4, column=0, columnspan=3, sticky="ew", padx=20, pady=15)

        self.__confirm_button.grid_forget()

        self.__cancel_button = CTkButton(self, text="Cancel Booking", command=self.__cancel_booking, corner_radius=15, fg_color=c["brown"], hover_color=c["brown_hover"], width=150, height=40)
        self.__cancel_button.grid(row=6, column=0, columnspan=1, pady=(20, 20), padx=20, sticky="ew")

        self.__go_to_bookings_button = CTkButton(self, text="Go to your bookings", command=self.__go_to_your_bookings, corner_radius=15, fg_color=c["green"], hover_color=c["green_hover"], width=150, height=40)
        self.__go_to_bookings_button.grid(row=6, column=1, columnspan=2, pady=(20, 20), padx=20, sticky="ew")

        self.__is_booking_in_progress = False
        self.__booking_after_ids.clear()
        self.__booking_information_manager.clear_booking_information()

    def __cancel_booking_process(self):
        for after_id in self.__booking_after_ids:
            self.after_cancel(after_id)

        self.__booking_after_ids.clear()
        self.__is_booking_in_progress = False

        if self.__current_booking_id:
            self.__db_handler.cancel_booking(self.__current_booking_id)
            self.__current_booking_id = None

        self.__title_label.configure(text="Booking summary")
        self.__confirm_button.configure(text="Confirm Booking", command=self.__confirm_booking)
        messagebox.showinfo("Booking Cancelled", "Booking has been cancelled.")

    def __cancel_booking(self):
        if self.__current_booking_id:
            self.__db_handler.cancel_booking(self.__current_booking_id)
            messagebox.showinfo("Booking Cancelled", f"Booking ID {self.__current_booking_id} has been cancelled.")
            self.__current_booking_id = None

            self.__booking_information_manager.clear_booking_information()
            self.__app.show_page("Booking")

    def __go_to_your_bookings(self):
        self.__app.show_page("History")
