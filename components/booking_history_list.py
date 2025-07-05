from customtkinter import *
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

        try:
            self.download_icon = CTkImage(
                light_image=Image.open("assets/icons/download_icon-dark.png"), 
                dark_image=Image.open("assets/icons/download_icon-dark.png")
            )
        except Exception as e:
            print(f"[UI WARNING] Could not load download icon: {e}")
            self.download_icon = None

        # Title
        CTkLabel(self, text="Your Ride History", font=f.font_h2).pack(pady=20)

        # Create scrollable frame for the table
        self.table_scroll_frame = CTkScrollableFrame(self, width=1000, height=500)
        self.table_scroll_frame.pack(fill="both", expand=True)

        self.table_scroll_frame.grid_columnconfigure(0, weight=1)

        # Load booking history
        self.create_table()

    # Creates the booking history table with user bookings
    def create_table(self):
        c = self.app.styles.colors
        f = self.app.styles

        # Clear existing widgets
        for widget in self.table_scroll_frame.winfo_children():
            widget.destroy()

        user_id = None
        user_role = None


        # Check if a user is currently logged in
        if self.app.current_user:
            user_id = self.app.current_user.get('user_id')
            user_role = self.app.current_user.get('role')
            # print(f"[UI DEBUG] Extracted user_id: {user_id}, role: {user_role}")
        else:
            print("[UI DEBUG] No user is currently logged in.")

        # If no user is logged in, display a message and return
        if user_id is None:
            print("[UI DEBUG] user_id is None, showing login message.")
            no_user_label = CTkLabel(
                self.table_scroll_frame, 
                text="Please log in to view your booking history.",
                font=f.font_h4, 
                text_color=c["text"]
            )
            no_user_label.pack(pady=20)
            return

        bookings = []
        if user_role == 'admin':
            # print("[UI DEBUG] Fetching all bookings for admin")
            bookings = self.db_handler.get_all_bookings()
        else:
            # print(f"[UI DEBUG] Fetching bookings for user_id: {user_id}")
            bookings = self.db_handler.get_bookings_by_user(user_id)

        print(f"[UI DEBUG] Retrieved {len(bookings)} booking(s).")
        # print(f"[UI DEBUG] First few bookings: {bookings[:2] if bookings else 'None'}")

        if not bookings or len(bookings) == 0:
            print("[UI DEBUG] No bookings found, showing no bookings message.")

            no_bookings_label = CTkLabel(
                self.table_scroll_frame, 
                text="No booking history found.",
                font=f.font_h4, 
                text_color=c["text"]
            )
            no_bookings_label.pack(pady=20)
            return
        
        # print("[UI DEBUG] Creating table with bookings...")
        # Create table header
        self.create_table_header()

        # Create table rows
        for i, booking in enumerate(bookings):
            # print(f"[UI DEBUG] Creating row {i} for booking ID: {booking.get('id', 'Unknown')}")
            self.create_table_row(booking, i)
        # print("[UI DEBUG] Table creation completed")

    # Creates the table header with column titles
    def create_table_header(self):
        f = self.app.styles
        c = self.app.styles.colors

        """Create the table header with column titles"""
        header_frame = CTkFrame(self.table_scroll_frame, fg_color=c["table_header"])
        header_frame.grid(row=0, column=0, sticky="ew", padx=5, pady=(10, 5), ipadx=5)

        columns_config = [
            (1, 80),    # Booking ID
            (3, 150),   # Pickup
            (3, 150),   # Destination
            (2, 100),   # Vehicle
            (2, 100),   # Driver
            (1, 80),    # Cost
            (1, 80),    # Status
            (2, 100),   # Date
            (0, 50)     # Action
        ]
        
        for col, (weight, minsize) in enumerate(columns_config):
            header_frame.grid_columnconfigure(col, weight=weight, minsize=minsize)
        headers = [
            "Booking ID", "Pickup", "Destination", "Vehicle",
            "Driver", "Cost", "Status", "Date", "Save"
        ]
        for col, header_text in enumerate(headers):
            label = CTkLabel(
                header_frame, 
                text=header_text, 
                font=f.font_h3, 
                text_color="White"
            )
            label.grid(row=0, column=col, padx=5, pady=10, sticky="ew")
        # print("[UI DEBUG] Header created successfully")

    # Creates a table row for each booking
    def create_table_row(self, booking, row_index):
        """Create a table row for each booking"""

        c = self.app.styles.colors
        f = self.app.styles

        # print(f"[UI DEBUG] Creating row {row_index} with booking data: {booking}")
        row_color = c["table_row_even"] if row_index % 2 == 0 else c["table_row_odd"]
        row_frame = CTkFrame(self.table_scroll_frame, fg_color=row_color, corner_radius=5)
        row_frame.grid(row=row_index + 1, column=0, sticky="ew", padx=5, pady=2, ipadx=5)
        # Configure grid columns for the row_frame (same as header)

        columns_config = [
            (1, 80),    # Booking ID
            (3, 150),   # Pickup
            (3, 150),   # Destination
            (2, 100),   # Vehicle
            (2, 100),   # Driver
            (1, 80),    # Cost
            (1, 80),    # Status
            (2, 100),   # Date
            (0, 50)     # Action
        ]

        for col, (weight, minsize) in enumerate(columns_config):
            row_frame.grid_columnconfigure(col, weight=weight, minsize=minsize)


        booking_id = str(booking.get('id', 'N/A'))
        pickup = self.truncate_text(booking.get('pickup', 'N/A'), 25)
        destination = self.truncate_text(booking.get('destination', 'N/A'), 25)
        vehicle = booking.get('vehicle_type', 'N/A')
        driver = booking.get('driver_name', 'N/A')

        try:
            cost = f"₱{float(booking.get('estimated_cost', 0)):.2f}"
        except (ValueError, TypeError):
            cost = "₱0.00"
            
        status = str(booking.get('status', 'Unknown')).capitalize()
        date = self.format_date(booking.get('created_at'))

        # Create data list
        row_data = [booking_id, pickup, destination, vehicle, driver, cost, status, date]

        # Create labels for each column
        for col, data in enumerate(row_data):
            label = CTkLabel(
                row_frame, 
                text=str(data), 
                font=f.font_h6, 
                text_color="white"
            )
            label.grid(row=0, column=col, padx=5, pady=8, sticky="ew")

        # Save Button (icon only)
        if self.download_icon:
            save_button = CTkButton(
                row_frame,
                text="",
                width=35,
                height=35,
                fg_color="transparent",
                hover_color=c.get("green_hover", "#45a049"),
                image=self.download_icon,
                command=lambda b=booking: self.save_booking_to_json(b)
            )
        else:
            save_button = CTkButton(
                row_frame,
                text="Save",
                width=50,
                height=30,
                fg_color=c.get("primary", "#1f538d"),
                hover_color=c.get("green_hover", "#45a049"),
                command=lambda b=booking: self.save_booking_to_json(b)
            )

        save_button.grid(row=0, column=8, padx=5, pady=8, sticky="w")

        # Add hover effect (optional)
        self.add_hover_effect(row_frame, row_color)

    # Saves booking data to a JSON file
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

    # Truncates text if it's too long
    def truncate_text(self, text, max_length):
        """Truncate text if it's too long"""
        if text and len(text) > max_length:
            return text[:max_length-3] + "..."
        return text if text else "N/A"

    # Formats date string to MM/DD/YYYY
    def format_date(self, date_string):
        if not date_string:
            return "No Date"
        
        date_str = str(date_string)
        
        try:
            # Handle various date formats
            if 'T' in date_str:
                # ISO format with T separator
                date_str = date_str.split('.')[0]  # Remove microseconds if present
                date_obj = datetime.fromisoformat(date_str.replace('T', ' '))
            elif ' ' in date_str and '-' in date_str:
                # Standard datetime format
                date_str = date_str.split('.')[0]  # Remove microseconds if present
                date_obj = datetime.strptime(date_str, "%Y-%m-%d %H:%M:%S")
            elif '-' in date_str and len(date_str) == 10:
                # Date only format
                date_obj = datetime.strptime(date_str, "%Y-%m-%d")
            else:
                # Try ISO format as fallback
                date_obj = datetime.fromisoformat(date_str)
            
            return date_obj.strftime("%m/%d/%Y")
            
        except (ValueError, TypeError) as e:
            print(f"[UI WARNING] Date parsing error for '{date_string}': {e}")
            return str(date_string)[:15] if len(str(date_string)) > 15 else str(date_string)

    # Adds hover effect to the frame and its children
    def add_hover_effect(self, frame, original_color):
        c = self.app.styles.colors
        
        def on_enter(event):
            frame.configure(fg_color=c.get("card_light", "#f0f0f0"))
        def on_leave(event):
            frame.configure(fg_color=original_color)
        frame.bind("<Enter>", on_enter)
        frame.bind("<Leave>", on_leave)
        
        # Apply to child widgets as well
        for child in frame.winfo_children():
            child.bind("<Enter>", on_enter)
            child.bind("<Leave>", on_leave)

    # Refreshes the booking history table
    def refresh_history(self):
        """Refresh the booking history table"""
        self.create_table()

