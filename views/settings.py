from customtkinter import *
from utils.pycache_cleaner import PycacheCleaner

class SettingsPage(CTkFrame):
    def __init__(self, master, app):
        super().__init__(master)
        self.app = app
        c = self.app.styles.colors
        t = self.app.styles

        self.configure(fg_color=c["background"])
        CTkLabel(self, text="Settings", font=t.font_h2).pack(pady=(20, 10))

        # Theme Mode Dropdown
        CTkLabel(self, text="Theme Mode", font=t.font_p).pack(pady=(10, 5))
        self.mode_menu = CTkOptionMenu(
            self,
            values=t.theme_modes,
            command=self.on_theme_change,  # updated here
            variable=StringVar(value=t.theme.capitalize())
        )
        self.mode_menu.pack(pady=(0, 15))

        # Reset Button
        CTkButton(self, text="Restore Defaults", command=self.restore_defaults).pack(pady=5)

    def on_theme_change(self, selected):
        c = self.app.styles.colors
        t = self.app.styles
        selected = selected.capitalize()
        t.theme = selected
        t.apply_mode(selected)

        save_settings({"theme_mode": selected})
        set_appearance_mode(selected.lower())

        self.app.navbar.configure(fg_color=c["navbar"])
        self.app.sidebar.configure(fg_color=c["sidebar"])
        self.app.show_page("Settings")

        RestartPopup(self.app)  # shows the restart notification popup

    def restore_defaults(self):
        reset_settings()
        messagebox.showinfo("Reset", "Settings restored to default.")
        self.on_theme_change("System")
