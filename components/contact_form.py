from customtkinter import *
from tkinter import messagebox
from database.db_handler import get_connection
from utils.session_manager import load_session
from PIL import Image
import datetime
import re

class ContactForm(CTkFrame):
    def __init__(self, master, app):
        super().__init__(master, fg_color="transparent")
        self.app = app

        session_user = load_session()
        self.prefilled_name = session_user["name"] if session_user and "name" in session_user else ""

        # Load send icon
        self.send_icon = CTkImage(light_image=Image.open("assets/send_icon-dark.png"), dark_image=Image.open("assets/send_icon-dark.png"), size=(20, 20))

        # Heading
        self.heading_label = CTkLabel(self, text="Send us a message", font=("Arial", 28, "bold"))
        self.heading_label.pack(pady=(20, 10))

        # Card
        self.card = CTkFrame(self, fg_color="#2a2a2a", corner_radius=10)
        self.card.pack(padx=20, pady=10, fill="x")

        # Name Entry
        self.name_entry = CTkEntry(self.card, fg_color="#3C3C3C", border_width=2, border_color="#4A4A4A")
        self.name_entry.insert(0, self.prefilled_name if self.prefilled_name else "Name")
        self.name_entry.bind("<FocusIn>", lambda e: self.clear_placeholder(self.name_entry, "Name"))
        self.name_entry.bind("<FocusOut>", lambda e: self.restore_placeholder(self.name_entry, "Name"))
        self.name_entry.bind("<KeyRelease>", self.on_field_edit)
        self.name_entry.pack(padx=20, pady=(20, 10), fill="x")

        # Email Entry
        self.email_entry = CTkEntry(self.card, fg_color="#3C3C3C", border_width=2, border_color="#4A4A4A")
        self.email_entry.insert(0, "Email")
        self.email_entry.bind("<FocusIn>", lambda e: self.clear_placeholder(self.email_entry, "Email"))
        self.email_entry.bind("<FocusOut>", lambda e: self.restore_placeholder(self.email_entry, "Email"))
        self.email_entry.bind("<KeyRelease>", self.on_field_edit)
        self.email_entry.pack(padx=20, pady=10, fill="x")

        # Message Entry
        self.message_entry = CTkTextbox(self.card, height=150, fg_color="#3C3C3C", border_width=2, border_color="#4A4A4A")
        self.message_entry.insert("1.0", "Your message...")
        self.message_entry.bind("<FocusIn>", lambda e: self.clear_textbox_placeholder(self.message_entry, "Your message..."))
        self.message_entry.bind("<FocusOut>", lambda e: self.restore_textbox_placeholder(self.message_entry, "Your message..."))
        self.message_entry.bind("<KeyRelease>", self.on_field_edit)
        self.message_entry.pack(padx=20, pady=(10, 20), fill="x")

        # Submit Button
        self.submit_btn = CTkButton(
            self.card,
            text="Submit",
            image=self.send_icon,
            compound="left",
            command=self.submit_message,
            state="disabled",
            fg_color="#444444",
            text_color="white",
            hover=False
        )
        self.submit_btn.pack(pady=(0, 20))

    def clear_placeholder(self, entry, placeholder):
        if entry.get() == placeholder:
            entry.delete(0, "end")

    def restore_placeholder(self, entry, placeholder):
        if not entry.get().strip():
            entry.insert(0, placeholder)
        self.on_field_edit()

    def clear_textbox_placeholder(self, textbox, placeholder):
        if textbox.get("1.0", "end-1c") == placeholder:
            textbox.delete("1.0", "end")

    def restore_textbox_placeholder(self, textbox, placeholder):
        if not textbox.get("1.0", "end-1c").strip():
            textbox.insert("1.0", placeholder)
        self.on_field_edit()

    def on_field_edit(self, event=None):
        name = self.name_entry.get().strip()
        email = self.email_entry.get().strip()
        message = self.message_entry.get("1.0", "end-1c").strip()
        is_valid_email = bool(re.match(r"[^@]+@[^@]+\.[^@]+", email))

        if (
            name and name != "Name" and
            email and email != "Email" and is_valid_email and
            message and message != "Your message..."
        ):
            self.submit_btn.configure(state="normal", fg_color="#1f6aa5", hover=True)
        else:
            self.submit_btn.configure(state="disabled", fg_color="#444444", hover=False)

    def submit_message(self):
        name = self.name_entry.get().strip()
        email = self.email_entry.get().strip()
        message = self.message_entry.get("1.0", "end-1c").strip()

        if not all([name, email, message]) or not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            messagebox.showerror("Error", "Please fill in all fields correctly.")
            return

        conn = get_connection()
        cursor = conn.cursor()
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        cursor.execute("INSERT INTO messages (name, email, message, timestamp) VALUES (?, ?, ?, ?)",
                       (name, email, message, timestamp))
        conn.commit()
        conn.close()

        messagebox.showinfo("Thank you", "Your message has been submitted.")
        self.reset_form()

    def reset_form(self):
        self.name_entry.delete(0, "end")
        self.email_entry.delete(0, "end")
        self.message_entry.delete("1.0", "end")

        if self.prefilled_name:
            self.name_entry.insert(0, self.prefilled_name)
        else:
            self.name_entry.insert(0, "Name")

        self.email_entry.insert(0, "Email")
        self.message_entry.insert("1.0", "Your message...")

        self.submit_btn.configure(state="disabled", fg_color="#444444", hover=False)
