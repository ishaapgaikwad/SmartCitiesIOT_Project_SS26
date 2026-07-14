import json
import time

import config

from sensors.pir import motion_detected
from sensors.led import is_light_on

# How long (seconds) without motion before room is considered empty
OCCUPANCY_TIMEOUT = 5

_last_motion_time = 0
_occupied = False


def update_context():
    """
    Updates the occupancy state using PIR sensor.
    A single motion detection marks the room occupied.
    The room becomes unoccupied only after OCCUPANCY_TIMEOUT seconds.
    """

    global _last_motion_time
    global _occupied

    if motion_detected():
        _last_motion_time = time.time()
        _occupied = True

    else:
        if time.time() - _last_motion_time > OCCUPANCY_TIMEOUT:
            _occupied = False

    state = {

        "occupied": _occupied,

        "light": is_light_on(),

        "temperature": None,

        "humidity": None

    }

    with open(config.STATE_FILE, "w") as f:
        json.dump(state, f, indent=4)

    return state


def get_state():

    with open(config.STATE_FILE) as f:
        return json.load(f)
