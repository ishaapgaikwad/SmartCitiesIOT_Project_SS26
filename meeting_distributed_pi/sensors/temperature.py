import math
import time

import grovepi_driver as grovepi

TEMP_PORT = 5

_last_temp = None
_last_humidity = None
_last_read = 0


def read_temperature():

    global _last_temp
    global _last_humidity
    global _last_read

    # DHT11 should not be read more often than every 2 seconds
    if time.time() - _last_read < 2:
        return _last_temp, _last_humidity

    _last_read = time.time()

    temp, humidity = grovepi.dht(
        TEMP_PORT,
        grovepi.DHT11
    )

    if (
        temp is None
        or humidity is None
        or math.isnan(temp)
        or math.isnan(humidity)
    ):
        return _last_temp, _last_humidity

    _last_temp = temp
    _last_humidity = humidity

    return temp, humidity
