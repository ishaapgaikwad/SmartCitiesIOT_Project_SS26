import grovepi_driver as grovepi
import config

_fan_state = False


def setup():

    grovepi.pinMode(config.FAN_PORT, grovepi.OUTPUT)

    grovepi.digitalWrite(config.FAN_PORT, grovepi.LOW)


def fan_on():

    global _fan_state

    grovepi.digitalWrite(config.FAN_PORT, grovepi.HIGH)

    _fan_state = True


def fan_off():

    global _fan_state

    grovepi.digitalWrite(config.FAN_PORT, grovepi.LOW)

    _fan_state = False


def is_fan_on():

    return _fan_state
