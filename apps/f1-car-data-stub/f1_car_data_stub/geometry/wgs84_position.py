from dataclasses import dataclass


@dataclass
class Wgs84Position:
    latitude: float
    longitude: float
    altitude: float = 0
