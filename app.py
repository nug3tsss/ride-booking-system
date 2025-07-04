from customtkinter import *
from views.dashboard import DashboardPage
from views.booking_page import BookingPage
from views.profile_page import ProfilePage
from views.history_page import HistoryPage
from views.about import AboutPage
from views.contact import ContactPage
from views.settings import SettingsPage
from views.login_page import LoginPage
from views.register_page import RegisterPage
from components.navbar import Navbar
from components.sidebar import Sidebar
from components.logout_popup import LogoutPopup
from config.styles import Styles
from config.settings_manager import load_settings
from config.settings_manager import load_settings
from utils.session_manager import load_session, clear_session
from services.booking_information_manager import BookingInformationManager
from database.db_handler import DatabaseHandler


class App(CTk):
    def __init__(self):
        super().__init__()

        # === Styling and Theme Setup ===
        self.styles = Styles()

        settings = load_settings()
        self.styles.theme = settings.get("theme_mode", "System")
        self.styles.apply_mode(self.styles.theme)
        set_appearance_mode(self.styles.theme.lower())

        # === Window Configuration ===

        settings = load_settings()
        self.styles.theme = settings.get("theme_mode", "System")
        self.styles.apply_mode(self.styles.theme)
        set_appearance_mode(self.styles.theme.lower())

        # === Window Configuration ===
        self.title("Gethub")
        self.geometry("900x600")

        current_appearance_mode = get_appearance_mode()
        if current_appearance_mode == "dark":
            self.iconbitmap("assets/Logo-Dark-Transparent.ico")
        else:
            self.iconbitmap("assets/Logo-Light-Transparent.ico")

        self.current_user = None
        # === Database & Session ===
        self.db = DatabaseHandler()

        self.current_user = load_session()

        self.logout_popup = None
        
        self.booking_information_manager = BookingInformationManager(self.db)

        # === Grid Layout ===
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(1, weight=1)

        # === UI Components ===
        self.navbar = Navbar(self, app=self, styles=self.styles)
        self.navbar.grid(row=0, column=0, columnspan=3, sticky="nsew")

        self.sidebar = Sidebar(self, styles=self.styles)

        self.container = CTkFrame(self, fg_color=self.styles.colors["background"])
        self.container.grid(row=1, column=1, sticky="nsew")

        # === Initial Page Setup ===
        self.pages = {}
        self.navbar.render_nav()
        self.sidebar.render_sidebar()
        self.show_page("Dashboard")

        # === Window Close Event ===
        self.protocol("WM_DELETE_WINDOW", self.on_closing)

    def show_page(self, page_name):
        for widget in self.container.winfo_children():
            widget.pack_forget()

        if page_name == "Dashboard":
            page = DashboardPage(self.container, self)
        elif page_name == "Booking":
            page = BookingPage(self.container, self)
        elif page_name == "Profile":
            page = ProfilePage(self.container, self)
        elif page_name == "History":
            page = HistoryPage(self.container, self)
        elif page_name == "About":
            page = AboutPage(self.container, self)
        elif page_name == "Contact":
            page = ContactPage(self.container, self)
        elif page_name == "Settings":
            page = SettingsPage(self.container, self)
        elif page_name == "Login":
            page = LoginPage(self.container, self)
        elif page_name == "Register":
            page = RegisterPage(self.container, self)
        else:
            raise ValueError(f"Page '{page_name}' not found.")

        page.pack(fill="both", expand=True)
        self.pages[page_name] = page

    def logout(self):
        if self.logout_popup and self.logout_popup.winfo_exists():
            self.logout_popup.lift()
            return

        self.logout_popup = LogoutPopup(self, self._confirm_logout)

    def _confirm_logout(self):
        clear_session()
        self.current_user = None
        self.navbar.render_nav()
        self.sidebar.render_sidebar()
        self.show_page("Dashboard")

        if self.logout_popup:
            self.logout_popup.destroy()
            self.logout_popup = None

    def on_closing(self):
        self.destroy()