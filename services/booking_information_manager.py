from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut, GeocoderServiceError

class BookingInformationManager():
    def __init__(self, pin_location_manager, route_lines_manager):
        self.pin_location_manager = pin_location_manager
        self.route_lines_manager = route_lines_manager
        self.geolocator = Nominatim(user_agent="ride-booking-system")

    def get_coordinates(self):
        pickup_coords = self.pin_location_manager.get_pickup_marker_position()
        dropoff_coords = self.pin_location_manager.get_dropoff_marker_position()

        return {
            "pickup": {"lat": pickup_coords[0], "lon": pickup_coords[1]} if pickup_coords else None,
            "dropoff": {"lat": dropoff_coords[0], "lon": dropoff_coords[1]} if dropoff_coords else None
        }

    def get_address_from_coords(self, lat, lon):
        """
        Reverse geocodes coordinates to an address string.
        """
        try:
            location = self.geolocator.reverse((lat, lon), exactly_one=True, timeout=5)
            if location:
                return location.address
            else:
                return f"Lat: {lat:.4f}, Lon: {lon:.4f}" # Fallback to coordinates if no address found
        except GeocoderTimedOut:
            return "Geocoding timed out"
        except GeocoderServiceError as e:
            return f"Geocoding error: {e}"
        except Exception as e:
            return f"Error getting address: {e}"

