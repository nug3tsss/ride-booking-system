from customtkinter import *
from PIL import Image, ImageOps, ImageDraw

class AboutPage(CTkFrame):
    """About Page of the application, providing information about the app and its team."""

    def __init__(self, master, app):
        super().__init__(master)
        self.app = app

        c = self.app.styles.colors
        f = self.app.styles

        self.scrollable_frame = CTkScrollableFrame(self, corner_radius=15, fg_color="transparent")
        self.scrollable_frame.pack(fill="both", expand=True)

        self.original_image = Image.open("assets/banners/about_image.jpg")
        self.about_image = CTkImage(self.original_image, size=(100, 100))

        self.logo_image = CTkImage(
            light_image=Image.open("assets/icons/logo-light--transparent.png"),
            dark_image=Image.open("assets/icons/logo-dark--transparent.png"),
            size=(64, 64)
        )

        self.bind("<Configure>", self.resize_image)
        self.bind("<Configure>", self.adjust_wraplength, add="+")

        self.__about_label = CTkLabel(
            self.scrollable_frame, text="About Us", text_color="white", font=f.font_h1,
            image=self.about_image, compound="center"
        )
        self.__about_label.pack()

        # Logo above the heading
        self.logo_label = CTkLabel(self.scrollable_frame, text="", image=self.logo_image)
        self.logo_label.pack(pady=(30, 10))

        # What is Gethub? Heading
        self.__what_label = CTkLabel(
            self.scrollable_frame,
            text="What is Gethub?",
            font=f.font_h2,
            anchor="center"
        )
        self.__what_label.pack(pady=(0, 10))

        # About Text Card
        about_card = CTkFrame(self.scrollable_frame, fg_color=c["about_card"], corner_radius=10)
        about_card.pack(padx=40, pady=(0, 40), fill="x")

        self.__text = (
            "Gethub is a new ride-booking platform made in the Philippines with the main purpose of providing affordable rides for everyone. "
            "As we say, “Booking isn’t a luxury, it’s a necessity.”\n\n"
            "Gethub provides effortless booking and budget-friendly rides for every customer. We offer rides including sedans, vans, or motorcycles, "
            "with verified drivers trained professionally to ensure your safety and satisfaction.\n\n"
            "Book stress-free as our rides will take the shortest route possible with our smart routing system. Thanks to this technology, "
            "we ensure that you won’t have to drain your wallet just to get to your destination."
        )

        self.__about_text = CTkLabel(
            about_card,
            text=self.__text,
            wraplength=1000,
            justify="left",
            font=f.font_h3p,
            text_color="white",
            anchor="w"
        )
        self.__about_text.pack(padx=30, pady=30)

        # Divider below the About Text
        divider = CTkFrame(self.scrollable_frame, height=2, fg_color=c["divider"])
        divider.pack(fill="x", padx=40, pady=(0, 30))

        # Meet the Team Heading (outside the card)
        self.__meet_the_team_label = CTkLabel(
            self.scrollable_frame, text="Meet the Team",
            font=f.font_h2, anchor="center"
        )
        self.__meet_the_team_label.pack(pady=(10, 20))

        # Team Card
        self.__team_card = CTkFrame(self.scrollable_frame, fg_color=c["about_card"], corner_radius=10)
        self.__team_card.pack(padx=40, pady=(0, 40), fill="x")

        self.__members_frame = CTkFrame(self.__team_card, fg_color="transparent")
        self.__members_frame.pack(padx=30, pady=30, fill="both")
        self.add_members()

    # Adds team members to the About page with their names, roles, and profile pictures
    def add_members(self):
        c = self.app.styles.colors
        f = self.app.styles

        members = [
            {"name": "Mark Christian Abucejo", "role": "Lead Developer"},
            {"name": "Zybert Jio Sibolboro", "role": "Full-stack Developer"},
            {"name": "Lorens Aron Mercado", "role": "Back-end Developer"},
            {"name": "Renier Dela Cruz", "role": "Back-end Developer"},
            {"name": "Kathlyn Estorco", "role": "UI/UX Designer"},
            {"name": "Maeryl Venida", "role": "UI/UX Designer"},
            {"name": "Luke Philip Lopez", "role": "QA/Test Engineer"},
        ]

        picture_paths = ["assets/members_profile/mark_profile.png",
                         "assets/members_profile/zybert_profile.jpg",
                         "assets/members_profile/lorens_profile.jpg",
                         "assets/members_profile/renier_profile.jpg",
                         "assets/members_profile/kath_profile.jpg",
                         "assets/members_profile/maeryl_profile.jpg",
                         "assets/members_profile/luke_profile.jpg"]

        # Main card background
        card_frame = CTkFrame(self.__members_frame, fg_color=c["about_card"], corner_radius=10)
        card_frame.pack(fill="x", padx=40, pady=(10, 40))

        # Top container: 4 members
        top_container = CTkFrame(card_frame, fg_color="transparent")
        top_container.pack(fill="x", padx=20, pady=(20, 10))

        for i in range(4):
            top_container.grid_columnconfigure(i, weight=1)

        # Bottom container: 3 members
        bottom_container = CTkFrame(card_frame, fg_color="transparent")
        bottom_container.pack(fill="x", padx=60, pady=(10, 20))

        for i in range(3):
            bottom_container.grid_columnconfigure(i, weight=1)

        # Add top 4 members
        for i in range(4):
            member = members[i]
            frame = CTkFrame(top_container, fg_color="transparent")
            frame.grid(row=0, column=i, padx=10, pady=10, sticky="nsew")

            member_image = Image.open(picture_paths[i])
            image_raw = member_image.resize((100, 100))
            mask = Image.new("L", image_raw.size, 0)
            draw = ImageDraw.Draw(mask)
            draw.ellipse((0, 0) + image_raw.size, fill=255)
            circular_profile = ImageOps.fit(image_raw, image_raw.size, centering=(0.5, 0.5))
            circular_profile.putalpha(mask)
            circular_profile = CTkImage(circular_profile, size=(100, 100))

            CTkLabel(frame, image=circular_profile, text="").pack()
            CTkLabel(frame, text=member["name"], text_color="white", font=f.font_h5, wraplength=150, justify="center").pack(pady=(5, 0))
            CTkLabel(frame, text=member["role"], text_color="white", font=f.font_p, wraplength=150, justify="center").pack()

        # Add bottom 3 members
        for i in range(3):
            member = members[i + 4]
            frame = CTkFrame(bottom_container, fg_color="transparent")
            frame.grid(row=0, column=i, padx=10, pady=10, sticky="nsew")

            member_image = Image.open(picture_paths[i + 4])
            image_raw = member_image.resize((100, 100))
            mask = Image.new("L", image_raw.size, 0)
            draw = ImageDraw.Draw(mask)
            draw.ellipse((0, 0) + image_raw.size, fill=255)
            circular_profile = ImageOps.fit(image_raw, image_raw.size, centering=(0.5, 0.5))
            circular_profile.putalpha(mask)
            circular_profile = CTkImage(circular_profile, size=(100, 100))

            CTkLabel(frame, image=circular_profile, text="").pack()
            CTkLabel(frame, text=member["name"], text_color="white", font=f.font_h5, wraplength=150, justify="center").pack(pady=(5, 0))
            CTkLabel(frame, text=member["role"], text_color="white", font=f.font_p, wraplength=150, justify="center").pack()

    # Adjusts the wraplength of the about text based on the available width
    def adjust_wraplength(self, event):
        available_width = self.winfo_width() - 200
        self.__about_text.configure(wraplength=available_width)

    # Resizes the about image based on the available width of the frame
    def resize_image(self, event):
        available_width = self.winfo_width()
        desired_height = 200
        if available_width > 0:
            fitted_image = ImageOps.fit(
                self.original_image,
                (available_width, desired_height),
                method=Image.Resampling.LANCZOS,
                centering=(0.5, 0.45)
            )
            self.about_image = CTkImage(
                light_image=fitted_image,
                dark_image=fitted_image,
                size=(available_width, desired_height)
            )
            self.__about_label.configure(image=self.about_image)
