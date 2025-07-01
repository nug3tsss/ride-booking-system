from customtkinter import *
from tkinter import messagebox
import sqlite3
from database.db_handler import get_connection

class RegisterPage(CTkFrame):
    def __init__(self, master, app):
        super().__init__(master)
        self.app = app

        CTkLabel(self, text="Register", font=("Arial", 24)).pack(pady=20)

        self.username_entry = CTkEntry(self, placeholder_text="Username", width=250)
        self.username_entry.pack(pady=10)

        self.password_entry = CTkEntry(self, placeholder_text="Password", show="*", width=250)
        self.password_entry.pack(pady=10)

        self.role_option = CTkOptionMenu(self, values=["user", "admin"])
        self.role_option.pack(pady=10)
        self.role_option.set("user")

        CTkButton(self, text="Register", command=self.register_user).pack(pady=20)
        CTkButton(self, text="Go to Login", command=lambda: app.show_page("Login")).pack(pady=5)

    def register_user(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        role = self.role_option.get()

        if not username or not password:
            messagebox.showerror("Error", "All fields are required.")
            return

        conn = get_connection()
        cursor = conn.cursor()

        try:
            cursor.execute("INSERT INTO users (username, password, role) VALUES (?, ?, ?)", (username, password, role))
            conn.commit()
            messagebox.showinfo("Success", "Registration successful. You can now log in.")
            self.app.show_page("Login")
        except sqlite3.IntegrityError:
            messagebox.showerror("Error", "Username already exists.")
        finally:
            conn.close()
