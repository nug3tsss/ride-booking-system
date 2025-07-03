from customtkinter import *
from components.logout_popup import LogoutPopup
from utils.session_manager import clear_session

class Sidebar(CTkFrame):
    """Displays the sidebar that contains the settings, about us, and contact us"""

    def __init__(self, master, styles=None):
        super().__init__(master)
        self.app = master
        self.styles = styles
        self.configure(width=200, fg_color=styles.sidebar_color, corner_radius=0)
        self.render_sidebar()

    def render_sidebar(self):
        for widget in self.winfo_children():
            widget.destroy()

        CTkButton(self, width=200, height=50, text="Settings", font=self.app.styles.sidebar_font,
                fg_color="transparent", hover_color=self.app.styles.hover_color,
                corner_radius=0, command=lambda: self.app.show_page("Settings")).pack(fill="x")

        if self.app.current_user:
            CTkButton(self, width=200, height=50, text="About Us", font=self.app.styles.sidebar_font,
                    fg_color="transparent", hover_color=self.app.styles.hover_color,
                    corner_radius=0, command=lambda: self.app.show_page("About")).pack(fill="x")
            CTkButton(self, width=200, height=50, text="Contact Us", font=self.app.styles.sidebar_font,
                    fg_color="transparent", hover_color=self.app.styles.hover_color,
                    corner_radius=0, command=lambda: self.app.show_page("Contact")).pack(fill="x")
            CTkButton(self, width=50, height=40, text="Logout", font=self.app.styles.sidebar_font,
                    fg_color="#9b1b1b", text_color="white", hover_color="#7f1515",
                    corner_radius=30, command=self.app.logout).pack(pady=(10, 0))

    def confirm_logout(self):
        clear_session()
        self.current_user = None
        self.navbar.render_nav()
        self.sidebar.render_sidebar()
        self.show_page("Dashboard")
        if self.logout_popup:
            self.logout_popup.destroy()
