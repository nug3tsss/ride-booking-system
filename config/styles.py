from customtkinter import CTkFont

class Styles:
    def __init__(self):
        # === Fonts ===
        self.font_h1 = CTkFont(family="Arial", size=32, weight="bold")
        self.font_h2 = CTkFont(family="Arial", size=24, weight="bold")
        self.font_h3 = CTkFont(family="Arial", size=18, weight="bold")
        self.font_h3p = CTkFont(family="Arial", size=18)
        self.font_h4 = CTkFont(family="Arial", size=16, weight="bold")
        self.font_h4pi = CTkFont(family="Arial", size=16, weight="normal", slant="italic")
        self.font_h5 = CTkFont(family="Arial", size=14, weight="bold")
        self.font_h5p = CTkFont(family="Arial", size=14)
        self.font_h6 = CTkFont(family="Arial", size=12, weight="bold")
        self.font_p = CTkFont(family="Arial", size=12)
        self.font_p_small = CTkFont(family="Arial", size=10)

        # === Theme Mode ===
        self.theme = "System"
        self.theme_modes = ["System", "Light", "Dark"]

        # === Light Mode Palette ===
        self.light_palette = {
            "green": {
                "base": "#287E2B",
                "hover": "#186D1C",
                "accent": "#3CA13F"
            },
            "brown": {
                "base": "#633C22",
                "hover": "#994F24",
                "accent": "#B96E52"
            },
            "monochrome": {
                "base": "#CFD8DC",
                "hover": "#B0BEC5",
                "accent": "#ECEFF1"
            },
            "background": "#E0C097",
            "card": "#795322",
            "card_light": "#A38849",
            "card_accent": "#62B956",
            "card_hover": "#578053",
            "navbar": "#39743B",
            "sidebar": "#815C32",
            "scrollbar": "#BDBDBD",
            "scrollbar_hover": "#9E9E9E",
            "button": "#487C4C",
            "button_hover": "#4DAF7E",
            "button_disable": "#595E63",
            "button_danger": "#702121",
            "button_danger_hover": "#944242",
            "entry": "#FFFFFF",
            "text": "#212121",
            "border": "#553914",
            "entry_border": "#795322",
            "table_header": "#E0E0E0",
            "table_row_even": "#916731",
            "table_row_odd": "#BE8C49",
            "divider": "#BDBDBD"
        }

        # === Dark Mode Palette ===
        self.dark_palette = {
            "green": {
                "base": "#2E7D32",
                "hover": "#1B5E20",
                "accent": "#2A352D"
            },
            "brown": {
                "base": "#6B4137",
                "hover": "#4B2E29",
                "accent": "#52403A"
            },
            "monochrome": {
                "base": "#37474F",
                "hover": "#263238",
                "accent": "#90A4AE"
            },
            "background": "#111613",
            "card": "#1F2521",
            "card_light": "#2D3A32",
            "card_accent": "#1C2720",
            "card_hover": "#2A352D",
            "navbar": "#191D1A",
            "sidebar": "#302A27",
            "scrollbar": "#444444",
            "scrollbar_hover": "#555555",
            "button": "#362222",
            "button_disable": "#555555",
            "button_hover": "#444444",
            "button_danger": "#9b1b1b",
            "button_danger_hover": "#7f1515",
            "entry": "#1E1E1E",
            "entry_border": "#333333",
            "text": "#FFFFFF",
            "border": "#444444",
            "table_header": "#1E1E1E",
            "table_row_even": "#242424",
            "table_row_odd": "#303030",
            "divider": "#444444"
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
