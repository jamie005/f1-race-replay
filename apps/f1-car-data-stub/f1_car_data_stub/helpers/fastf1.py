import logging

import fastf1
from fastf1.core import Telemetry


def get_car_telemetry(track: str, year: int, session_type: str, driver: str) -> Telemetry:
    logger = logging.getLogger(__package__)
    fastf1.set_log_level(logging.CRITICAL) # Set to CRITICAL to avoid FastF1 logs

    logger.debug(f"Loading {track} {year} {session_type} session...")
    session = fastf1.get_session(year, track, session_type)
    session.load(weather=False, messages=False)
    logger.debug(f"{session} loaded successfully!")

    logger.debug(f"Loading {driver} laps...")
    driver_laps = session.laps.pick_drivers(driver)
    logger.debug(f"Laps loaded!")
    
    return driver_laps.get_telemetry()
