from customtkinter import *
from utils.pycache_cleaner import PycacheCleaner

class SettingsPage(CTkFrame):
    def __init__(self, master, app):
        super().__init__(master)
        self.app = app

        CTkLabel(self, text="Settings", font=("Arial", 24)).pack(pady=20)

        CTkButton(self, text="Clear Cache").pack(pady=10)