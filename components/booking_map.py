from tkintermapview import *

class BookingMap(TkinterMapView):
    def __init__(self, *args, width = 300, height = 200, corner_radius = 0, bg_color = None, database_path = None, use_database_only = False, max_zoom = 19, **kwargs):
        super().__init__(*args, width=width, height=height, corner_radius=corner_radius, bg_color=bg_color, database_path=database_path, use_database_only=use_database_only, max_zoom=max_zoom, **kwargs)