from customtkinter import *
from tkinter import messagebox
from database.db_handler import get_connection
from utils.session_manager import save_session
import re
from PIL import Image

class AuthPopup(CTkToplevel):
    _instance = None

    def __new__(cls, app):
        if cls._instance is None or not cls._instance.winfo_exists():
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self, app):
        if hasattr(self, 'initialized') and self.initialized:
            return

        super().__init__(app)
        self.initialized = True
        self.app = app
        self.title("Authentication")
        self.geometry("400x460")
        self.resizable(False, False)

        self.attributes("-topmost", True)
        self.grab_set()
        self.focus_force()
        self.protocol("WM_DELETE_WINDOW", self.on_close)

        self.switch_mode("signup")

    def switch_mode(self, mode):
        for widget in self.winfo_children():
            widget.destroy()

        self.mode = mode
        self.show_password_var = BooleanVar(value=False)

        if mode == "signup":
            CTkLabel(self, text="Sign Up", font=("Arial", 20)).pack(pady=10)

            self.first_name = CTkEntry(self, placeholder_text="First Name")
            self.last_name = CTkEntry(self, placeholder_text="Last Name")
            self.username = CTkEntry(self, placeholder_text="Username")
            self.password = CTkEntry(self, placeholder_text="Password", show="*")

            self.first_name.pack(pady=5)
            self.last_name.pack(pady=5)
            self.username.pack(pady=5)
            self.password.pack(pady=5)

            CTkSwitch(self, text="Show Password", variable=self.show_password_var, command=self.toggle_password_visibility).pack(pady=3)

            CTkButton(self, text="Sign Up", command=self.register).pack(pady=10)

            frame = CTkFrame(self, fg_color="transparent")
            frame.pack()
            CTkLabel(frame, text="Already have an account?", text_color="gray").pack(side="left")
            login_label = CTkLabel(frame, text="Log In", text_color="#1E90FF", cursor="hand2")
            login_label.pack(side="left", padx=2)
            login_label.bind("<Enter>", lambda e: login_label.configure(text_color="#4682B4"))
            login_label.bind("<Leave>", lambda e: login_label.configure(text_color="#1E90FF"))
            login_label.bind("<Button-1>", lambda e: self.switch_mode("login"))

        else:
            CTkLabel(self, text="Login", font=("Arial", 20)).pack(pady=10)

            self.username = CTkEntry(self, placeholder_text="Username")
            self.password = CTkEntry(self, placeholder_text="Password", show="*")

            self.username.pack(pady=5)
            self.password.pack(pady=5)

            CTkSwitch(self, text="Show Password", variable=self.show_password_var, command=self.toggle_password_visibility).pack(pady=3)

            self.remember_me = CTkCheckBox(self, text="Remember Me")
            self.remember_me.pack(pady=5)

            CTkButton(self, text="Login", command=self.login).pack(pady=10)

            frame = CTkFrame(self, fg_color="transparent")
            frame.pack()
            CTkLabel(frame, text="Don't have an account?", text_color="gray").pack(side="left")
            signup_label = CTkLabel(frame, text="Sign Up", text_color="#1E90FF", cursor="hand2")
            signup_label.pack(side="left", padx=2)
            signup_label.bind("<Enter>", lambda e: signup_label.configure(text_color="#4682B4"))
            signup_label.bind("<Leave>", lambda e: signup_label.configure(text_color="#1E90FF"))
            signup_label.bind("<Button-1>", lambda e: self.switch_mode("signup"))

    def toggle_password_visibility(self):
        if self.show_password_var.get():
            self.password.configure(show="")
        else:
            self.password.configure(show="*")

    def highlight_error(self, entry):
        entry.configure(border_color="red")

    def clear_highlight(self, *entries):
        for entry in entries:
            entry.configure(border_color="gray")

    def register(self):
        f = self.first_name.get().strip()
        l = self.last_name.get().strip()
        u = self.username.get().strip()
        p = self.password.get().strip()

        self.clear_highlight(self.first_name, self.last_name, self.username, self.password)

        if not f or not l or not u or not p:
            messagebox.showerror("Error", "All fields are required.")
            if not f: self.highlight_error(self.first_name)
            if not l: self.highlight_error(self.last_name)
            if not u: self.highlight_error(self.username)
            if not p: self.highlight_error(self.password)
            return

        if u.lower() == "admin":
            messagebox.showerror("Error", "You cannot register as 'admin'.")
            self.highlight_error(self.username)
            return

        if len(p) < 8 or not re.search(r"[A-Z]", p) or not re.search(r"[a-z]", p) or not re.search(r"\d", p) or not re.search(r"[!@#$%^&*(),.?\":{}|<>]", p):
            messagebox.showerror("Error", "Password must be at least 8 characters and include uppercase, lowercase, digit, and special character.")
            self.highlight_error(self.password)
            return

        conn = get_connection()
        try:
            cur = conn.cursor()
            cur.execute("SELECT id FROM users WHERE username=?", (u,))
            if cur.fetchone():
                messagebox.showerror("Error", "Username already exists.")
                self.highlight_error(self.username)
                return

            cur.execute("INSERT INTO users (first_name, last_name, username, password, role) VALUES (?, ?, ?, ?, ?)",
                        (f, l, u, p, "user"))
            conn.commit()
            messagebox.showinfo("Success", "Account created. You can now login.")
            self.switch_mode("login")
        finally:
            conn.close()

    def login(self):
        u = self.username.get().strip()
        p = self.password.get().strip()

        self.clear_highlight(self.username, self.password)

        if not u or not p:
            messagebox.showerror("Error", "All fields are required.")
            if not u: self.highlight_error(self.username)
            if not p: self.highlight_error(self.password)
            return

        remember = self.remember_me.get() if hasattr(self, "remember_me") else False

        if u == "admin" and p == "admin":
            self.app.current_user = {
                "user_id": 0,
                "username": "admin",
                "first_name": "Admin",
                "last_name": "",
                "password": "admin",
                "profile_pic": "assets/profile.jpg",
                "role": "admin"
            }
            save_session(self.app.current_user, remember)
            self._post_login()
            return

        conn = get_connection()
        cur = conn.cursor()
        cur.execute("SELECT id, username, first_name, last_name, profile_pic, password FROM users WHERE username=? AND password=?", (u, p))
        user = cur.fetchone()
        conn.close()

        if user:
            self.app.current_user = {
                "user_id": user[0],
                "username": user[1],
                "first_name": user[2],
                "last_name": user[3],
                "profile_pic": user[4] if user[4] else "assets/profile.jpg",
                "password": user[5],
                "role": "user"
            }
            save_session(self.app.current_user, remember)
            self._post_login()
        else:
            messagebox.showerror("Error", "Invalid credentials.")
            self.highlight_error(self.username)
            self.highlight_error(self.password)

    def _post_login(self):
        self.app.navbar.render_nav()
        self.app.sidebar.render_sidebar()
        self.app.show_page("Dashboard")
        self.destroy()

    def on_close(self):
        self.grab_release()
        self.destroy()
