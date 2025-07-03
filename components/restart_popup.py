from customtkinter import *
import sys
import os

class RestartPopup(CTkToplevel):
    def __init__(self, master):
        super().__init__(master)
        self.master = master
        self.styles = master.styles
        self.title("Restart Required")
        self.geometry("300x300")
        # self.resizable(False, False)
        self.grab_set()
        self.attributes("-topmost", True)
        self.configure(fg_color=self.styles.colors["card"])

        # === Message ===
        CTkLabel(
            self,
            text="Restart the app to apply\ntheme changes.",
            font=self.styles.font_h5,
            text_color=self.styles.colors["text"],
            justify="center"
        ).pack(pady=(30, 10), padx=20)
       
        # === Buttons Frame ===
        button_frame = CTkFrame(self, fg_color="transparent")
        button_frame.pack(pady=20)

        # === Restart Now ===
        restart_btn = CTkButton(
            button_frame,
            text="Restart Now",
            font=self.styles.font_p,
            fg_color=self.styles.colors["green"],
            hover_color=self.styles.colors["green"],
            text_color="white",
            width=120,
            command=self.restart_app
        )
        restart_btn.pack(side="left", padx=10)

        # === Later ===
        later_btn = CTkButton(
            button_frame,
            text="Later",
            font=self.styles.font_p,
            fg_color=self.styles.colors["monochrome"],
            hover_color=self.styles.colors["monochrome"],
            text_color=self.styles.colors["text"],
            width=120,
            command=self.destroy
        )
        later_btn.pack(side="left", padx=10)

    def restart_app(self):
        python = sys.executable
        os.execl(python, python, *sys.argv)
