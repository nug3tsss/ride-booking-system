from customtkinter import *
from tkinter import filedialog
import requests
import threading

class BookingForm(CTkScrollableFrame):
    """
    Gets user input and passes it to the BookingMap and BookingInformationManager
    """

    def __init__(self, app, master_frame, map_manager, booking_information_manager):
        super().__init__(master_frame)
        self.configure(scrollbar_button_color="#333333", scrollbar_button_hover_color="#333333")
        self.pack(side=LEFT, fill="both", expand=True, padx=15, pady=15)

        self.__map_manager = map_manager
        self.__app = app
        self.__booking_information_manager = booking_information_manager

        self.__API_KEY = "86f10e4840eb45f4b94f17fce6d3fcec"
        self.__after_id = None
        self.__min_chars = 4
        self.__debounce_ms = 0
        self.__autosuggest_popup_frame = None

        self.__create_form_labels()
        self.__create_form_entries()
        self.__create_import_and_clear_buttons()
        self.__bind_form_entry_events()

        self.__restore_information_from_previous()
   
    def __create_form_labels(self):
        self.__select_pickup_label = CTkLabel(self, text="Select a pickup destination", anchor="w", font=("Arial", 32))
        self.__select_pickup_label.pack(fill="x", pady=15, padx=15)

        self.__select_dropoff_label = CTkLabel(self, text="Select a dropoff destination", anchor="w", font=("Arial", 32))
        self.__select_dropoff_label.pack(fill="x", pady=15, padx=15)

        self.__select_vehicle_label = CTkLabel(self, text="Select a vehicle", anchor="w", font=("Arial", 32))
        self.__select_vehicle_label.pack(fill="x", pady=15, padx=15)
   
    def __create_form_entries(self):
        self.__select_pickup_frame = CTkFrame(self)
        self.__select_pickup_frame.pack(fill="x", pady=5, padx=15, after=self.__select_pickup_label)

        self.__select_dropoff_frame = CTkFrame(self)
        self.__select_dropoff_frame.pack(fill="x", pady=5, padx=15, after=self.__select_dropoff_label)

        self.__select_vehicle_frame = CTkFrame(self)
        self.__select_vehicle_frame.pack(fill="x", pady=5, padx=15, after=self.__select_vehicle_label)

        self.__select_pickup_entry = CTkEntry(self.__select_pickup_frame, placeholder_text="Search for a destination...")
        self.__select_pickup_entry.pack(fill="x", pady=15, padx=15)

        self.__select_dropoff_entry = CTkEntry(self.__select_dropoff_frame, placeholder_text="Search for a destination...")
        self.__select_dropoff_entry.pack(fill="x", pady=15, padx=15)

        self.__vehicle_var = IntVar(value=0)
        self.__vehicle1 = CTkRadioButton(self.__select_vehicle_frame, text="Car (4-seater)", command=self.__set_vehicle_type, variable=self.__vehicle_var, value=1)
        self.__vehicle1.pack(fill="x", pady=15, padx=15)

        self.__vehicle2 = CTkRadioButton(self.__select_vehicle_frame, text="Van (12-seater)", command=self.__set_vehicle_type, variable=self.__vehicle_var, value=2)
        self.__vehicle2.pack(fill="x", pady=15, padx=15)

        self.__vehicle3 = CTkRadioButton(self.__select_vehicle_frame, text="Motorcycle (2-seater)", command=self.__set_vehicle_type, variable=self.__vehicle_var, value=3)
        self.__vehicle3.pack(fill="x", pady=15, padx=15)
    
    def __create_import_and_clear_buttons(self):
        self.__import_button = CTkButton(self, text="Import booking", command=self.__import_booking_from_file)
        self.__import_button.pack(fill="x", pady=15, padx=15)

        self.__import_button = CTkButton(self, text="Clear booking", command=self.__clear_form_entries)
        self.__import_button.pack(fill="x", pady=15, padx=15)
    
    def __import_booking_from_file(self):
        file_path = filedialog.askopenfilename(
            title="Select a booking file",
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")]
        )

        if file_path:
            print("YOU HAVE SELECTED A FILE!")
    
    def __clear_form_entries(self):
        self.__booking_information_manager.clear_booking_information()
        self.__app.show_page("Booking")

    def __bind_form_entry_events(self):
        self.__select_pickup_entry.bind("<KeyRelease>", lambda event: self.__on_key_released(self.__select_pickup_entry, event))
        self.__select_dropoff_entry.bind("<KeyRelease>", lambda event: self.__on_key_released(self.__select_dropoff_entry, event))

    def __set_vehicle_type(self):
        __vehicle_type_int = self.__vehicle_var.get()

        if __vehicle_type_int == 1:
            __vehicle_type_str = "Car"
        elif __vehicle_type_int == 2:
            __vehicle_type_str = "Van"
        elif __vehicle_type_int == 3:
            __vehicle_type_str = "Motorcycle"

        self.__booking_information_manager.set_vehicle_type_str(__vehicle_type_str)
        self.__booking_information_manager.set_vehicle_type_int(__vehicle_type_int)

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
        # Create frame
        if not self.__autosuggest_popup_frame:
            if form_entry_name is self.__select_pickup_entry:
                self.__autosuggest_popup_frame = CTkScrollableFrame(self.__select_pickup_frame, scrollbar_button_color="#333333", scrollbar_button_hover_color="#333333")
                self.__autosuggest_popup_frame.pack(fill="x", pady=15, padx=15)
            elif form_entry_name is self.__select_dropoff_entry:
                self.__autosuggest_popup_frame = CTkScrollableFrame(self.__select_dropoff_frame, scrollbar_button_color="#333333", scrollbar_button_hover_color="#333333")
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
                    label = CTkLabel(self.__autosuggest_popup_frame, text=address, fg_color="gray20", corner_radius=5, anchor="w")
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
        __pickup = self.__booking_information_manager.get_pickup_address()
        __dropoff = self.__booking_information_manager.get_dropoff_address()
        __vehicle_type = self.__booking_information_manager.get_vehicle_type_int()

        if __pickup != "":
            self.__select_pickup_entry.configure(placeholder_text=__pickup)
        
        if __dropoff != "":
            self.__select_dropoff_entry.configure(placeholder_text=__dropoff)
        
        if __vehicle_type is not None:
            self.__vehicle_var.set(__vehicle_type)
