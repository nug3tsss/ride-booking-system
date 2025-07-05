from customtkinter import *
from utils.session_manager import clear_session

class Sidebar(CTkFrame):
    """Displays the sidebar that contains the settings, about us, and contact us"""

    def __init__(self, master, styles=None):
        super().__init__(master)
        self.app = master
        self.styles = styles
        c = self.styles.colors
        f = self.styles

        self.configure(width=200, fg_color=c["sidebar"], corner_radius=0)
        self.render_sidebar()

    def render_sidebar(self):
        for widget in self.winfo_children():
            widget.destroy()

        c = self.styles.colors
        f = self.styles

        CTkButton(
            self,
            width=200,
            height=50,
            text="Settings",
            font=f.font_h5,
            fg_color="transparent",
            hover_color=c["sidebar_hover"],
            corner_radius=0,
            command=lambda: self.app.show_page("Settings")
        ).pack(fill="x")

        if self.app.current_user:
            CTkButton(
                self,
                width=200,
                height=50,
                text="About Us",
                font=f.font_h5,
                fg_color="transparent",
                hover_color=c["sidebar_hover"],
                corner_radius=0,
                command=lambda: self.app.show_page("About")
            ).pack(fill="x")

            CTkButton(
                self,
                width=200,
                height=50,
                text="Contact Us",
                font=f.font_h5,
                fg_color="transparent",
                hover_color=c["brown_accent"],
                corner_radius=0,
                command=lambda: self.app.show_page("Contact")
            ).pack(fill="x")

            CTkButton(
                self,
                width=50,
                height=40,
                text="Logout",
                font=f.font_h5,
                fg_color=c["brown"],
                text_color="white",
                hover_color=c["brown_hover"],
                corner_radius=30,
                command=self.app.logout
            ).pack(pady=(10, 0))

    def confirm_logout(self):
        clear_session()
        self.app.current_user = None
        self.app.navbar.render_nav()
        self.app.sidebar.render_sidebar()
        self.app.show_page("Dashboard")

        if hasattr(self.app, "logout_popup") and self.app.logout_popup:
            self.app.logout_popup.destroy()
