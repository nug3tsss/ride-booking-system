from customtkinter import *
from PIL import Image, ImageDraw, ImageOps
from tkinter import PhotoImage
import itertools

class Navbar(CTkFrame):
    def __init__(self, master, app):
        super().__init__(master)
        self.app = app
        self.configure(fg_color="#1d1d1d", corner_radius=0)

        # Define grid columns for spacing
        self.grid_columnconfigure(0, weight=0)  # logo
        self.grid_columnconfigure(1, weight=1)  # left space
        self.grid_columnconfigure(2, weight=0)  # dashboard
        self.grid_columnconfigure(3, weight=0)  # booking
        self.grid_columnconfigure(4, weight=1)  # right space
        self.grid_columnconfigure(5, weight=0)  # profile
        self.grid_columnconfigure(6, weight=0)  # hamburger icon

        # Fonts
        logo_font = CTkFont(family="Arial", size=24, weight="bold")
        nav_font = CTkFont(family="Arial", size=14, weight="bold")
        profile_font = CTkFont(family="Arial", size=16, weight="bold")

        # Logo
        logo_image = CTkImage(Image.open("assets/logo-dark--transparent.png"), size=(50, 50))
        self.logo = CTkButton(self, text="", font=logo_font, image=logo_image,
                              command=lambda: app.show_page("Dashboard"),
                              fg_color="transparent", anchor="w", hover=False)
        self.logo.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

        # Center Navigation Buttons
        self.dashboard_button = CTkButton(self, text="Home", font=nav_font,
                                          command=lambda: app.show_page("Dashboard"),
                                          fg_color="transparent", text_color="white",
                                          hover_color="#444", corner_radius=0)
        self.booking_button = CTkButton(self, text="Booking", font=nav_font,
                                        command=lambda: app.show_page("Booking"),
                                        fg_color="transparent", text_color="white",
                                        hover_color="#444", corner_radius=0)
        self.dashboard_button.grid(row=0, column=2, padx=5, sticky="nsew")
        self.booking_button.grid(row=0, column=3, padx=5, sticky="nsew")

        # Profile Button with circular image
        profile_raw = Image.open("assets/profile.jpg").resize((40, 40))
        mask = Image.new("L", profile_raw.size, 0)
        draw = ImageDraw.Draw(mask)
        draw.ellipse((0, 0) + profile_raw.size, fill=255)
        circular_profile = ImageOps.fit(profile_raw, profile_raw.size, centering=(0.5, 0.5))
        circular_profile.putalpha(mask)
        profile_image = CTkImage(light_image=circular_profile, size=(40, 40))

        self.profile_button = CTkButton(self, text="John Doe", font=profile_font,
                                        fg_color="transparent", image=profile_image,
                                        command=lambda: app.show_page("Profile"),
                                        text_color="white", hover=False, compound="right")
        self.profile_button.grid(row=0, column=5, padx=(10, 0), sticky="nsew")

        # Load GIF frames for hamburger icon
        self.hamburger_frames = [
            PhotoImage(file="assets/hamburger_icon-animated.gif", format=f"gif -index {i}")
            for i in range(self.get_gif_frame_count("assets/hamburger_icon-animated.gif"))
        ]
        self.hamburger_iterator = itertools.cycle(self.hamburger_frames)
        self.hamburger_icon_label = CTkLabel(self, text="", image=self.hamburger_frames[0])
        self.hamburger_icon_label.grid(row=0, column=6, padx=(10, 10), pady=10, sticky="nsew")
        self.hamburger_icon_label.bind("<Button-1>", self.animate_hamburger)

    def get_gif_frame_count(self, path):
        from PIL import Image as PILImage
        with PILImage.open(path) as img:
            return getattr(img, "n_frames", 1)

    def animate_hamburger(self, event=None):
        def next_frame():
            try:
                frame = next(self.hamburger_iterator)
                self.hamburger_icon_label.configure(image=frame)
                self.after(50, next_frame)  # Adjust speed as needed
            except StopIteration:
                pass

        next_frame()
