from customtkinter import *
from tkinter import Canvas
from PIL import Image, ImageTk
from utils.session_manager import load_session

class DashboardPage(CTkFrame):
    def __init__(self, master, app):
        super().__init__(master)
        self.__app = app
        self.__booking_information_manager = self.__app.booking_information_manager
        f = self.__app.styles
        c = self.__app.styles.colors

        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)

        # Load original image once
        self.original_image = Image.open("assets/banners/dashboard_image.jpg").convert("RGB")

        # Create Canvas for image background
        self.canvas = Canvas(self, highlightthickness=0, bd=0)
        self.canvas.grid(row=0, column=0, sticky="nsew")

        # Placeholder image
        self.tk_background_image = None
        self.image_id = self.canvas.create_image(0, 0, anchor="nw", image=None)

        # Overlay Card
        self.card_container = CTkFrame(
            self,
            corner_radius=0,
            fg_color=c["home_card"],
            border_width=2,
            border_color=c["home_card_border"],
            width=400
        )
        self.card_container.place(relx=0.22, rely=0.5, anchor="center")

        # Logo
        logo_image = CTkImage(
            light_image=Image.open("assets/icons/logo-dark--transparent.png"),
            dark_image=Image.open("assets/icons/logo-dark--transparent.png"),
            size=(150, 150)
        )
        self.logo_label = CTkLabel(
            self.card_container,
            image=logo_image,
            text="",
            fg_color="transparent",
            bg_color="transparent"
        )
        self.logo_label.pack(pady=(30, 10))

        # Welcome Text
        self.welcome_label = CTkLabel(
            self.card_container,
            text="Welcome to Gethub!",
            font=f.font_h2,
            text_color="white",
            bg_color="transparent"
        )
        self.welcome_label.pack(padx=40, pady=(5, 5))

        # Slogan Text
        self.slogan_label = CTkLabel(
            self.card_container,
            text="We get you there. Fast. Safe. Simple.",
            font=CTkFont(family="Arial", size=16, weight="normal", slant="italic"),
            text_color="white",
            bg_color="transparent"
        )
        self.slogan_label.pack(padx=40, pady=(0, 15))

        # Ride Icon
        ride_icon = CTkImage(
            light_image=Image.open("assets/icons/ride_icon-dark.png"),
            dark_image=Image.open("assets/icons/ride_icon-dark.png"),
            size=(24, 24)
        )

        # Check session to decide button behavior
        session_user = load_session()
        if session_user:
            book_command = self.go_to_booking_page
        else:
            book_command = self.__app.navbar.open_signup_popup

        # Book Button
        self.book_button = CTkButton(
            self.card_container,
            text="Book a ride now!",
            font=f.font_h5,
            text_color="White",
            fg_color=c["green"],
            hover_color=c["green_hover"],
            image=ride_icon,
            corner_radius=10,
            width=200,
            height=40,
            command=book_command
        )
        self.book_button.pack(pady=(20, 40))

        # Bind resize event
        self.bind("<Configure>", self.resize_image)
        self.after(100, lambda: self.resize_image(None))

    def resize_image(self, event):
        window_width = self.winfo_width()
        window_height = self.winfo_height()

        if window_width <= 0 or window_height <= 0:
            return

        zoom_factor = 1.3
        window_aspect = window_width / window_height

        orig_w, orig_h = self.original_image.size
        crop_h = int(orig_h / zoom_factor)
        crop_w = int(crop_h * window_aspect)

        if crop_w > orig_w:
            crop_w = orig_w
            crop_h = int(crop_w / window_aspect)

        x = max(0, min(int((orig_w - crop_w) * 0), orig_w - crop_w))
        y = max(0, min(int((orig_h - crop_h) * 1), orig_h - crop_h))

        cropped = self.original_image.crop((x, y, x + crop_w, y + crop_h))
        final_image = cropped.resize((window_width, window_height), Image.Resampling.LANCZOS)

        self.tk_background_image = ImageTk.PhotoImage(final_image)
        self.canvas.config(width=window_width, height=window_height)
        self.canvas.itemconfig(self.image_id, image=self.tk_background_image)

        if window_width < 950:
            self.card_container.place_configure(relx=0.5, anchor="center")
            self.card_container.configure(width=int(window_width * 0.85))
        else:
            self.card_container.place_configure(relx=0.22, anchor="center")
            self.card_container.configure(width=400)

    def go_to_booking_page(self):
        self.__booking_information_manager.clear_booking_information()
        self.__app.show_page("Booking")
