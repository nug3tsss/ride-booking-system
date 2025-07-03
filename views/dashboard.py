from customtkinter import *
from tkinter import Canvas
from PIL import Image, ImageTk

class DashboardPage(CTkFrame):
    def __init__(self, master, app):
        super().__init__(master)
        self.__app = app
        self.__booking_information_manager = self.__app.booking_information_manager

        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)

        # Load original image once
        self.original_image = Image.open("assets/dashboard_image.jpg").convert("RGB")

        # Create Canvas for image background
        self.canvas = Canvas(self, highlightthickness=0, bd=0)
        self.canvas.grid(row=0, column=0, sticky="nsew")

        # Placeholder image
        self.tk_background_image = None
        self.image_id = self.canvas.create_image(0, 0, anchor="nw", image=None)

        # Overlay Card (on top of canvas)
        self.card_container = CTkFrame(
            self,
            corner_radius=0,
            fg_color="#222222",
            border_width=2,
            border_color="#444444",
            width=400  # default width
        )
        self.card_container.place(relx=0.22, rely=0.5, anchor="center")

        # Logo
        logo_image = CTkImage(Image.open("assets/logo-dark--transparent.png"), size=(150, 150))
        self.logo_label = CTkLabel(
            self.card_container,
            image=logo_image,
            text="",
            fg_color="transparent",
            bg_color="transparent")
        self.logo_label.pack(pady=(30, 10))

        # Welcome Text
        self.welcome_label = CTkLabel(
            self.card_container,
            text="Welcome to Gethub!",
            font=("Arial", 32, "bold"),
            text_color="white",
            bg_color="transparent"
        )
        self.welcome_label.pack(padx=40, pady=(5, 5))

        # Slogan Text
        self.slogan_label = CTkLabel(
            self.card_container,
            text="We get you there. Fast. Safe. Simple.",
            font=("Arial", 16, "italic"),
            text_color="#cccccc",
            bg_color="transparent"
        )
        self.slogan_label.pack(padx=40, pady=(0, 15))

        # Book Button
        ride_icon = CTkImage(Image.open("assets/ride_icon-dark.png"), size=(24, 24))
        self.book_button = CTkButton(
            self.card_container,
            text="Book a ride now!",
            font=("Arial", 16, "bold"),
            text_color="white",
            image=ride_icon,
            corner_radius=10,
            width=200,
            height=40,
            command=self.go_to_booking_page
        )
        self.book_button.pack(pady=(20, 40))

        # Bind resize event
        self.bind("<Configure>", self.resize_image)

        # Initial forced resize (after widgets load)
        self.after(100, lambda: self.resize_image(None))

    def resize_image(self, event):
        window_width = self.winfo_width()
        window_height = self.winfo_height()

        if window_width <= 0 or window_height <= 0:
            return

        # Zoom factor: lower values for subtle zoom
        zoom_factor = 1.3

        # Aspect ratio of the window
        window_aspect = window_width / window_height

        # Original image dimensions
        orig_w, orig_h = self.original_image.size

        # Crop dimensions based on zoom factor
        crop_h = int(orig_h / zoom_factor)
        crop_w = int(crop_h * window_aspect)

        # Clamp crop_w to image width (to avoid overcropping)
        if crop_w > orig_w:
            crop_w = orig_w
            crop_h = int(crop_w / window_aspect)

        # Crop start point (adjust these to shift framing)
        x = max(0, min(int((orig_w - crop_w) * 0), orig_w - crop_w))
        y = max(0, min(int((orig_h - crop_h) * 1), orig_h - crop_h))

        # Crop and resize
        cropped = self.original_image.crop((x, y, x + crop_w, y + crop_h))
        final_image = cropped.resize((window_width, window_height), Image.Resampling.LANCZOS)

        # Update canvas
        self.tk_background_image = ImageTk.PhotoImage(final_image)
        self.canvas.config(width=window_width, height=window_height)
        self.canvas.itemconfig(self.image_id, image=self.tk_background_image)

        # Responsively reposition and resize card
        if window_width < 950:
            self.card_container.place_configure(relx=0.5, anchor="center")
            self.card_container.configure(width=int(window_width * 0.85))
        else:
            self.card_container.place_configure(relx=0.22, anchor="center")
            self.card_container.configure(width=400)

    def go_to_booking_page(self):
        self.__booking_information_manager.clear_booking_information()
        self.__app.show_page("Booking")
