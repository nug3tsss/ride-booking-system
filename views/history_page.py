from customtkinter import *
from database.db_handler import DatabaseHandler
from datetime import datetime
from tkinter import messagebox
from tkinter import messagebox, filedialog
from PIL import Image
import json

class HistoryPage(CTkFrame):
    def __init__(self, master, app):
        super().__init__(master)
        self.app = app
        self.pack(fill="both", expand=True)

        self.db_handler = DatabaseHandler()
        self.download_icon = CTkImage(Image.open("assets/download_icon-dark.png"))
        # Title
        CTkLabel(self, text="Your Ride History", font=("Arial", 24, "bold")).pack(pady=20)

        # Create main container for the table
        self.table_container = CTkFrame(self, fg_color="transparent")
        self.table_container.pack(fill="both", expand=True, padx=20, pady=10)

        # Create scrollable frame for the table
        self.table_frame = CTkScrollableFrame(self.table_container, width=1000, height=500)
        self.table_frame.pack(fill="both", expand=True)

        # Load booking history
        self.create_table()

    def create_table(self):
        # Clear existing widgets
        for widget in self.table_frame.winfo_children():
            widget.destroy()

        user_id = None
        # Check if a user is currently logged in
        if self.app.current_user:
            user_id = self.app.current_user.get('user_id')

        # If no user is logged in, display a message and return
        if user_id is None:
            no_user_frame = CTkFrame(self.table_frame, fg_color="#2a2a2a", corner_radius=10)
            no_user_frame.pack(fill="x", padx=10, pady=20)
            CTkLabel(no_user_frame, text="Please log in to view your booking history.", 
                    font=("Arial", 16)).pack(pady=20)
            return

        # Fetch bookings specific to the logged-in user
        bookings = self.db_handler.get_bookings_by_user(user_id)

        # If no bookings are found for this user, display a message
        if not bookings:
            no_bookings_frame = CTkFrame(self.table_frame, fg_color="#2a2a2a", corner_radius=10)
            no_bookings_frame.pack(fill="x", padx=10, pady=20)
            CTkLabel(no_bookings_frame, text="No booking history found.", 
                    font=("Arial", 16)).pack(pady=20)
            return

        # Create table header
        self.create_table_header()

        # Create table rows
        for i, booking in enumerate(bookings):
            self.create_table_row(booking, i)

    def create_table_header(self):
        """Create the table header with column titles"""
        header_frame = CTkFrame(self.table_frame, fg_color="#1a1a1a", corner_radius=5)
        header_frame.pack(fill="x", padx=5, pady=(0, 2))

        # Configure grid columns with weights
        header_frame.grid_columnconfigure(0, weight=1) 
        header_frame.grid_columnconfigure(1, weight=3)  
        header_frame.grid_columnconfigure(2, weight=3) 
        header_frame.grid_columnconfigure(3, weight=2)  
        header_frame.grid_columnconfigure(4, weight=2) 
        header_frame.grid_columnconfigure(5, weight=1)  
        header_frame.grid_columnconfigure(6, weight=1)  
        header_frame.grid_columnconfigure(7, weight=1)  
        header_frame.grid_columnconfigure(8, weight=2) 

        # Header labels
        headers = [
            "Booking Id", "Pickup", "Destination", "Vehicle", 
            "Driver", "Cost", "Status", "Date"
        ]

        for col, header in enumerate(headers):
            label = CTkLabel(header_frame, text=header, font=("Arial", 18, "bold"))
            label.grid(row=0, column=col, padx=5, pady=10, sticky="w")

    def create_table_row(self, booking, row_index):
        """Create a table row for each booking"""

        row_color = "#2a2a2a" if row_index % 2 == 0 else "#333333"
        
        row_frame = CTkFrame(self.table_frame, fg_color=row_color, corner_radius=10)
        row_frame.pack(fill="x")

        # Configure grid columns with same weights as header
        row_frame.grid_columnconfigure(0, weight=1)
        row_frame.grid_columnconfigure(1, weight=3)
        row_frame.grid_columnconfigure(2, weight=3)
        row_frame.grid_columnconfigure(3, weight=2)
        row_frame.grid_columnconfigure(4, weight=2)
        row_frame.grid_columnconfigure(5, weight=1)
        row_frame.grid_columnconfigure(6, weight=1)
        row_frame.grid_columnconfigure(7, weight=1)

        # Prepare data for display
        booking_id = str(booking['id'])
        pickup = self.truncate_text(booking['pickup'], 30)
        destination = self.truncate_text(booking['destination'], 30)
        vehicle = f"{booking['vehicle_type']} - {booking['license_plate']}" if booking['vehicle_type'] else "N/A"
        driver = booking['driver_name'] if booking['driver_name'] else "N/A"
        cost = f"₱{booking['estimated_cost']:.2f}"
        status = booking['status'].capitalize()
        date = self.format_date(booking['created_at'])

        # Create data list
        row_data = [booking_id, pickup, destination, vehicle, driver, cost, status, date]

        # Create labels for each column
        for col, data in enumerate(row_data):
            label = CTkLabel(row_frame, text=data, font=("Arial", 15))
            label.grid(row=0, column=col, sticky="w")

        # Save Button
        save_button = CTkButton(
            row_frame,
            image=self.download_icon,
            text ="",
            font=("Arial", 10, "bold"),
            width=35,
            height=35,
            fg_color="transparent",
            hover_color="#1a5a8a",
            command=lambda b=booking: self.save_booking_to_json(b)
        )
        save_button.grid(row=0, column=9, padx=5, pady=8, sticky="e")

        # Add hover effect (optional)
        self.add_hover_effect(row_frame, row_color)

    def save_booking_to_json(self, booking_data):
        vehicle_type_map = {
            "Car": 1,
            "Van": 2,
            "Motorcycle": 3
        }
        vehicle_type_str = booking_data.get('vehicle_type', '')
        vehicle_type_int = vehicle_type_map.get(vehicle_type_str, 0)

        export_data = {
            "pickup_address": booking_data.get('pickup', ''),
            "dropoff_address": booking_data.get('destination', ''),
            "vehicle_type_int": vehicle_type_int
        }
        file_path = filedialog.asksaveasfilename(
            defaultextension=".json",
            filetypes=[("   JSON files", "*.json"), ("All files", "*.*")],
            initialfile=f"booking_{booking_data['id']}.json" # Suggest a filename
        )
        if file_path:
            try:
                with open(file_path, 'w') as f:
                    json.dump(export_data, f, indent=4) # Use indent for pretty printing
                messagebox.showinfo("Success", f"Booking {booking_data['id']} saved successfully to:\n{file_path}")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to save booking: {e}")

    def truncate_text(self, text, max_length):
        """Truncate text if it's too long"""
        if text and len(text) > max_length:
            return text[:max_length-3] + "..."
        return text if text else "N/A"

    def format_date(self, date_string):
        """Format the date string for display"""
        if isinstance(date_string, str):  # Check if date_string is a string
            try:
                # SQLite stores TIMESTAMP as 'YYYY-MM-DD HH:MM:SS.SSSSSS'
                date_obj = datetime.fromisoformat(date_string)
                return date_obj.strftime("%m/%d/%Y %H:%M")  # Include time for more detail
            except ValueError:
                # Fallback for unexpected date formats
                return date_string.split(' ')[0] if ' ' in date_string else date_string  # Just date part


    def add_hover_effect(self, frame, original_color):
        """Add hover effect to table rows"""
        def on_enter(event):
            frame.configure(fg_color="#404040")

        def on_leave(event):
            frame.configure(fg_color=original_color)

        frame.bind("<Enter>", on_enter)
        frame.bind("<Leave>", on_leave)

        # Bind to all child widgets as well
        for child in frame.winfo_children():
            child.bind("<Enter>", on_enter)
            child.bind("<Leave>", on_leave)

    def refresh_history(self):
        """Refresh the booking history table"""
        self.create_table()

