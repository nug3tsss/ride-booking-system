from customtkinter import CTkFont

class Styles:
    def __init__(self):
        # === Define fonts ===

        # Default font
        self.default_font = CTkFont(family="Arial", size=12)

        # Navbar and sidebar fonts
        self.logo_font = CTkFont(family="Arial", size=24, weight="bold")
        self.nav_font = CTkFont(family="Arial", size=14, weight="bold")
        self.profile_font = CTkFont(family="Arial", size=16, weight="bold")
        self.sidebar_font = CTkFont(family="Arial", size=14, weight="normal")

        # === Define colors ===

        self.primary_color = "#1d1d1d"
        self.secondary_color = "#444444"
        self.sidebar_color = "#2a2a2a"
        self.hover_color = "#444444"

