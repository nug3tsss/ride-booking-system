from customtkinter import *
from PIL import Image, ImageOps, ImageDraw

class AboutPage(CTkFrame):
    def __init__(self, master, app):
        super().__init__(master)

        self.app = app

        self.original_image = Image.open("assets/user_8_profile.png")
        self.about_image = CTkImage(light_image=self.original_image, dark_image=self.original_image, size=(100, 100))

        self.bind("<Configure>", self.resize_image)
        self.bind("<Configure>", self.adjust_wraplength, add="+")

        self.__about_label = CTkLabel(self, text="About Us", font=("Arial", 32, "bold"), image=self.about_image, compound="center")
        self.__about_label.pack()

        self.__text = (
            "Gethub is a new ride-booking platform made in the Philippines with the main purpose of providing affordable rides for everyone. As we say, “Booking isn’t a luxury, it’s a necessity.”\n\n"
            "Gethub provides effortless booking and budget-friendly rides for every customer. We offer rides including sedans, vans, or motorcycles, with verified drivers trained professionally to ensure your safety and satisfaction.\n\n"
            "Book stress-free as our rides will take the shortest route possible with our smart routing system. Thanks to this technology, we ensure that you won’t have to drain your wallet just to get to your destination.\n\n"
            "Gethub is proudly developed by computer engineering students of the Polytechnic University of the Philippines - College of Engineering as part of CMPE 103 (Object Oriented Programming) final project requirement."
        )

        self.__about_text = CTkLabel(self, text=self.__text, wraplength=1000, justify="left", font=("Arial", 20))
        self.__about_text.pack(pady=30)

        self.__meet_the_team_label = CTkLabel(self, text="Meet the Team", font=("Arial", 32,"bold"), anchor="w")
        self.__meet_the_team_label.pack(pady=30)

        self.__members_frame = CTkFrame(self, fg_color="transparent")
        self.__members_frame.pack(fill="both")

        self.add_members()

    def add_members(self):
        rows = 2
        cols = 4

        members = [
            {"name": "Mark Christian Abucejo", "role": "Lead Developer"},
            {"name": "Zybert Jio Sibolboro", "role": "Full-stack Developer"},
            {"name": "Lorens Aron Mercado", "role": "Back-end Developer"},
            {"name": "Renier Dela Cruz", "role": "Back-end Developer"},
            {"name": "Kathlyn Estorco", "role": "UI/UX Designer"},
            {"name": "Maeryl Venida", "role": "UI/UX Designer"},
            {"name": "Luke Philip Lopez", "role": "QA/Test Engineer"}
        ]

        for row in range(rows):
            self.__members_frame.rowconfigure(row, weight=1)
        for col in range(cols):
            self.__members_frame.columnconfigure(col, weight=1)
        
        image_raw = self.original_image.resize((100, 100))
        mask = Image.new("L", image_raw.size, 0)
        draw = ImageDraw.Draw(mask)
        draw.ellipse((0, 0) + image_raw.size, fill=255)
        circular_profile = ImageOps.fit(image_raw, image_raw.size, centering=(0.5, 0.5))
        circular_profile.putalpha(mask)
        circular_profile = CTkImage(light_image=circular_profile, dark_image=circular_profile, size=(100, 100))

        member_index = 0
        for row in range(rows):
            for col in range(cols):
                frame = CTkFrame(self.__members_frame, fg_color="transparent")
                frame.grid(row=row, column=col, padx=10, pady=10, sticky="nsew")

                # Image label
                if row == 1 and col == 3:
                    pass
                else:
                    img_label = CTkLabel(frame, text="", image=circular_profile)
                    img_label.pack()

                # Name and role labels if member exists
                if member_index < len(members):
                    member = members[member_index]

                    name_label = CTkLabel(frame, text=member["name"], font=("Arial", 14, "bold"), wraplength=150, justify="center")
                    name_label.pack(pady=(5,0))

                    role_label = CTkLabel(frame, text=member["role"], font=("Arial", 12), wraplength=150, justify="center")
                    role_label.pack()
                    
                    member_index += 1
    
    def adjust_wraplength(self, event):
        available_width = self.winfo_width() - 200
        self.__about_text.configure(wraplength=available_width)
    
    def resize_image(self, event):
        available_width = self.winfo_width() # Full width, no padding subtraction
        desired_height = 200
        if available_width > 0:
            # Resize and crop image to fill the width and crop vertically
            fitted_image = ImageOps.fit(
                self.original_image,
                (available_width, desired_height),
                method=Image.Resampling.LANCZOS,
                centering=(0.5, 0.3)  # crop bias slightly upward if needed
            )

            self.about_image = CTkImage(
                light_image=fitted_image,
                dark_image=fitted_image,
                size=(available_width, desired_height)
            )
            self.__about_label.configure(image=self.about_image)