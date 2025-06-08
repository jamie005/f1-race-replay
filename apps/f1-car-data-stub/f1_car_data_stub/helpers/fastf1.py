import logging

import fastf1
from fastf1.core import Telemetry


def get_car_telemetry(track: str, year: int, session_type: str, driver: str) -> Telemetry:
    """
    Loads telemetry data for a specific driver from a FastF1 session.

    Args:
        track (str): The name of the track (e.g., "Monza").
        year (int): The year of the session (e.g., 2021).
        session_type (str): The type of session (e.g., "Race", "Qualifying").
        driver (str): The driver code (e.g., "VER" for Verstappen).

    Returns:
        Telemetry: The telemetry data for the specified driver and session.
    """
    logger = logging.getLogger(__package__)
    fastf1.set_log_level(logging.CRITICAL)  # Set to CRITICAL to avoid FastF1 logs

    logger.debug(f"Loading {track} {year} {session_type} session...")
    session = fastf1.get_session(year, track, session_type)
    session.load(weather=False, messages=False)
    logger.debug(f"{session} loaded successfully!")

    logger.debug(f"Loading {driver} laps...")
    driver_laps = session.laps.pick_drivers(driver)
    logger.debug("Laps loaded!")

    return driver_laps.get_pos_data()
