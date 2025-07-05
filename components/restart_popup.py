from customtkinter import *
import sys
import os

class RestartPopup(CTkToplevel):
    def __init__(self, master):
        super().__init__(master)
        self.master = master
        self.styles = master.styles
        self.title("Restart Required")
        self.geometry("320x200")
        self.resizable(False, False)
        self.grab_set()
        self.attributes("-topmost", True)

        c = self.styles.colors
        f = self.styles

        # === Message ===
        CTkLabel(
            self,
            text="Restart the app to apply\nchanges.",
            font=f.font_h5,
            text_color=c["text"],
            justify="center"
        ).pack(pady=(40, 20), padx=20)

        # === Buttons Frame ===
        button_frame = CTkFrame(self, fg_color="transparent")
        button_frame.pack(pady=10)

        # === Restart Now ===
        restart_btn = CTkButton(
            button_frame,
            text="Restart Now",
            font=f.font_p,
            fg_color=c["green"],
            hover_color=c["green"],
            text_color="white",
            width=120,
            command=self.restart_app
        )
        restart_btn.pack(side="left", padx=10, pady=10)

        # === Later ===
        later_btn = CTkButton(
            button_frame,
            text="Later",
            font=f.font_p,
            fg_color=c["green"],
            hover_color=c["green"],
            text_color="white",
            width=120,
            command=self.destroy
        )
        later_btn.pack(side="left", padx=10, pady=10)

    def restart_app(self):
        python = sys.executable
        os.execl(python, python, *sys.argv)
