from customtkinter import *
from PIL import Image, ImageDraw, ImageOps
from tkinter import PhotoImage
import itertools

class Navbar(CTkFrame):
    def __init__(self, master, app):
        super().__init__(master)
        self.app = app
        self.configure(fg_color="#1d1d1d", corner_radius=0)

        # Define grid columns for spacing
        self.grid_columnconfigure(0, weight=0)  # logo
        self.grid_columnconfigure(1, weight=1)  # left space
        self.grid_columnconfigure(2, weight=0)  # dashboard
        self.grid_columnconfigure(3, weight=0)  # booking
        self.grid_columnconfigure(4, weight=0)  # history
        self.grid_columnconfigure(5, weight=1)
        self.grid_columnconfigure(6, weight=0)  # profile
        self.grid_columnconfigure(7, weight=0)  # hamburger icon

        # Fonts
        logo_font = CTkFont(family="Arial", size=24, weight="bold")
        nav_font = CTkFont(family="Arial", size=14, weight="bold")
        profile_font = CTkFont(family="Arial", size=16, weight="bold")

        # Logo
        logo_image = CTkImage(Image.open("assets/logo-dark--transparent.png"), size=(50, 50))
        self.logo = CTkButton(self, text="", font=logo_font, image=logo_image,
                              command=lambda: app.show_page("Dashboard"),
                              fg_color="transparent", anchor="w", hover=False)
        self.logo.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

        # Center Navigation Buttons
        self.dashboard_button = CTkButton(self, text="Home", font=nav_font,
                                          command=lambda: app.show_page("Dashboard"),
                                          fg_color="transparent", text_color="white",
                                          hover_color="#444", corner_radius=0)
        self.booking_button = CTkButton(self, text="Booking", font=nav_font,
                                        command=lambda: app.show_page("Booking"),
                                        fg_color="transparent", text_color="white",
                                        hover_color="#444", corner_radius=0)
        self.history_button = CTkButton(self, text="History", font=nav_font,
                                        command=lambda: app.show_page("History"),
                                        fg_color="transparent", text_color="white",
                                        hover_color="#444", corner_radius=0)
        self.dashboard_button.grid(row=0, column=2, padx=5, sticky="nsew")
        self.booking_button.grid(row=0, column=3, padx=5, sticky="nsew")
        self.history_button.grid(row=0, column=4, padx=5, sticky="nsew")

        # Profile Button with circular image
        profile_raw = Image.open("assets/profile.jpg").resize((40, 40))
        mask = Image.new("L", profile_raw.size, 0)
        draw = ImageDraw.Draw(mask)
        draw.ellipse((0, 0) + profile_raw.size, fill=255)
        circular_profile = ImageOps.fit(profile_raw, profile_raw.size, centering=(0.5, 0.5))
        circular_profile.putalpha(mask)
        profile_image = CTkImage(light_image=circular_profile, size=(40, 40))

        self.profile_button = CTkButton(self, text="John Doe", font=profile_font,
                                        fg_color="transparent", image=profile_image,
                                        command=lambda: app.show_page("Profile"),
                                        text_color="white", hover=False, compound="right")
        self.profile_button.grid(row=0, column=6, padx=(10, 0), sticky="nsew")

        hamburger_image = CTkImage(Image.open("assets/hamburger_icon-default.png"), size=(30, 30))

        self.hamburger_button = CTkButton(self, text="", image=hamburger_image,
                                        fg_color="transparent", hover_color="#444",
                                        width=40, height=40,
                                        command=self.toggle_sidebar)
        self.hamburger_button.grid(row=0, column=7, padx=(10, 10), pady=10, sticky="nsew")
    
    def toggle_sidebar(self):
        if self.app.sidebar.winfo_ismapped():
            self.app.sidebar.grid_remove()
        else:
            self.app.sidebar.grid(row=1, column=2, sticky="nsew")
            self.app.sidebar.lift()
