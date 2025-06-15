# 🚖 Ride Booking System

A ride booking program made with Python using OpenStreetMap, OSRM, CustomTkinter, TkinterMapView, Geopy, and SQLite.

---

## 🔭 Features (WIP)

- Interactive map (select pick-up/drop-off locations with a click of your mouse)
- Route display with OSRM
- Calculate distance (km), time (m), and fare (₱).
- Select from multiple vehicle types.
- Book a ride and manage it (view and cancel booking).

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
Make sure to check **"Add Python to PATH** during installation.

### 2. 📂 Clone the GitHub repository

```bash
git clone https://github.com/nug3tsss/ride-booking-system.git
cd ride-booking-system
```

### 3. 🖥️ Create a Virtual Environment

```bash
python -m venv .venv
```
Activate it:
```bash
venv\Scripts\activate
```

### 4. 📃 Install the Required Libraries

```bash
pip install -r requirements.txt
```

### 5. 🏃 Run the Application

```bash
python main.py
```

### ❗ IF THE TERMINAL COMMANDS DON'T WORK
Try typing:

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

before typing the terminal command; for example:

```bash
py -m pip install -r requirements.txt
```

---

## 📄 Included Tools/Libraries
- CustomTkinter
- TkinterMapView
- Geopy
- Requests
- SQLite3
