from customtkinter import *

class Sidebar(CTkFrame):
    def __init__(self, master, styles=None):
        super().__init__(master)
        self.configure(width=200, fg_color=styles.sidebar_color, corner_radius=0)

        # Sidebar buttonss
        self.settings_btn = CTkButton(self, width=200, height=50, text="Settings", font=styles.sidebar_font, fg_color="transparent", hover_color=styles.hover_color, corner_radius=0,
                                  command=lambda: master.show_page("Settings"))
        self.about_btn = CTkButton(self, width=200, height=50, text="About Us", font=styles.sidebar_font, fg_color="transparent", hover_color=styles.hover_color, corner_radius=0,
                                     command=lambda: master.show_page("About"))
        self.contact_btn = CTkButton(self, width=200, height=50, text="Contact Us", font=styles.sidebar_font, fg_color="transparent", hover_color=styles.hover_color, corner_radius=0,
                                     command=lambda: master.show_page("Contact"))

        self.settings_btn.pack(fill="x")
        self.about_btn.pack(fill="x")
        self.contact_btn.pack(fill="x")
