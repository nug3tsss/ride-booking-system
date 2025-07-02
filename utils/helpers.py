import requests
from customtkinter import *

def create_nav_button(self, text, page, column):
    CTkButton(self, text=text, font=self.styles.nav_font,
              command=lambda: self.app.show_page(page),
              fg_color="transparent", text_color="white",
              hover_color=self.styles.hover_color, corner_radius=0
              ).grid(row=0, column=column, padx=5, sticky="nsew")
    
def get_current_location():
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