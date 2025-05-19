from dataclasses import dataclass


@dataclass
class Wgs84Position:
    """
    Represents a position in WGS84 geodetic coordinates.

    Attributes:
        latitude (float): Latitude in decimal degrees.
        longitude (float): Longitude in decimal degrees.
        altitude (float): Altitude in meters above sea level (default is 0).
    """
    latitude: float
    longitude: float
    altitude: float = 0
