import grovepi_driver as grovepi
import config

_configured = False
_light_state = False


def setup():
    global _configured

    if not _configured:
        grovepi.pinMode(config.LED_PORT, grovepi.OUTPUT)
        _configured = True


def light_on():
    global _light_state

    setup()

    grovepi.digitalWrite(config.LED_PORT, 1)

    _light_state = True


def light_off():
    global _light_state

    setup()

    grovepi.digitalWrite(config.LED_PORT, 0)

    _light_state = False


def is_light_on():
    return _light_state
