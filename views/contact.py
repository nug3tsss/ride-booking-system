from customtkinter import *

class ContactPage(CTkFrame):
    def __init__(self, master, app):
        super().__init__(master)

        CTkLabel(self, text="Hi, How are you?", font=("Arial", 24)).pack(pady=20)