from customtkinter import CTkButton, CTkImage
from PIL import Image

class Logo(CTkButton):
    def __init__(self, master, app, **kwargs):
        super().__init__(master, **kwargs)
        self.app = app

        self.logo_image = CTkImage(Image.open("assets/logo-dark--transparent.png"), size=(50, 50))
        self.configure(image=self.logo_image, command=lambda: app.show_page("Dashboard"), anchor="w", hover=False)