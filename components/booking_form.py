from customtkinter import *
import requests

class BookingForm(CTkScrollableFrame):
    """
    Gets user input and passes it to the BookingMap and BookingInformationManager
    """

    def __init__(self, master_frame, map_manager, booking_information_manager):
        super().__init__(master_frame)
        self.configure(scrollbar_button_color="#333333", scrollbar_button_hover_color="#333333")
        self.map_manager = map_manager
        self.booking_information_manager = booking_information_manager

        # AUTOSUGGEST IMPLEMENTATION
        self.API_KEY = "86f10e4840eb45f4b94f17fce6d3fcec"
        self.after_id = None
        self.min_chars = 5
        self.debounce_ms = 500

        self.is_prompt_active = False

        self.autosuggest_popup_frame = None

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
        self.select_pickup_entry.bind("<KeyRelease>", self.on_key_release)
        self.select_pickup_entry.bind("<FocusOut>", self.delete_autosuggest_options)

        self.select_dropoff_entry = CTkEntry(self.select_dropoff_frame, placeholder_text="Enter a dropoff destination")
        self.select_dropoff_entry.pack(fill="x", pady=15, padx=15)
        self.select_dropoff_entry.bind("<Return>", lambda event: self.on_entry_entered(self.select_dropoff_entry, event))
        # self.select_dropoff_entry.bind("<KeyRelease>", lambda event: self.generate_autosuggest_options(self.select_dropoff_entry, event))
        # self.select_dropoff_entry.bind("<FocusOut>", self.delete_autosugget_options)
   
    def on_entry_entered(self, form_entry_name, event):
        self.entry_input = form_entry_name.get()

        if self.after_id:
            self.after_cancel(self.after_id)
            self.after_id = None
        
        self.clear_suggestions()
        self.delete_autosuggest_options(event)

        if form_entry_name is self.select_pickup_entry:
            self.map_manager.get_coords_from_address(self.entry_input, "pickup", callback=self.update_pickup_entry)
            
        elif form_entry_name is self.select_dropoff_entry:
            self.map_manager.get_coords_from_address(self.entry_input, "dropoff", callback=self.update_dropoff_entry)
            
    def update_pickup_entry(self, pickup_address):
        self.select_pickup_entry.delete(0, END)
        self.select_pickup_entry.insert(0, pickup_address)

    def update_dropoff_entry(self, dropoff_address):
        self.select_dropoff_entry.delete(0, END)
        self.select_dropoff_entry.insert(0, dropoff_address)
    
    def generate_autosuggest_options(self, form_entry_name):
        if self.autosuggest_popup_frame is None:
            if form_entry_name is self.select_pickup_entry:
                self.autosuggest_popup_frame = CTkScrollableFrame(self.select_pickup_frame)
                self.autosuggest_popup_frame.pack(fill="x", pady=15, padx=15)
            elif form_entry_name is self.select_dropoff_entry:
                self.autosuggest_popup_frame = CTkScrollableFrame(self.select_dropoff_frame)
                self.autosuggest_popup_frame.pack(fill="x", pady=15, padx=15)
        else:
            return
   
    def delete_autosuggest_options(self, event):
        if self.autosuggest_popup_frame is not None:
            self.autosuggest_popup_frame.pack_forget()
            self.autosuggest_popup_frame = None
    
    # # AUTOSUGGEST IMPLEMENTATION
    def on_key_release(self, event):
        if event.keysym == "Return":
            if self.after_id:
                self.after_cancel(self.after_id)
                self.after_id = None
            self.clear_suggestions()
            self.delete_autosuggest_options(event)
            return

        if self.after_id:
            self.after_cancel(self.after_id)
        
        text = self.select_pickup_entry.get()
        if len(text.strip()) >= self.min_chars:
            self.generate_autosuggest_options(self.select_pickup_entry)
            self.after_id = self.after(self.debounce_ms, self.perform_search)
        else:
            self.clear_suggestions()
            self.delete_autosuggest_options(event)
    
    def perform_search(self):
        text = self.select_pickup_entry.get()
        url = f"https://api.geoapify.com/v1/geocode/autocomplete?text={text}&lang=en&limit=10&apiKey={self.API_KEY}"
        response = requests.get(url)

        if response.status_code != 200:
            self.clear_suggestions()
            return
        
        data = response.json()
        self.clear_suggestions()

        count = 0
        for feature in data.get("features", []):
            props = feature["properties"]
            address = props.get("formatted")
            country_code = props.get("country_code")
            country = props.get("country")

            if country_code == "PH" or country == "Philippines":
                label = CTkLabel(self.autosuggest_popup_frame, text=address, fg_color="gray20", corner_radius=5)
                label.pack(fill="x", pady=2)
                label.bind("<Button-1>", lambda e, a=address: self.select_suggestion(a))
                label.bind("<Button-1>", self.delete_autosuggest_options)
                count += 1
            
            if count >= 5:
                break
    
    def clear_suggestions(self):
        if self.autosuggest_popup_frame is not None:
            for widget in self.autosuggest_popup_frame.winfo_children():
                widget.pack_forget()
    
    def select_suggestion(self, address):
        self.select_pickup_entry.delete(0, END)
        self.select_pickup_entry.insert(0, address)
        self.clear_suggestions()