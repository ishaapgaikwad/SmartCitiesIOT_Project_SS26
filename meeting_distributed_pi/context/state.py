import json
import time

import config

from sensors.pir import motion_detected
from sensors.led import is_light_on
from sensors.fan import is_fan_on
from sensors.temperature import read_temperature
from sensors.air_quality import read_air_quality
from sensors.rotary import read_rotary


OCCUPANCY_TIMEOUT = 5

_last_motion_time = 0
_occupied = False
_last_pir = False


def update_context():

    global _last_motion_time
    global _occupied
    global _last_pir

    pir = motion_detected()

    print(f"PIR={pir}")

    # Detect new motion
    if pir and not _last_pir:
        _last_motion_time = time.time()
        _occupied = True

    # Room becomes empty after timeout
    elif time.time() - _last_motion_time > OCCUPANCY_TIMEOUT:
        _occupied = False

    _last_pir = pir

    # Read temperature and humidity
    temperature, humidity = read_temperature()

    # Read air quality
    air_quality, air_value = read_air_quality()

    # Read rotary sensor
    desired_temperature, rotary_value = read_rotary()

    state = {

        "occupied": _occupied,

        "light": is_light_on(),

        "fan": is_fan_on(),

        "temperature": temperature,

        "humidity": humidity,

        "air_quality": air_quality,

        "air_quality_value": air_value,

        "desired_temperature": desired_temperature,

        "rotary_value": rotary_value

    }

    with open(config.STATE_FILE, "w") as f:
        json.dump(state, f, indent=4)

    return state


def get_state():

    with open(config.STATE_FILE) as f:
        return json.load(f)
