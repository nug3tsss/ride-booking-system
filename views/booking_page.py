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

        self.__app = app
        self.__booking_information_manager = self.__app.booking_information_manager

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
        self.__booking_label.configure(text="Booking summary")
        self.__current_section = "Summary"
        self.__booking_information_manager.set_current_booking_section(self.__current_section)
        self.__button.configure(text="Go Back")

        self.__summary_form = CTkFrame(self.__booking_inner_frame)
        self.__summary_form.pack(side=LEFT, fill="both", expand=True, padx=15, pady=15)
        self.__summary_map = BookingSummaryMap(self.__booking_inner_frame, self.__booking_information_manager)

    def __display_current_section(self):
        if self.__current_section == "Booking":
            self.__display_booking_section()
        elif self.__current_section == "Summary":
            self.__display_summary_section()

    def __change_section(self):
        if self.__current_section == "Booking":
            if self.__can_go_next_page():
                self.__remove_current_section()
                self.__display_summary_section()
        elif self.__current_section == "Summary":
            self.__remove_current_section()
            self.__display_booking_section()

    def __remove_current_section(self):
        if self.__booking_inner_frame.winfo_children():
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
