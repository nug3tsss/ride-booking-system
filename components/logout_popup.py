from customtkinter import *

class LogoutPopup(CTkToplevel):
    """Popup for user logout"""

    def __init__(self, app, confirm_callback):
        super().__init__(app)
        self.app = app
        self.confirm_callback = confirm_callback
        self.title("Confirm Logout")
        self.geometry("300x150")
        self.resizable(False, False)

        self.attributes("-topmost", True)  # Always on top
        self.grab_set()  # Make modal (disable interaction with parent)
        self.focus_force()

        CTkLabel(self, text="Are you sure you want to logout?", font=("Arial", 16)).pack(pady=20)

        # Create a horizontal frame for buttons
        button_frame = CTkFrame(self, fg_color="transparent")
        button_frame.pack(pady=(5, 0))

        CTkButton(button_frame, text="Yes", command=self.confirm, fg_color="#9b1b1b").pack(side="left", padx=10)
        CTkButton(button_frame, text="Cancel", command=self.close).pack(side="left", padx=10)

    # Confirm logout action
    def confirm(self):
        self.grab_release()
        self.destroy()
        self.confirm_callback()

    # Close the popup without action
    def close(self):
        self.grab_release()
        self.destroy()
