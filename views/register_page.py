from customtkinter import *
from tkinter import messagebox
import sqlite3
from database.db_handler import get_connection

class RegisterPage(CTkFrame):
    def __init__(self, master, app):
        super().__init__(master)
        self._app = app

        CTkLabel(self, text="Register", font=("Arial", 24)).pack(pady=20)

        self.__username_entry = CTkEntry(self, placeholder_text="Username", width=250)
        self.__username_entry.pack(pady=10)

        self.__password_entry = CTkEntry(self, placeholder_text="Password", show="*", width=250)
        self.__password_entry.pack(pady=10)

        self.__role_option = CTkOptionMenu(self, values=["user", "admin"])
        self.__role_option.pack(pady=10)
        self.__role_option.set("user")

        CTkButton(self, text="Register", command=self.__register_user).pack(pady=20)
        CTkButton(self, text="Go to Login", command=lambda: self._app.show_page("Login")).pack(pady=5)

    def __register_user(self):
        username = self.__username_entry.get()
        password = self.__password_entry.get()
        role = self.__role_option.get()

        if not username or not password:
            messagebox.showerror("Error", "All fields are required.")
            return

        conn = get_connection()
        cursor = conn.cursor()

        try:
            cursor.execute("INSERT INTO users (username, password, role) VALUES (?, ?, ?)", (username, password, role))
            conn.commit()
            messagebox.showinfo("Success", "Registration successful. You can now log in.")
            self._app.show_page("Login")
        except sqlite3.IntegrityError:
            messagebox.showerror("Error", "Username already exists.")
        finally:
            conn.close()
