from customtkinter import *
from components.booking_map import BookingMap
from services.booking.map_manager import MapManager

class BookingPage(CTkFrame):
    def __init__(self, master, app):
        super().__init__(master)
        self.app = app
        self.pack(fill="both", expand=True)

        self.label = CTkLabel(self, text="", anchor=W, font=("Arial", 32))
        self.label.pack(side=TOP, fill="x", padx=15, pady=15)

        self.secondary_frame = CTkFrame(self)
        self.secondary_frame.pack(fill="both", expand=True, padx=15, pady=15)

        self.display_booking_page()
    
    # User will choose pick-up and drop-off locations
    def display_booking_page(self):
        self.label.configure(text="Select your destination!")

        # ----- LEFT AND RIGHT FRAMES -----
        self.map_frame = CTkFrame(self.secondary_frame)
        self.map_frame.pack(side=RIGHT, fill="both", expand=True, padx=15, pady=15)

        self.prompts_frame = CTkFrame(self.secondary_frame)
        self.prompts_frame.pack(side=LEFT, fill="both", expand=True, padx=15, pady=15)

        # ----- CREATE THE PROMPTS -----
        self.active_prompt = None
        self.prompt_names = ["Pick-up", "Drop-off", "Vehicle Type"]
        self.buttons = {}
        self.prompts = {}

        for prompt_name in self.prompt_names:
            button = CTkButton(self.prompts_frame, text=prompt_name, anchor=W, font=("Arial", 32), command=lambda name=prompt_name: self.toggle_prompt(name))
            button.pack(fill="x", pady=15, padx=15)
            self.buttons[prompt_name] = button

            prompt = CTkFrame(self.prompts_frame)
            CTkLabel(prompt, text=f"{prompt_name} content here").pack(pady=15)
            self.prompts[prompt_name] = prompt
        
        # ----- GENERATE THE MAP -----
        self.booking_map = BookingMap(self.map_frame)
        self.map_manager = MapManager(self.booking_map)
        self.map_manager.initialize_map()
    
    def toggle_prompt(self, prompt_name):
        if self.active_prompt:
            self.active_prompt.pack_forget()
            if self.active_prompt == self.prompts[prompt_name]:
                self.active_prompt = None
                return
        
        selected_prompt = self.prompts[prompt_name]
        selected_prompt.pack(fill="x", pady=5, padx=15, after=self.buttons[prompt_name])
        self.active_prompt = selected_prompt
        