
from customtkinter import *
from components.booking_history_list import BookingHistoryList

class HistoryPage(CTkFrame):
    def __init__(self, master, app):
        super().__init__(master)
        self.app = app
        self.pack(fill="both", expand=True)

        self.__booking_history_list = BookingHistoryList(self, app)
