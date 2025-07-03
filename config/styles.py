from customtkinter import CTkFont

class Styles:
    def __init__(self):
        # === Fonts ===
        self.font_h1 = CTkFont(family="Arial", size=24, weight="bold")
        self.font_h2 = CTkFont(family="Arial", size=20, weight="bold")
        self.font_h3 = CTkFont(family="Arial", size=18, weight="bold")
        self.font_h4 = CTkFont(family="Arial", size=16, weight="bold")
        self.font_h5 = CTkFont(family="Arial", size=14, weight="bold")
        self.font_h6 = CTkFont(family="Arial", size=12, weight="bold")
        self.font_p = CTkFont(family="Arial", size=12)
        self.font_p_small = CTkFont(family="Arial", size=10)

        # === Theme Mode ===
        self.theme = "System"
        self.theme_modes = ["System", "Light", "Dark"]

        # === Light Mode Palette ===
        self.light_palette = {
            "green": {
                "base": "#4CAF50",
                "hover": "#388E3C",
                "accent": "#C8E6C9"
            },
            "brown": {
                "base": "#A1887F",
                "hover": "#8D6E63",
                "accent": "#D7CCC8"
            },
            "monochrome": {
                "base": "#CFD8DC",
                "hover": "#B0BEC5",
                "accent": "#ECEFF1"
            },
            "background": "#F5F5F5",
            "card": "#FFFFFF",
            "navbar": "#FFFFFF",
            "sidebar": "#E0E0E0",
            "button": "#DDDDDD",
            "button_hover": "#CCCCCC",
            "entry": "#FFFFFF",
            "text": "#212121",
            "border": "#CCCCCC"
        }

        # === Dark Mode Palette ===
        self.dark_palette = {
            "green": {
                "base": "#2E7D32",
                "hover": "#1B5E20",
                "accent": "#66BB6A"
            },
            "brown": {
                "base": "#4E342E",
                "hover": "#3E2723",
                "accent": "#A1887F"
            },
            "monochrome": {
                "base": "#37474F",
                "hover": "#263238",
                "accent": "#90A4AE"
            },
            "background": "#121212",
            "card": "#1E1E1E",
            "navbar": "#1E1E1E",
            "sidebar": "#2A2A2A",
            "button": "#362222",
            "button_hover": "#444444",
            "entry": "#1E1E1E",
            "text": "#FFFFFF",
            "border": "#444444"
        }

        # Active color map
        self.colors = {}
        self.apply_mode("light")  # Default mode

    def apply_mode(self, mode):
        """Apply theme colors based on mode and add flat aliases."""
        self.theme = mode.lower()
        palette = self.light_palette if self.theme == "light" else self.dark_palette
        self.colors = palette.copy()

        # Flat shorthand color aliases
        self.colors.update({
            # Green
            "green": palette["green"]["base"],
            "green_hover": palette["green"]["hover"],
            "green_accent": palette["green"]["accent"],

            # Brown
            "brown": palette["brown"]["base"],
            "brown_hover": palette["brown"]["hover"],
            "brown_accent": palette["brown"]["accent"],

            # Monochrome
            "mono": palette["monochrome"]["base"],
            "mono_hover": palette["monochrome"]["hover"],
            "mono_accent": palette["monochrome"]["accent"],

            # Generic accent color (brown)
            "accent": palette["brown"]["base"],
            "accent_hover": palette["brown"]["hover"],
            "accent_accent": palette["brown"]["accent"],

            # Shorthand UI elements
            "bg": palette["background"],
            "card": palette["card"],
            "navbar": palette["navbar"],
            "sidebar": palette["sidebar"],
            "button": palette["button"],
            "button_hover": palette["button_hover"],
            "entry": palette["entry"],
            "text": palette["text"],
            "border": palette["border"],
        })

    def reset_to_defaults(self):
        """Reset to default system theme (Light as fallback)."""
        self.theme = "System"
        self.apply_mode("light")
