from customtkinter import CTkButton, CTkImage
from PIL import Image

class HamburgerButton(CTkButton):
    """Displays the button for toggleable sidebar"""

    def __init__(self, master, app,**kwargs):
        super().__init__(master, **kwargs)
        self.app = app
        self.image = CTkImage(light_image=Image.open("assets/hamburger_icon-dark.png"), dark_image=Image.open("assets/hamburger_icon-dark.png"), size=(30, 30))
        self.configure(image=self.image, command=self.toggle_sidebar, width=40, height=40, hover=False)

    def toggle_sidebar(self):
        if self.app.sidebar.winfo_ismapped():
            self.app.sidebar.grid_remove()
            self.image = CTkImage(light_image=Image.open("assets/hamburger_icon-dark.png"), dark_image=Image.open("assets/hamburger_icon-dark.png"), size=(30, 30))
            self.configure(image=self.image)
        else:
            self.app.sidebar.grid(row=1, column=2, sticky="nsew")
            self.image = CTkImage(light_image=Image.open("assets/close_icon-dark.png"), dark_image=Image.open("assets/close_icon-dark.png"), size=(30, 30))
            self.configure(image=self.image)