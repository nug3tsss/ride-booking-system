from customtkinter import *

class BookingForm(CTkFrame):
    def __init__(self, master_frame):
        super().__init__(master_frame)

        self.is_prompt_active = False

        self.create_form_labels()
        self.create_form_prompts()
    
    def create_form_labels(self):
        self.select_pickup_label = CTkLabel(self, text="Select a pickup destination", anchor="w", font=("Arial", 32))
        self.select_pickup_label.pack(fill="x", pady=15, padx=15)

        self.select_dropoff_label = CTkLabel(self, text="Select a dropoff destination", anchor="w", font=("Arial", 32))
        self.select_dropoff_label.pack(fill="x", pady=15, padx=15)

        self.select_vehicle_label = CTkLabel(self, text="Select a vehicle", anchor="w", font=("Arial", 32))
        self.select_vehicle_label.pack(fill="x", pady=15, padx=15)
    
    def create_form_prompts(self):
        self.select_vehicle_frame = CTkFrame(self)
        self.select_vehicle_frame.pack(fill="x", pady=5, padx=15, after=self.select_vehicle_label)

        self.select_pickup_frame = CTkFrame(self)
        self.select_pickup_frame.pack(fill="x", pady=5, padx=15, after=self.select_pickup_label)

        self.select_dropoff_frame = CTkFrame(self)
        self.select_dropoff_frame.pack(fill="x", pady=5, padx=15, after=self.select_dropoff_label)

        self.vehicle_var = IntVar(value=0)
        self.vehicle1 = CTkRadioButton(self.select_vehicle_frame, text="Vehicle 1", variable=self.vehicle_var, value=1)
        self.vehicle2 = CTkRadioButton(self.select_vehicle_frame, text="Vehicle 2", variable=self.vehicle_var, value=2)
        self.vehicle3 = CTkRadioButton(self.select_vehicle_frame, text="Vehicle 3", variable=self.vehicle_var, value=3)
        self.vehicle1.pack(fill="x", pady=15, padx=15)
        self.vehicle2.pack(fill="x", pady=15, padx=15)
        self.vehicle3.pack(fill="x", pady=15, padx=15)

        self.select_pickup_entry = CTkEntry(self.select_pickup_frame, placeholder_text="Enter a pickup destination")
        self.select_pickup_entry.pack(fill="x", pady=15, padx=15)
        self.select_pickup_entry.bind("<Return>", lambda event: self.on_entry_entered(self.select_pickup_entry, event))

        self.select_dropoff_entry = CTkEntry(self.select_dropoff_frame, placeholder_text="Enter a dropoff destination")
        self.select_dropoff_entry.pack(fill="x", pady=15, padx=15)
        self.select_dropoff_entry.bind("<Return>", lambda event: self.on_entry_entered(self.select_dropoff_entry, event))
    
    def on_entry_entered(self, form_entry_name, event):
        self.entry_input = form_entry_name.get()

        # CALL BOOKING INFORMATION MANAGER TO CONVERT ADDRESS TO COORDINATES
