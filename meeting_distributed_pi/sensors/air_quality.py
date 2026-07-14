import grovepi_driver as grovepi

AIR_PORT = 1

GOOD_THRESHOLD = 30


def read_air_quality():
    """
    Returns:
        status (str): "Good" or "Poor"
        value (int): Raw analog reading
    """

    value = grovepi.analogRead(AIR_PORT)

    if value < GOOD_THRESHOLD:
        status = "Good"
    else:
        status = "Poor"

    return status, value
