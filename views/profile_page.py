from customtkinter import *

class ProfilePage(CTkFrame):
    def __init__(self, master, app):
        super().__init__(master)
        self.app = app
        self.pack(fill="both", expand=True)

        # Add content to the profile page
        self.label = CTkLabel(self, text="Welcome to the Profile Page!")
        self.label.pack(pady=20)

        # self.button = CTkButton(self, text="Go to Dashboard", command=lambda: app.show_page("dashboard"))
        # self.button.pack(pady=20)