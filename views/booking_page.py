from customtkinter import *
from tkintermapview import *
from tkinter import messagebox
from components.booking_form import BookingForm
from components.booking_map import BookingMap
from components.booking_summary_map import BookingSummaryMap
from components.booking_summary_form import BookingSummaryForm

class BookingPage(CTkFrame):
    """Contains booking form, booking map, and booking summary and confirmation button"""

    def __init__(self, master, app):
        super().__init__(master)
        self.pack(fill="both", expand=True)

        self.__app = app
        self.__booking_information_manager = app.booking_information_manager

        f = app.styles
        c = app.styles.colors

        self.configure(fg_color=c["bg"])

        self.__current_section = self.__booking_information_manager.get_current_booking_section()

        self.__create_core_widgets(f, c)
        self.__display_last_section_selected()

    # Creates the core widgets for the booking page
    # Includes a label, inner frame for content, and a button to change sections
    def __create_core_widgets(self, f, c):
        self.__booking_label = CTkLabel(
            self,
            text="",
            font=f.font_h2,
            text_color=c["text"],
            fg_color="transparent"
        )
        self.__booking_label.pack(anchor="w", padx=15, pady=15, side=TOP)

        self.__booking_inner_frame = CTkFrame(
            self,
            fg_color=c["card"],
            corner_radius=10
        )
        self.__booking_inner_frame.pack(fill="both", expand=True, padx=15, pady=(0, 15))

        self.__button = CTkButton(
            self,
            command=self.__change_section,
            font=f.font_h5,
            text_color=c["text"],
            fg_color=c["green"],
            hover_color=c["green_hover"],
            corner_radius=8,
            width=150,
            height=40
        )
        self.__button.pack(side=LEFT, padx=15, pady=(0, 15))

    # Displays the booking section with the booking form and map
    def __display_booking_section(self):
        self.__booking_label.configure(text="Book a Ride!")

        self.__current_section = "Booking"
        self.__booking_information_manager.set_current_booking_section(self.__current_section)
        self.__button.configure(text="Next", text_color="white")

        booking_map = BookingMap(self.__booking_inner_frame, self.__booking_information_manager)
        booking_form = BookingForm(
            self.__app,
            self.__booking_inner_frame,
            booking_map.get_map_manager_instance(),
            self.__booking_information_manager
        )

    # Displays the summary section with booking summary form and map
    def __display_summary_section(self):
        self.__booking_label.configure(text="")

        self.__current_section = "Summary"
        self.__booking_information_manager.set_current_booking_section(self.__current_section)
        self.__button.configure(text="Go Back", text_color="white")

        summary_form = BookingSummaryForm(self.__booking_inner_frame, self.__app, self.__booking_information_manager)
        summary_map = BookingSummaryMap(self.__booking_inner_frame, self.__booking_information_manager)

    # Displays the last selected section based on the current section
    def __display_last_section_selected(self):
        if self.__current_section == "Booking":
            self.__display_booking_section()
        elif self.__current_section == "Summary":
            self.__display_summary_section()

    # Changes the section based on the current section
    def __change_section(self):
        if self.__current_section == "Booking":
            if self.__can_go_next_page():
                self.__remove_current_section()
                self.__display_summary_section()

        elif self.__current_section == "Summary":
            self.__remove_current_section()
            self.__display_booking_section()

    # Removes all widgets in the current section to prepare for the next section
    def __remove_current_section(self):
        for widget in self.__booking_inner_frame.winfo_children():
            widget.destroy()

    # Checks if all required fields are filled before proceeding to the next page
    def __can_go_next_page(self):
        pickup = self.__booking_information_manager.get_pickup_coords()
        dropoff = self.__booking_information_manager.get_dropoff_coords()
        vehicle_type = self.__booking_information_manager.get_vehicle_type_int()

        if pickup is not None and dropoff is not None and vehicle_type is not None:
            return True
        else:
            messagebox.showwarning("WARNING!", "Please input all required fields before proceeding!")
            return False