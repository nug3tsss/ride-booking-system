from customtkinter import *

class Sidebar(CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        self.configure(width=200, fg_color="#2a2a2a", corner_radius=0)

        # Example buttons inside the sidebar
        self.home_btn = CTkButton(self, text="Settings", fg_color="transparent", hover_color="#444",
                                  command=lambda: master.show_page("Settings"))
        self.booking_btn = CTkButton(self, text="About Us", fg_color="transparent", hover_color="#444",
                                     command=lambda: master.show_page("About"))
        self.history_btn = CTkButton(self, text="Contact Us", fg_color="transparent", hover_color="#444",
                                     command=lambda: master.show_page("Contact"))

        # Pack or grid the widgets
        self.home_btn.pack(padx=10, pady=10, fill="x")
        self.booking_btn.pack(padx=10, pady=10, fill="x")
        self.history_btn.pack(padx=10, pady=10, fill="x")
