from customtkinter import *
from components.logo import Logo
from components.profile_button import ProfileButton
from components.hamburger_button import HamburgerButton

class Navbar(CTkFrame):
    def __init__(self, master, app, styles=None):
        super().__init__(master)
        self.app = app
        self.configure(fg_color=styles.primary_color, corner_radius=0)

        # Define grid columns for spacing
        self.grid_columnconfigure(0, weight=0)  # logo
        self.grid_columnconfigure(1, weight=1)  # left space
        self.grid_columnconfigure(2, weight=0)  # dashboard
        self.grid_columnconfigure(3, weight=0)  # booking
        self.grid_columnconfigure(4, weight=0)  # history
        self.grid_columnconfigure(5, weight=1)  # right space
        self.grid_columnconfigure(6, weight=0)  # profile
        self.grid_columnconfigure(7, weight=0)  # hamburger icon

        # Logo
        self.logo = Logo(self, app, text="", font=styles.logo_font,
                         fg_color="transparent", anchor="w", hover=False)
        self.logo.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

        # Center Navigation Buttons
        self.dashboard_button = CTkButton(self, text="Home", font=styles.nav_font,
                                          command=lambda: app.show_page("Dashboard"),
                                          fg_color="transparent", text_color="white",
                                          hover_color=styles.hover_color, corner_radius=0)
        self.booking_button = CTkButton(self, text="Booking", font=styles.nav_font,
                                        command=lambda: app.show_page("Booking"),
                                        fg_color="transparent", text_color="white",
                                        hover_color=styles.hover_color, corner_radius=0)
        self.history_button = CTkButton(self, text="History", font=styles.nav_font,
                                        command=lambda: app.show_page("History"),
                                        fg_color="transparent", text_color="white",
                                        hover_color=styles.hover_color, corner_radius=0)
        
        self.dashboard_button.grid(row=0, column=2, padx=5, sticky="nsew")
        self.booking_button.grid(row=0, column=3, padx=5, sticky="nsew")
        self.history_button.grid(row=0, column=4, padx=5, sticky="nsew")

        # Profile Button
        self.profile_button = ProfileButton(self, app, text="Zybert Sibolboro", font=styles.profile_font,
                                            fg_color="transparent", text_color="white")
        self.profile_button.grid(row=0, column=6, padx=(10, 0), sticky="nsew")

        # Hamburger Menu Button
        self.hamburger_button = HamburgerButton(self, app, text="", fg_color="transparent")
        self.hamburger_button.grid(row=0, column=7, padx=(0, 10), pady=10, sticky="nsew")
