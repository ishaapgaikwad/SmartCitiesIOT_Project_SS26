import config

import grovepi_driver as grovepi


def read_rotary():

    raw_value = grovepi.analogRead(config.ROTARY_PORT)

    desired_temperature = (
        config.MIN_DESIRED_TEMP
        + (raw_value / 1023.0)
        * (config.MAX_DESIRED_TEMP - config.MIN_DESIRED_TEMP)
    )

    return round(desired_temperature, 1), raw_value
