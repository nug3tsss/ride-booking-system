from customtkinter import *
from tkinter import messagebox
import sqlite3
from database.db_handler import get_connection

class LoginPage(CTkFrame):
    def __init__(self, master, app):
        super().__init__(master)
        self._app = app

        CTkLabel(self, text="Login", font=("Arial", 24)).pack(pady=20)

        self.__username_entry = CTkEntry(self, placeholder_text="Username", width=250)
        self.__username_entry.pack(pady=10)

        self.__password_entry = CTkEntry(self, placeholder_text="Password", show="*", width=250)
        self.__password_entry.pack(pady=10)

        CTkButton(self, text="Login", command=self.__login_user).pack(pady=20)
        CTkButton(self, text="Go to Register", command=lambda: self._app.show_page("Register")).pack(pady=5)

    def login_user(self):
        username = self.__username_entry.get()
        password = self.__password_entry.get()

        if not username or not password:
            messagebox.showerror("Error", "Please fill in all fields.")
            return

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("SELECT id, username, role FROM users WHERE username=? AND password=?", (username, password))
        user = cursor.fetchone()

        if user:
            self._app.current_user = {
                "user_id": user[0],
                "username": user[1],
                "role": user[2]
            }
            self._app.navbar.render_nav()
            self._app.show_page("Dashboard")
        else:
            messagebox.showerror("Login Failed", "Incorrect username or password.")

        conn.close()
