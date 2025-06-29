from customtkinter import *
from components.navbar import Navbar

class DashboardPage(CTkFrame):
    def __init__(self, master, app):
        super().__init__(master)

        CTkLabel(self, text="Welcome to the Dashboard!", font=("Arial", 24)).pack(pady=20)