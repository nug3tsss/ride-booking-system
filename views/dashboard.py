from customtkinter import *
from components.navbar import Navbar

class DashboardPage(CTkFrame):
    def __init__(self, master, app):
        super().__init__(master)
        self.__app = app
        self.__booking_information_manager = self.__app.booking_information_manager

        # Adjust the size of the frames (currently 60% left, 40% right)
        self.columnconfigure(0, weight=6)
        self.columnconfigure(1, weight=4)
        self.rowconfigure(0, weight=1)

        self.left_frame = CTkFrame(self)
        self.left_frame.grid(row=0, column=0, sticky="nsew", padx=15, pady=15)

        self.right_frame = CTkFrame(self)
        self.right_frame.grid(row=0, column=1, sticky="nsew", padx=15, pady=15)

        # Add left frame contents
        self.welcome_label = CTkLabel(self.left_frame, text="Welcome to Gethub!", font=("Arial", 32))
        self.welcome_label.pack(anchor="w", padx=15, pady=15)
        
        self.picture_label = CTkLabel(self.left_frame, text="Picture Placeholder", font=("Arial", 16))
        self.picture_label.pack(padx=15, pady=15)

        self.book_your_ride_button = CTkButton(self.left_frame, text="Book your ride", command=self.go_to_booking_page)
        self.book_your_ride_button.pack(anchor="w", side=BOTTOM, padx=15, pady=15)

        # Add right frame contents
        self.quotation_label = CTkLabel(self.right_frame, text="\"The best way to predict the future is to create it.\"", font=("Arial", 16))
        self.quotation_label.pack(anchor="w", padx=15, pady=15)
    
    def go_to_booking_page(self):
        self.__booking_information_manager.clear_booking_information()
        self.__app.show_page("Booking")
