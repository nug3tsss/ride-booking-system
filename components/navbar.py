from customtkinter import *
from components.logo import Logo
from components.hamburger_button import HamburgerButton
from components.profile_button import ProfileButton


class Navbar(CTkFrame):
    def __init__(self, master, app, styles=None):
        super().__init__(master)
        self.app = app
        self.styles = styles
        self.configure(fg_color=styles.primary_color, corner_radius=0)

        # Setup navbar grid layout
        for i in range(8):
            self.grid_columnconfigure(i, weight=0)
        self.grid_columnconfigure(1, weight=1)  # left space
        self.grid_columnconfigure(5, weight=1)  # right space

        self.logo = Logo(self, self.app, text="", font=self.styles.logo_font, fg_color="transparent")
        self.logo.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

        self.render_nav()

    def render_nav(self):
        # Clear existing widgets (except logo)
        for widget in self.winfo_children():
            if widget != self.logo:
                widget.destroy()

        user = self.app.current_user

        if user is None:
            # Guest Navbar
            self.create_nav_button("Home", "Dashboard", 2)
            self.create_nav_button("About Us", "About", 3)
            self.create_nav_button("Contact Us", "Contact", 4)

            CTkButton(
                self,
                text="Sign Up",
                font=self.styles.nav_font,
                command=self.open_signup_popup,
                fg_color="#1E90FF",
                hover_color="#4682B4",
                text_color="white",
                corner_radius=20,
                width=100,
                height=32
            ).grid(row=0, column=6, padx=10, pady=10)

        else:
            # Logged-in Navbar
            self.create_nav_button("Home", "Dashboard", 2)
            self.create_nav_button("Booking", "Booking", 3)
            self.create_nav_button("History", "History", 4)

            first_name = user['username'].split()[0].capitalize()
            image_path = user.get("profile_pic", "assets/profile.png")

            self.profile_button = ProfileButton(
                self, self.app,
                text=first_name,
                image_path=image_path
            )
            self.profile_button.grid(row=0, column=6, padx=(10, 0), sticky="nsew")

        # Hamburger Menu (always shown)
        HamburgerButton(self, self.app, text="", fg_color="transparent").grid(
            row=0, column=7, padx=(0, 10), pady=10, sticky="nsew")

    def create_nav_button(self, text, page, column):
        CTkButton(self, text=text, font=self.styles.nav_font,
                  command=lambda: self.app.show_page(page),
                  fg_color="transparent", text_color="white",
                  hover_color=self.styles.hover_color, corner_radius=0
                  ).grid(row=0, column=column, padx=5, sticky="nsew")

    def open_signup_popup(self):
        if hasattr(self.app, "auth_popup") and self.app.auth_popup.winfo_exists():
            self.app.auth_popup.lift()  # bring to front
            return

        from components.auth_popup import AuthPopup
        self.app.auth_popup = AuthPopup(self.app)

