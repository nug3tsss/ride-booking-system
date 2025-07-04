from customtkinter import *
from tkinter import filedialog
import requests
import threading
import json

class BookingForm(CTkScrollableFrame):
    """Gets user input and passes it to the BookingMap and BookingInformationManager"""

    def __init__(self, app, master, map_manager, booking_information_manager):
        super().__init__(master)

        f = app.styles
        c = app.styles.colors

        self.configure(scrollbar_button_color=c["card_accent"], scrollbar_button_hover_color=c["scrollbar"])
        self.pack(side=LEFT, fill="both", expand=True, padx=15, pady=15)

        self.__map_manager = map_manager
        self.__app = app
        self.__booking_information_manager = booking_information_manager

        self.__initialize_autosuggest_api()

        self.__create_pickup_entry()
        self.__create_dropoff_entry()
        self.__create_vehicle_select()
        self.__create_import_and_clear_buttons()
        self.__bind_form_entry_events()

        self.__restore_information_from_previous()
    
    def __initialize_autosuggest_api(self):
        self.__API_KEY = "86f10e4840eb45f4b94f17fce6d3fcec"
        self.__after_id = None
        self.__min_chars = 4
        self.__debounce_ms = 0
        self.__autosuggest_popup_frame = None
    
    def __create_pickup_entry(self):
        c = self.__app.styles.colors
        f = self.__app.styles

        select_pickup_label = CTkLabel(self, text="Select a pickup destination", anchor="w", font=f.font_h1)
        select_pickup_label.pack(fill="x", pady=(15,5), padx=15)

        self.__select_pickup_frame = CTkFrame(self)
        self.__select_pickup_frame.pack(fill="x", pady=5, padx=15, after=select_pickup_label)

        self.__select_pickup_entry = CTkEntry(self.__select_pickup_frame, placeholder_text="Search for a destination...")
        self.__select_pickup_entry.pack(fill="x", pady=15, padx=15, ipady=5)
   
    def __create_dropoff_entry(self):
        c = self.__app.styles.colors
        f = self.__app.styles

        select_dropoff_label = CTkLabel(self, text="Select a dropoff destination", anchor="w", font=f.font_h1)
        select_dropoff_label.pack(fill="x", pady=(15,0), padx=15)

        self.__select_dropoff_frame = CTkFrame(self)
        self.__select_dropoff_frame.pack(fill="x", pady=5, padx=15, after=select_dropoff_label)

        self.__select_dropoff_entry = CTkEntry(self.__select_dropoff_frame, placeholder_text="Search for a destination...")
        self.__select_dropoff_entry.pack(fill="x", pady=15, padx=15, ipady=5)
   
    def __create_vehicle_select(self):
        c = self.__app.styles.colors
        f = self.__app.styles

        select_vehicle_label = CTkLabel(self, text="Select a vehicle", anchor="w", font=f.font_h1)
        select_vehicle_label.pack(fill="x", pady=(15,0), padx=15)

        select_vehicle_frame = CTkFrame(self)
        select_vehicle_frame.pack(fill="x", pady=5, padx=15, after=select_vehicle_label)

        self.__vehicle_var = IntVar(value=0)
        vehicle1 = CTkRadioButton(select_vehicle_frame, text="Car (4-seater)", command=self.__set_vehicle_type, variable=self.__vehicle_var, value=1)
        vehicle1.pack(fill="x", pady=(15,10), padx=15)

        vehicle2 = CTkRadioButton(select_vehicle_frame, text="Van (12-seater)", command=self.__set_vehicle_type, variable=self.__vehicle_var, value=2)
        vehicle2.pack(fill="x", pady=10, padx=15)

        vehicle3 = CTkRadioButton(select_vehicle_frame, text="Motorcycle (2-seater)", command=self.__set_vehicle_type, variable=self.__vehicle_var, value=3)
        vehicle3.pack(fill="x", pady=(10,15), padx=15)
    
    def __create_import_and_clear_buttons(self):
        import_button = CTkButton(self, text="Import booking", command=self.__import_booking_from_file)
        import_button.pack(fill="x", pady=(20,10), padx=15)

        import_button = CTkButton(self, text="Clear booking", command=self.__clear_form_entries)
        import_button.pack(fill="x", pady=(10,15), padx=15)
    
    def __bind_form_entry_events(self):
        self.__select_pickup_entry.bind("<KeyRelease>", lambda event: self.__on_key_released(self.__select_pickup_entry, event))
        self.__select_dropoff_entry.bind("<KeyRelease>", lambda event: self.__on_key_released(self.__select_dropoff_entry, event))

    def __set_vehicle_type(self):
        vehicle_type_int = self.__vehicle_var.get()

        if vehicle_type_int == 1:
            vehicle_type_str = "Car"
        elif vehicle_type_int == 2:
            vehicle_type_str = "Van"
        elif vehicle_type_int == 3:
            vehicle_type_str = "Motorcycle"

        self.__booking_information_manager.set_vehicle_type_str(vehicle_type_str)
        self.__booking_information_manager.set_vehicle_type_int(vehicle_type_int)

    def __on_key_released(self, form_entry_name, event):
        if self.__after_id:
            self.after_cancel(self.__after_id)
            self.__after_id = None

        entry_input = form_entry_name.get()

        if len(entry_input.strip()) >= self.__min_chars:
            self.__after_id = self.after(self.__debounce_ms, lambda: self.__generate_autosuggest(form_entry_name, entry_input))
        else:
            self.__delete_autosuggest()
            return
    
    def __generate_autosuggest(self, form_entry_name, entry_input):
        threading.Thread(target=self.__generate_autosuggest_thread, args=(form_entry_name, entry_input)).start()

    def __generate_autosuggest_thread(self, form_entry_name, entry_input):
        try:
            url = f"https://api.geoapify.com/v1/geocode/autocomplete?text={entry_input}&lang=en&limit=10&apiKey={self.__API_KEY}"
            response = requests.get(url)
            data = response.json()

            self.after(0, lambda: self.__display_autosuggest_results(form_entry_name, data))
        except Exception as e:
            print("Connection Timed Out", e)
    
    def __display_autosuggest_results(self, form_entry_name, data):
        c = self.__app.styles.colors
        f = self.__app.styles

        if not self.__autosuggest_popup_frame:
            if form_entry_name is self.__select_pickup_entry:
                self.__autosuggest_popup_frame = CTkScrollableFrame(self.__select_pickup_frame, scrollbar_button_color=c["scrollbar"], scrollbar_button_hover_color=c["scrollbar_hover"])
                self.__autosuggest_popup_frame.pack(fill="x", pady=15, padx=15)
            elif form_entry_name is self.__select_dropoff_entry:
                self.__autosuggest_popup_frame = CTkScrollableFrame(self.__select_dropoff_frame, scrollbar_button_color=c["scrollbar"], scrollbar_button_hover_color=c["scrollbar_hover"])
                self.__autosuggest_popup_frame.pack(fill="x", pady=15, padx=15)
        else:
            for widget in self.__autosuggest_popup_frame.winfo_children():
                widget.destroy()
        
        count = 0
        for feature in data.get("features", []):
            props = feature["properties"]
            address = props.get("formatted")
            country_code = props.get("country_code")
            country = props.get("country")

            if country_code == "PH" or country == "Philippines":
                    label = CTkLabel(self.__autosuggest_popup_frame, text=address, fg_color=c["card_accent"], corner_radius=5, anchor="w")
                    label.pack(fill="x", pady=2, anchor=W)
                    label.bind("<Button-1>", lambda e, a=address, f=form_entry_name: (self.__confirm_entry(a, f), self.__delete_autosuggest()))
                    count += 1
                            
            if count >= 5:
                break
    
    def __confirm_entry(self, address, form_entry_name):
        if form_entry_name is self.__select_pickup_entry:
            self.__map_manager.get_coords_from_address(address, "pickup", callback=self.__update_entry)
        elif form_entry_name is self.__select_dropoff_entry:
            self.__map_manager.get_coords_from_address(address, "dropoff", callback=self.__update_entry)

    def __update_entry(self, address, destination):
        if destination == "pickup":
            self.__select_pickup_entry.delete(0, END)
            self.__select_pickup_entry.configure(placeholder_text=address)
        elif destination == "dropoff":
            self.__select_dropoff_entry.delete(0, END)
            self.__select_dropoff_entry.configure(placeholder_text=address)

    def __delete_autosuggest(self):
        if self.__autosuggest_popup_frame:
            for widget in self.__autosuggest_popup_frame.winfo_children():
                widget.pack_forget()
        
            self.__autosuggest_popup_frame.pack_forget()
            self.__autosuggest_popup_frame = None
        
    def __restore_information_from_previous(self):
        pickup = self.__booking_information_manager.get_pickup_address()
        dropoff = self.__booking_information_manager.get_dropoff_address()
        vehicle_type = self.__booking_information_manager.get_vehicle_type_int()

        if pickup != "":
            self.__select_pickup_entry.configure(placeholder_text=pickup)
        
        if dropoff != "":
            self.__select_dropoff_entry.configure(placeholder_text=dropoff)
        
        if vehicle_type is not None:
            self.__vehicle_var.set(vehicle_type)
        
    def __import_booking_from_file(self):
        file_path = filedialog.askopenfilename(
            title="Select a booking file",
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")]
        )

        if file_path:
            self.__booking_information_manager.clear_booking_information()

            try:
                with open(file_path, 'r') as file:
                    data = json.load(file)

                    self.__booking_information_manager.set_pickup_address(data.get("pickup_address", ""))
                    self.__booking_information_manager.set_dropoff_address(data.get("dropoff_address", ""))
                    self.__booking_information_manager.set_vehicle_type_int(data.get("vehicle_type_int", 0))

                    self.__vehicle_var.set(self.__booking_information_manager.get_vehicle_type_int())
                    self.__set_vehicle_type()

                    self.after(250, self.__confirm_entry(self.__booking_information_manager.get_pickup_address(), self.__select_pickup_entry))
                    self.after(500, lambda: self.__confirm_entry(self.__booking_information_manager.get_dropoff_address(), self.__select_dropoff_entry))

                    print("Booking information imported successfully.")
            
            except Exception as e:
                print(f"Error importing booking information: {e}")
    
    def __clear_form_entries(self):
        self.__booking_information_manager.clear_booking_information()
        self.__app.show_page("Booking")
    