<picture>
  <source srcset="assets/icons/logo-dark--transparent.png" media="(prefers-color-scheme: dark)">
  <img src="assets/icons/logo-light--transparent.png" alt="Gethub logo light">
</picture>

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
