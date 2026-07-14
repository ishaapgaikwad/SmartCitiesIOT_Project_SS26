import grovepi_driver as grovepi
import config

_configured = False


def setup():
    global _configured

    if not _configured:
        grovepi.pinMode(config.PIR_PORT, grovepi.INPUT)
        _configured = True


def motion_detected():
    setup()
    return grovepi.digitalRead(config.PIR_PORT) == 1
