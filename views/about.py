from customtkinter import *

class AboutPage(CTkFrame):
    def __init__(self, master, app):
        super().__init__(master)

        CTkLabel(self, text="Welcome to the About Us Page!", font=("Arial", 24)).pack(pady=20)