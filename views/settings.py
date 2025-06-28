from customtkinter import *

class SettingsPage(CTkFrame):
    def __init__(self, master, app):
        super().__init__(master)

        CTkLabel(self, text="Settings", font=("Arial", 24)).pack(pady=20)