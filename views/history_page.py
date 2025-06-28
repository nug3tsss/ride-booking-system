from customtkinter import *

class HistoryPage(CTkFrame):
    def __init__(self, master, app):
        super().__init__(master)

        CTkLabel(self, text="Welcome to the History!", font=("Arial", 24)).pack(pady=20)