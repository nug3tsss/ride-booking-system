from customtkinter import *
from components.logo import Logo
from components.hamburger_button import HamburgerButton
from components.profile_button import ProfileButton


class Navbar(CTkFrame):
    """Displays the navigation bar at the top of the app"""

    def __init__(self, master, app, styles=None):
        super().__init__(master)
        self.app = app
        self.styles = styles
        c = self.styles.colors

        self.configure(fg_color=c["navbar"], corner_radius=0)

        # Setup navbar grid layout
        for i in range(8):
            self.grid_columnconfigure(i, weight=0)
        self.grid_columnconfigure(1, weight=1)  # left space
        self.grid_columnconfigure(5, weight=1)  # right space

        self.logo = Logo(self, self.app, text="", font=self.styles.font_h4, fg_color="transparent")
        self.logo.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

        self.render_nav()

    # Renders the navigation bar based on the current user state
    def render_nav(self):
        # Clear existing widgets (except logo)
        for widget in self.winfo_children():
            if widget != self.logo:
                widget.destroy()

        user = self.app.current_user
        c = self.styles.colors
        f = self.styles

        if user is None:
            # Guest Navbar
            self.create_nav_button("Home", "Dashboard", 2)
            self.create_nav_button("About Us", "About", 3)
            self.create_nav_button("Contact Us", "Contact", 4)

            CTkButton(
                self,
                text="Sign Up",
                font=f.font_h5,
                command=self.open_signup_popup,
                fg_color=c["signup"],
                hover_color=c["signup_hover"],
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
            image_path = user.get("profile_pic", "assets/user/profile.png")

            self.profile_button = ProfileButton(
                self, self.app,
                text=first_name,
                image_path=image_path
            )
            self.profile_button.grid(row=0, column=6, padx=(10, 0), sticky="nsew")

        # Hamburger Menu (always shown)
        HamburgerButton(self, self.app, text="", fg_color="transparent").grid(
            row=0, column=7, padx=(0, 10), pady=10, sticky="nsew")

    # Creates a navigation button with the given text, page, and column index
    def create_nav_button(self, text, page, column):
        c = self.styles.colors
        f = self.styles

        CTkButton(
            self,
            text=text,
            font=f.font_h5,
            command=lambda: self.app.show_page(page),
            fg_color="transparent",
            text_color="white",
            hover_color=c["green_accent"],
            corner_radius=0
        ).grid(row=0, column=column, padx=5, sticky="nsew")

    # Opens the signup popup if it doesn't already exist
    def open_signup_popup(self):
        if hasattr(self.app, "auth_popup") and self.app.auth_popup.winfo_exists():
            self.app.auth_popup.lift()  # bring to front
            return

        from components.auth_popup import AuthPopup
        self.app.auth_popup = AuthPopup(self.app)
