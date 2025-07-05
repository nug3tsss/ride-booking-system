from customtkinter import *
from components.restart_popup import RestartPopup
from config.settings_manager import save_settings, reset_settings
from tkinter import messagebox
from utils.pycache_cleaner import PycacheCleaner

class SettingsPage(CTkFrame):
    """Settings Page of the application, allowing users to change theme and manage settings."""

    def __init__(self, master, app):
        super().__init__(master)
        self.app = app
        c = self.app.styles.colors
        t = self.app.styles

        self.configure(fg_color=c["background"])
        CTkLabel(self, text="Settings", font=t.font_h2).pack(pady=(20, 10))

        # Theme Mode Dropdown
        CTkLabel(self, text="Theme Mode", font=t.font_h5).pack(pady=(10, 5))
        self.mode_menu = CTkOptionMenu(
            self,
            fg_color=c["card_light"],
            button_color=c["card"],
            button_hover_color=c["card_light_hover"],
            values=t.theme_modes,
            command=self.on_theme_change,
            variable=StringVar(value=t.theme.capitalize())
        )
        self.mode_menu.pack(pady=(0, 15))

        # Restore Defaults
        CTkButton(self, text="Restore Defaults", fg_color=c["green"], hover_color=c["green_hover"], command=self.restore_defaults).pack(pady=5)

        # Clear Cache
        CTkButton(self, text="Clear Cache", fg_color=c["green"], hover_color=c["green_hover"], command=self.clear_cache).pack(pady=5)

    # Handles theme change from the dropdown menu
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

        RestartPopup(self.app)

    # Restores default settings and updates the theme
    def restore_defaults(self):
        reset_settings()
        messagebox.showinfo("Reset", "Settings restored to default.")
        self.on_theme_change("System")

    # Clears the Python cache by deleting .pyc files and __pycache__ folders
    def clear_cache(self):
        pyc_count, folder_count = PycacheCleaner.clear_pycache(".")
        messagebox.showinfo(
            "Cache Cleared",
            f"Deleted {pyc_count} .pyc file(s) and {folder_count} __pycache__ folder(s)."
        )

