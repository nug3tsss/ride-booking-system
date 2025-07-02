from customtkinter import *
from PIL import Image, ImageOps

class DashboardPage(CTkFrame):
    def __init__(self, master, app):
        super().__init__(master)
        self.__app = app
        self.__booking_information_manager = self.__app.booking_information_manager

        # Configure the main grid
        self.rowconfigure(1, weight=1)
        self.columnconfigure(0, weight=1)

        # Header label
        self.welcome_label = CTkLabel(
            self,
            text="Welcome to Gethub!",
            font=("Arial", 32, "bold"),
            text_color="white"
        )
        self.welcome_label.grid(row=0, column=0, sticky="n", padx=30, pady=(30, 10))

        # Load the original image once
        self.original_image = Image.open("assets/dashboard_image.jpg")

        # Placeholder image
        self.dashboard_image = CTkImage(light_image=self.original_image, dark_image=self.original_image, size=(100, 100))
        self.picture_label = CTkLabel(self, image=self.dashboard_image, text="")
        self.picture_label.grid(row=1, column=0, sticky="nsew", padx=0, pady=10)  # No horizontal padding

        # Book ride button
        ride_icon = CTkImage(Image.open("assets/ride_icon-dark.png"), size=(24, 24))
        self.book_your_ride_button = CTkButton(
            self,
            text="Book a ride now!",
            font=("Arial", 16, "bold"),
            width=220,
            height=50,
            corner_radius=10,
            image=ride_icon,
            fg_color="#1abc9c",
            hover_color="#16a085",
            text_color="white",
            command=self.go_to_booking_page
        )
        self.book_your_ride_button.grid(row=2, column=0, pady=(20, 30))

        # Bind resize event
        self.bind("<Configure>", self.resize_image)

    def resize_image(self, event):
        available_width = self.winfo_width()  # Full width, no padding subtraction
        desired_height = 720

        if available_width > 0:
            # Resize and crop image to fill the width and crop vertically
            fitted_image = ImageOps.fit(
                self.original_image,
                (available_width, desired_height),
                method=Image.Resampling.LANCZOS,
                centering=(0.5, 0.3)  # crop bias slightly upward if needed
            )

            self.dashboard_image = CTkImage(
                light_image=fitted_image,
                dark_image=fitted_image,
                size=(available_width, desired_height)
            )
            self.picture_label.configure(image=self.dashboard_image)

    def go_to_booking_page(self):
        self.__booking_information_manager.clear_booking_information()
        self.__app.show_page("Booking")
