<p align="center">
  <picture>
    <source srcset="assets/icons/logo-dark--transparent.png" media="(prefers-color-scheme: dark)">
    <img src="assets/icons/logo-light--transparent.png" alt="My Image" width="200">
  </picture>
</p>

<h1 align="center">Gethub</h1>
<p align="center">
  A ride-hailing program developed by 1st year Computer Engineering students of PUP College of Engineering.
</p>

---

## 🔭 Features

- Interactive booking experience
  - Responsive map with manual marker placements and display autofocus
  - Route navigation display
  - Location address entry with autosuggestion feature
  - Vehicle type selection
  - Import past booking information
  - Clear booking entries
- Route and fare calculation
  - Distance in km
  - Estimate Time of Arrival in mins
  - Calculated cost in ₱
- Booking history and management
  - Downloadable bookings as .json
- Account creation and customization

---

## 🔭 File Structure

This app follows a modular, component-based file structure designed for clarity, scalability, and ease of maintenance. 

```bash
.
├── _documentation/                  # Final project report and presentation
│   ├── OOP_CPE-1-7_Group-4_Project-Final-Report.pdf
│   └── OOP_CPE-1-7_Group-4_Project-Presentation.pdf
│
├── assets/                          # All static images/icons used in the app
│   ├── banners/                     # Banner/header images for each main page
│   ├── icons/                       # UI icons for light/dark mode
│   ├── members_profile/             # Member pictures used in about us page
│   └── user/                        # User-uploaded profile pictures
│
├── components/                      # Reusable UI elements across pages
│   ├── navbar.py                    # Top navigation bar with theme/login buttons
│   ├── sidebar.py                   # Side navigation menu with route buttons
│   ├── booking_form.py              # Form UI to create new ride bookings
│   ├── booking_summary_form.py      # Displays booking summary + confirm button
│   ├── booking_map.py               # Shows map route preview (via OSRM)
│   ├── contact_form.py              # Contact Us form logic with validation
│   └── auth_popup.py                # Reusable login/register modals
│
├── config/                          # App settings and centralized style configs
│   ├── styles.py                    # Fonts, theme modes, colors, hover effects
│   └── settings_manager.py          # Manages saving/loading UI settings
│
├── database/                        # SQLite database and related logic
│   ├── db_handler.py                # Connects to SQLite DB and runs queries
│   ├── query.sql                    # Raw SQL schema or seed data (optional)
│   └── rides.db                     # SQLite database file storing all records
│
├── models/                          # Data classes representing core app entities
│   ├── message.py                   # Message model used in Contact Us page
│   └── vehicle.py                   # Vehicle data model for bookings
│
├── services/                        # Logic connecting UI and data models
│   ├── booking_information_manager.py  # Handles temporary booking data across pages
│   └── map_manager.py               # Manages map routes, geocoding, etc.
│
├── tests/                           # Sample JSON test data for booking scenarios
│   ├── test_booking_0.json
│   └── test_booking_1.json
│
├── utils/                           # Small helper modules
│   ├── ip_location.py               # Gets user location via IP (for maps)
│   ├── pycache_cleaner.py           # Removes __pycache__ folders and .pyc files
│   └── session_manager.py           # Saves/loads session (logged-in user)
│
├── views/                           # Full-page layouts and routing logic
│   ├── about.py                     # Static About Us page
│   ├── contact.py                   # Static Contact Us page
│   ├── dashboard.py                 # Logged-in home page with metrics/cards
│   ├── login_page.py                # Login screen UI
│   ├── register_page.py             # Registration form
│   ├── profile_page.py              # User profile editor with image cropping
│   ├── history_page.py              # Ride history page (past bookings)
│   └── settings.py                  # App settings page (theme, font, etc.)
│
├── .gitattributes                   # Git settings for line endings or diffing
├── .gitignore                       # Untracked files by Git
├── app.py                           # Main App GUI class or layout controller
├── main.py                          # Entry point: setup loading, then start app
├── requirements.txt                 # List of all required Python packages
├── README.md                        # Project overview, instructions, credits
└── LICENSE                          # Open-source license information
```

---

## 📚 Libraries and APIs Used

- CustomTkinter -> GUI elements
- TkinterMapView -> Map GUI integration
- OpenStreetMap -> Map GUI integration
- Pillow -> Image integration and customization
- Open Source Routing Machine -> Routing calculations
- Geopy -> Geolocation
- SQLite -> Database handling
- Geoapify -> Location addresses

---

## 📦 Requirements

- Python 3.9 or newer
- Git

---

## 🧰 Setup Instructions

### 1. ✔️ Check if Python is installed and on the required version

Open Command Prompt/Terminal and run:

```bash
py --version
```
or
```bash
python --version
```
or
```bash
python3 --version
```

If python is **not installed**, download it from:  
https://www.python.org/downloads/  
Make sure to check **"Add Python to PATH"** during installation.  

### 2. 📂 Clone the GitHub repository

```bash
git clone https://github.com/nug3tsss/ride-booking-system.git
cd ride-booking-system
```

### 3. 🖥️ Create a Virtual Environment

```bash
py -m venv .venv
```
or
```bash
python -m venv .venv
```
or
```bash
python3 -m venv .venv
```

Activate it:
```bash
.venv\Scripts\activate
```

### 4. 📃 Install the Required Libraries

```bash
pip install -r requirements.txt
```

### 5. 🏃 Run the Application

```bash
python main.py
```

---

### ❗ IF THE TERMINAL COMMANDS DON'T WORK
Add the possible prefix/es:

```bash
py -m
```
or
```bash
python -m
```
or
```bash
python3 -m
```

then type the terminal command.  
For example:

```bash
py -m pip install -r requirements.txt
```
