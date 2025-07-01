from customtkinter import *
from views.dashboard import DashboardPage
from views.booking_page import BookingPage
from views.profile_page import ProfilePage
from views.history_page import HistoryPage
from components.navbar import Navbar
from components.sidebar import Sidebar
from views.about import AboutPage
from views.contact import ContactPage
from views.settings import SettingsPage
from database.db_handler import initialize_database

class App(CTk):
    def __init__(self):
        super().__init__()
        self.title("Gethub")
        self.geometry("900x600")
        self.iconbitmap("assets/Logo-Dark-Transparent.ico")
        
        # Grid layout: navbar top, container left, sidebar right
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(1, weight=1)  # container fills center

        # Add navbar on top spanning both main + sidebar
        self.navbar = Navbar(self, app=self)
        self.navbar.grid(row=0, column=0, columnspan=3, sticky="nsew")

        # Main content container (center area)
        self.container = CTkFrame(self)
        self.container.grid(row=1, column=1, sticky="nsew")

        # Sidebar (initially hidden, placed on the right)
        self.sidebar = Sidebar(self)
        # Don't grid the sidebar initially - it will be shown when hamburger is clicked

        # Optional scrollbar inside container
        self.scrollbar = CTkScrollbar(self.container, orientation="vertical")
        self.scrollbar.pack(side="right", fill="y")

        self.pages = {}
        self.show_page("Dashboard")

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
        else:
            raise ValueError(f"Page '{page_name}' not found.")

        page.pack(fill="both", expand=True)
        self.pages[page_name] = page

    def on_closing(self):
        if self.db_conn:
            self.db_conn.close()
        self.destroy()
