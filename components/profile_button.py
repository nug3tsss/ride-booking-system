from customtkinter import CTkButton, CTkImage
from PIL import Image, ImageDraw, ImageOps

class ProfileButton(CTkButton):
    def __init__(self, master, app, **kwargs):
        super().__init__(master, **kwargs)
        self.app = app
        self.configure(
            text="John Doe",
            font=("Arial", 16, "bold"),
            fg_color="transparent",
            image=self.create_profile_image(),
            command=lambda: app.show_page("Profile"),
            text_color="white",
            hover=False,
            compound="right"
        )

    def create_profile_image(self):
        profile_raw = Image.open("assets/profile.jpg").resize((40, 40))
        mask = Image.new("L", profile_raw.size, 0)
        draw = ImageDraw.Draw(mask)
        draw.ellipse((0, 0) + profile_raw.size, fill=255)
        circular_profile = ImageOps.fit(profile_raw, profile_raw.size, centering=(0.5, 0.5))
        circular_profile.putalpha(mask)
        return CTkImage(light_image=circular_profile, size=(40, 40))