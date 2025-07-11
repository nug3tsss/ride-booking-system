from customtkinter import *
from PIL import Image, ImageOps
from components.contact_form import ContactForm

class ContactPage(CTkFrame):
    """Contact Page of the application, allowing users to send messages or inquiries."""

    def __init__(self, master, app):
        super().__init__(master)
        self.app = app

        c = self.app.styles.colors
        f = self.app.styles

        # Scrollable frame
        self.scrollable_frame = CTkScrollableFrame(self, corner_radius=15, fg_color="transparent")
        self.scrollable_frame.pack(fill="both", expand=True, pady=0, padx=0)

        # Top banner image
        self.original_image = Image.open("assets/banners/contact_image.jpg")
        self.contact_image = CTkImage(self.original_image, size=(100, 100))

        self.bind("<Configure>", self.resize_image)
        self.bind("<Configure>", self.adjust_wraplength, add="+")

        self.title_label = CTkLabel(
            self.scrollable_frame,
            text="Contact Us",
            text_color="white",
            font=f.font_h1,
            image=self.contact_image,
            compound="center"
        )
        self.title_label.pack()

        # Intro heading
        intro_heading = CTkLabel(
            self.scrollable_frame,
            text="How can we help you?",
            font=f.font_h2,
            anchor="center"
        )
        intro_heading.pack(pady=(20, 10))

        # Intro body
        self.intro_label = CTkLabel(
            self.scrollable_frame,
            text="If you have any comments, suggestions or questions, please do not hesitate to contact us.\n"
                 "We'll do our best to help and respond as soon as possible.",
            font=f.font_h3p,
            wraplength=1000,
            justify="center"
        )
        self.intro_label.pack(pady=(0, 30))

        # Info section: Address, Phone, Email
        self.create_contact_info()

        # Contact form component
        self.contact_form = ContactForm(self.scrollable_frame, app)
        self.contact_form.pack(pady=(40, 20), fill="x", padx=40)

    # Creates the contact information section with address, phone, and email
    def create_contact_info(self):
        f = self.app.styles
        info_frame = CTkFrame(self.scrollable_frame, fg_color="transparent")
        info_frame.pack(pady=10, padx=60, fill="x")

        info_frame.grid_columnconfigure((0, 2, 4), weight=1, uniform="info")
        info_frame.grid_columnconfigure((1, 3), weight=0)

        def create_info_column(light_icon_path, dark_icon_path, label_text, detail_text):
            frame = CTkFrame(info_frame, fg_color="transparent")
            icon = CTkImage(light_image=Image.open(light_icon_path), dark_image=Image.open(dark_icon_path), size=(48, 48))

            icon_label = CTkLabel(frame, image=icon, text="")
            icon_label.pack(pady=(0, 5))

            label = CTkLabel(frame, text=label_text, font=f.font_h4)
            label.pack()

            detail = CTkLabel(frame, text=detail_text, font=f.font_h5p)
            detail.pack(pady=(2, 0))

            return frame

        # Info columns
        address_col = create_info_column("assets/icons/location_icon-light.png", "assets/icons/location_icon-dark.png", "Address", "Sta. Mesa, Manila, PH")
        phone_col = create_info_column("assets/icons/phone_icon-light.png", "assets/icons/phone_icon-dark.png", "Phone", "+63 912 345 6789")
        email_col = create_info_column("assets/icons/email_icon-light.png", "assets/icons/email_icon-dark.png", "Email", "gethub@catgroup.uk")

        # Layout with dividers
        address_col.grid(row=0, column=0, padx=40, pady=10)
        self.add_divider(info_frame, 1)

        phone_col.grid(row=0, column=2, padx=40, pady=10)
        self.add_divider(info_frame, 3)

        email_col.grid(row=0, column=4, padx=40, pady=10)

    # Adds a vertical divider between contact info columns
    def add_divider(self, parent, col):
        c = self.app.styles.colors
        divider = CTkFrame(parent, width=3, fg_color=c["divider"])
        divider.grid(row=0, column=col, sticky="ns", pady=10)

    # Adjusts the wraplength of the intro label based on available width
    def adjust_wraplength(self, event):
        available_width = self.winfo_width() - 200
        self.intro_label.configure(wraplength=available_width)

    # Resizes the contact image based on the available width of the frame
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

            self.contact_image = CTkImage(
                light_image=fitted_image,
                dark_image=fitted_image,
                size=(available_width, desired_height)
            )
            self.title_label.configure(image=self.contact_image)
