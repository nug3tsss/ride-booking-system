from customtkinter import CTkButton, CTkImage
from PIL import Image, ImageDraw, ImageOps

class ProfileButton(CTkButton):
    """Displays the circular profile image of user"""

    def __init__(self, master, app, text="John Doe", image_path="assets/user/profile.jpg", **kwargs):
        self.app = app
        f = self.app.styles
        c = self.app.styles.colors

        self.profile_image = self.create_profile_image(image_path)

        super().__init__(
            master,
            text=text,
            font=f.font_h5,
            fg_color="transparent",
            image=self.profile_image,
            command=lambda: app.show_page("Profile"),
            text_color="white",
            hover=False,
            compound="right",
            **kwargs
        )

    def create_profile_image(self, path):
        try:
            profile_raw = Image.open(path).resize((40, 40))
        except Exception:
            profile_raw = Image.open("assets/user/profile.jpg").resize((40, 40))  # fallback if missing

        mask = Image.new("L", profile_raw.size, 0)
        draw = ImageDraw.Draw(mask)
        draw.ellipse((0, 0) + profile_raw.size, fill=255)
        circular_profile = ImageOps.fit(profile_raw, profile_raw.size, centering=(0.5, 0.5))
        circular_profile.putalpha(mask)
        return CTkImage(circular_profile, size=(40, 40))
