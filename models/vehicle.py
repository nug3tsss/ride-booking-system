# MultipleFiles/vehicle.py
from abc import ABC, abstractmethod

class Vehicle(ABC):
    def __init__(self, id: int, type: str, model: str, license_plate: str, driver_name: str, driver_contact: str, base_fare: float, per_km_rate: float):
        self._id = id
        self._type = type
        self._model = model
        self._license_plate = license_plate
        self._driver_name = driver_name
        self._driver_contact = driver_contact
        self._base_fare = base_fare
        self._per_km_rate = per_km_rate

    @property
    def id(self) -> int:
        return self._id

    @property
    def type(self) -> str:
        return self._type

    @property
    def model(self) -> str:
        return self._model

    @property
    def license_plate(self) -> str:
        return self._license_plate

    @property
    def driver_name(self) -> str:
        return self._driver_name

    @property
    def driver_contact(self) -> str:
        return self._driver_contact

    @property
    def base_fare(self) -> float:
        return self._base_fare

    @property
    def per_km_rate(self) -> float:
        return self._per_km_rate

    @abstractmethod
    def get_capacity(self) -> int:
        """Returns the passenger capacity of the vehicle."""
        pass

    def calculate_fare(self, distance_km: float) -> float:
        """Calculates the fare based on distance."""
        return self._base_fare + (self._per_km_rate * distance_km)

    def get_details(self) -> dict:
        """Returns a dictionary of common vehicle details."""
        return {
            "id": self._id,
            "type": self._type,
            "model": self._model,
            "license_plate": self._license_plate,
            "driver_name": self._driver_name,
            "driver_contact": self._driver_contact,
            "base_fare": self._base_fare,
            "per_km_rate": self._per_km_rate,
            "capacity": self.get_capacity() # Include capacity from concrete class
        }

class Car(Vehicle):
    def __init__(self, id: int, model: str, license_plate: str, driver_name: str, driver_contact: str, base_fare: float, per_km_rate: float):
        super().__init__(id, "Car", model, license_plate, driver_name, driver_contact, base_fare, per_km_rate)

    def get_capacity(self) -> int:
        return 4 # Example capacity for a car

class Van(Vehicle):
    def __init__(self, id: int, model: str, license_plate: str, driver_name: str, driver_contact: str, base_fare: float, per_km_rate: float):
        super().__init__(id, "Van", model, license_plate, driver_name, driver_contact, base_fare, per_km_rate)

    def get_capacity(self) -> int:
        return 12 # Example capacity for a van

class Motorcycle(Vehicle):
    def __init__(self, id: int, model: str, license_plate: str, driver_name: str, driver_contact: str, base_fare: float, per_km_rate: float):
        super().__init__(id, "Motorcycle", model, license_plate, driver_name, driver_contact, base_fare, per_km_rate)

    def get_capacity(self) -> int:
        return 2 # Example capacity for a motorcycle

