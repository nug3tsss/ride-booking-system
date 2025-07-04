
from customtkinter import *
from database.db_handler import DatabaseHandler
from datetime import datetime
from tkinter import messagebox, filedialog
from PIL import Image
import json
from database.db_handler import DatabaseHandler
from datetime import datetime
from tkinter import messagebox, filedialog
from PIL import Image
import json

class BookingHistoryList(CTkFrame):
    """Displays booking history of specific user in table format"""

    def __init__(self, master, app):
        super().__init__(master, fg_color="transparent")
        self.pack(fill="both", expand=True, padx=20, pady=10)

        self.app = app
        f = self.app.styles

        self.db_handler = DatabaseHandler()
        self.download_icon = CTkImage(light_image=Image.open("assets/download_icon-dark.png"), dark_image=Image.open("assets/download_icon-dark.png"))

        # Title
        CTkLabel(self, text="Your Ride History", font=f.font_h2).pack(pady=20)

        # Create scrollable frame for the table
        self.table_frame = CTkScrollableFrame(self, width=1000, height=500)
        self.table_frame.pack(fill="both", expand=True)

        # Load booking history
        self.create_table()

    def configure_grid_columns(self, frame):
        """Configure grid columns with consistent weights for both header and rows"""
        frame.grid_columnconfigure(0, weight=1, minsize=80)   # Booking ID
        frame.grid_columnconfigure(1, weight=3, minsize=200)  # Pickup
        frame.grid_columnconfigure(2, weight=3, minsize=200)  # Destination  
        frame.grid_columnconfigure(3, weight=2, minsize=150)  # Vehicle
        frame.grid_columnconfigure(4, weight=2, minsize=120)  # Driver
        frame.grid_columnconfigure(5, weight=1, minsize=80)   # Cost
        frame.grid_columnconfigure(6, weight=1, minsize=80)   # Status
        frame.grid_columnconfigure(7, weight=1, minsize=120)  # Date
        frame.grid_columnconfigure(8, weight=0, minsize=50)   # Save button

    def create_table(self):
        c = self.app.styles.colors
        f = self.app.styles

        # Clear existing widgets
        for widget in self.table_frame.winfo_children():
            widget.destroy()

        user_id = None
        # Check if a user is currently logged in
        if self.app.current_user:
            user_id = self.app.current_user.get('user_id')

        # If no user is logged in, display a message and return
        if user_id is None:
            no_user_frame = CTkFrame(self.table_frame, fg_color=c["table_row_even"], corner_radius=10)
            no_user_frame.pack(fill="x", padx=10, pady=20)
            CTkLabel(no_user_frame, text="Please log in to view your booking history.",
                    font=f.font_h4).pack(pady=20)
            return

        # Fetch bookings specific to the logged-in user
        bookings = self.db_handler.get_bookings_by_user(user_id)

        # If no bookings are found for this user, display a message
        if not bookings:
            no_bookings_frame = CTkFrame(self.table_frame, fg_color=c["table_row_even"], corner_radius=10)
            no_bookings_frame.pack(fill="x", padx=10, pady=20)
            CTkLabel(no_bookings_frame, text="No booking history found.",
                    font=(f.font_h4)).pack(pady=20)
            return

        # Create table header
        self.create_table_header()

        # Create table rows
        for i, booking in enumerate(bookings):
            self.create_table_row(booking, i)

    def create_table_header(self):
        f = self.app.styles

        """Create the table header with column titles"""
        header_frame = CTkFrame(self.table_frame, fg_color="#1a1a1a", corner_radius=5)
        header_frame.pack(fill="x", padx=5, pady=(0, 2))

        # Configure grid columns using the shared method
        self.configure_grid_columns(header_frame)

        # Header labels
        headers = [
            "Booking ID", "Pickup", "Destination", "Vehicle",
            "Driver", "Cost", "Status", "Date", "Action"
        ]

        for col, header_text in enumerate(headers):
            label = CTkLabel(header_frame, text=header_text, font=(f.font_h3))
            label.grid(row=0, column=col, padx=5, sticky="ns")

    def create_table_row(self, booking, row_index):
        """Create a table row for each booking"""

        c = self.app.styles.colors
        f = self.app.styles

        row_color = c["table_row_even"] if row_index % 2 == 0 else c["table_row_odd"]

        row_frame = CTkFrame(self.table_frame, fg_color=row_color, corner_radius=5)
        row_frame.pack(fill="x", padx=5, pady=1)

        # Configure grid columns using the shared method
        self.configure_grid_columns(row_frame)

        # Prepare data for display
        booking_id = str(booking['id'])
        pickup = self.truncate_text(booking['pickup'], 25)
        destination = self.truncate_text(booking['destination'], 25)
        vehicle = f"{booking['vehicle_type']}" if booking['vehicle_type'] else "N/A"
        driver = booking['driver_name'] if booking['driver_name'] else "N/A"
        cost = f"₱{booking['estimated_cost']:.2f}"
        status = booking['status'].capitalize()
        date = self.format_date(booking.get('created_at'))

        # Create data list
        row_data = [booking_id, pickup, destination, vehicle, driver, cost, status, date]

        # Create labels for each column
        for col, data in enumerate(row_data):
            label = CTkLabel(row_frame, text=data, font=f.font_p)
            label.grid(row=0, column=col,padx=5, sticky="ns")

        # Save Button (icon only)
        save_button = CTkButton(
            row_frame,
            text="",
            width=35,
            height=35,
            fg_color="transparent",
            hover_color=c["green_hover"],
            image=self.download_icon,
            command=lambda b=booking: self.save_booking_to_json(b)
        )
        save_button.grid(row=0, column=8, padx=10, pady=8, sticky="w")

        # Add hover effect (optional)
        self.add_hover_effect(row_frame, row_color)

    def save_booking_to_json(self, booking_data):
        # Map vehicle type string to integer for export, if needed by the import function
        # This mapping should ideally be consistent with how vehicle_type_int is used in BookingForm
        vehicle_type_map = {
            "Car": 1,
            "Van": 2,
            "Motorcycle": 3
        }
        # Get the vehicle type string from booking_data and convert it to int using the map
        # Default to 0 or None if not found, depending on what the import expects
        vehicle_type_str = booking_data.get('vehicle_type', '')
        vehicle_type_int = vehicle_type_map.get(vehicle_type_str, 0) # Default to 0 if not found

        export_data = {
            "pickup_address": booking_data.get('pickup', ''),
            "dropoff_address": booking_data.get('destination', ''),
            "vehicle_type_int": vehicle_type_int
        }
        file_path = filedialog.asksaveasfilename(
            defaultextension=".json",
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")],
            initialfile=f"booking_{booking_data['id']}.json"
        )
        if file_path:
            try:
                with open(file_path, 'w') as f:
                    json.dump(export_data, f, indent=4)
                messagebox.showinfo("Success", f"Booking {booking_data['id']} saved successfully to:\n{file_path}")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to save booking: {e}")

    def truncate_text(self, text, max_length):
        """Truncate text if it's too long"""
        if text and len(text) > max_length:
            return text[:max_length-3] + "..."
        return text if text else "N/A"

    def format_date(self, date_string):
        if not date_string:
            return "No Date"
        date_str = str(date_string)
        
        try:
            if 'T' in date_str:
                date_obj = datetime.fromisoformat(date_str.replace('T', ' '))
                if '.' in date_str:
                    date_str = date_str.split('.')[0]
                date_obj = datetime.strptime(date_str, "%Y-%m-%d %H:%M:%S")
            elif '-' in date_str and len(date_str) == 10:
                date_obj = datetime.strptime(date_str, "%Y-%m-%d")
            else:
                date_obj = datetime.fromisoformat(date_str)
            
            return date_obj.strftime("%m/%d/%Y")
            
        except (ValueError, TypeError) as e:
            print(f"Date parsing error for '{date_string}': {e}")
            return str(date_string) if len(str(date_string)) < 20 else "Invalid Date"

    def add_hover_effect(self, frame, original_color):
        c = self.app.styles.colors
        
        """Add hover effect to table rows"""
        def on_enter(event):
            frame.configure(fg_color=c["card_light"])

        def on_leave(event):
            frame.configure(fg_color=original_color)

        frame.bind("<Enter>", on_enter)
        frame.bind("<Leave>", on_leave)

        for child in frame.winfo_children():
            child.bind("<Enter>", on_enter)
            child.bind("<Leave>", on_leave)

    def refresh_history(self):
        """Refresh the booking history table"""
        self.create_table()

