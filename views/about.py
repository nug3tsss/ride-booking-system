from customtkinter import *
from PIL import Image

class AboutPage(CTkFrame):
    def __init__(self, master, app):
        super().__init__(master)

        self.__image = Image.open("assets/user_8_profile.png")

        self.__ctkimage = CTkImage(light_image=self.__image, size=(1920, 200))

        self.__about_label = CTkLabel(self, text="About Gethub", font=("Arial", 32), image=self.__ctkimage, compound="center")
        self.__about_label.pack()

        self.__text = (
            "Gethub is a new ride-booking platform made in the Philippines with the main purpose of providing affordable rides for everyone. As we say, “Booking isn’t a luxury, it’s a necessity.”\n\n"
            "Gethub provides effortless booking and budget-friendly rides for every customer. We offer rides including sedans, vans, or motorcycles, with verified drivers trained professionally to ensure your safety and satisfaction.\n\n"
            "Book stress-free as our rides will take the shortest route possible with our smart routing system. Thanks to this technology, we ensure that you won’t have to drain your wallet just to get to your destination.\n\n"
            "Gethub is proudly developed by computer engineering students of the Polytechnic University of the Philippines - College of Engineering as part of CMPE 103 (Object Oriented Programming) final project requirement."
        )

        self.__about_text = CTkLabel(self, text=self.__text, wraplength=1000, justify="left", font=("Arial", 16))
        self.__about_text.pack(padx=30, pady=30)

        self.__meet_the_team_label = CTkLabel(self, text="Meet the Team", font=("Arial", 32))
        self.__meet_the_team_label.pack(padx=30, pady=30)

        self.__members_frame = CTkFrame(self)
        self.__members_frame.pack(padx=30, pady=30, fill="x")
