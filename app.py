from customtkinter import *
from views.dashboard import DashboardPage
from views.booking_page import BookingPage
from views.profile_page import ProfilePage
# from components.navbar import Navbar 
# from components. import

class App(CTk):
    def __init__(self):
        super().__init__()
        self.title("Gethub")
        self.geometry("900x600")

        # set icon
        self.iconbitmap("assets/Logo-Dark-Transparent.ico")

        self.mainframe = CTkFrame(self)
        self.mainframe.pack(fill="both", expand=True)

        # set frame for displaying different views
        self.container = CTkFrame(self.mainframe)
        self.container.pack(fill="both", expand=True)

        # set up pages
        self.pages = {} 
        self.show_page("Dashboard") # default page

    # def fade_in(self, widget=None, alpha=0.0):
    #     # Use window transparency for fade-in effect
    #     if widget is None:
    #         widget = self
    #     if alpha < 1.0:
    #         alpha += 0.05
    #         widget.attributes('-alpha', alpha)
    #         widget.after(1, lambda: self.fade_in(widget, alpha))
    #     else:
    #         widget.attributes('-alpha', 1.0)

    def show_page(self, page_name):
        # clear current frame
        for widget in self.container.winfo_children():
            widget.destroy()

        # page routing
        if page_name == "Dashboard":
            page = DashboardPage(self.container, self)
        elif page_name == "Booking":
            page = BookingPage(self.container, self)
        elif page_name == "Profile":
            page = ProfilePage(self.container, self)
        else:
            raise ValueError(f"Page '{page_name}' not found.")

        page.pack(fill="both", expand=True)
        self.pages[page_name] = page
        # self.fade_in()
