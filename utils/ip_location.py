import requests
from customtkinter import *

def get_current_location():
    """Fetches the current geographical location of the user based on their IP address."""
    
    try:
        response = requests.get("https://ipinfo.io/json")
        data = response.json()
        loc = data['loc'].split(',')
        lat = float(loc[0])
        lon = float(loc[1])
        return lat, lon
    except Exception as e:
        print("Error:", e)
        return 14.5995, 120.9842