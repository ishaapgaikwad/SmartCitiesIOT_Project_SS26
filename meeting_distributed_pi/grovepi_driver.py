"""
grovepi_driver.py
=================

A lightweight GrovePi driver for modern Raspberry Pi operating systems.

This library communicates directly with the GrovePi firmware over I2C and
provides the most commonly used GrovePi functions:

    - pinMode()
    - digitalRead()
    - digitalWrite()
    - analogRead()
    - analogWrite()
    - dht()

The implementation is based on the GrovePi firmware command protocol and
does not require the legacy GrovePi Python package.

IMPORTANT DHT NOTE:
    DHT sensors may occasionally return invalid values (including NaN in some
    GrovePi environments) if the sensor cannot keep up with the requested
    sample rate or a read fails. DHT sensors should not be read more than
    once every 2 seconds.

---------------------------------------------------------------------------
INSTALLATION
---------------------------------------------------------------------------

Install the required dependency:

    pip install smbus2

Enable I2C on Raspberry Pi:

    sudo raspi-config

        Interface Options
            -> I2C
                -> Enable

---------------------------------------------------------------------------
QUICK START
---------------------------------------------------------------------------

    import grovepi_driver as grovepi

    grovepi.init()

    grovepi.pinMode(3, grovepi.OUTPUT)
    grovepi.digitalWrite(3, grovepi.HIGH)

    grovepi.pinMode(5, grovepi.INPUT)
    value = grovepi.digitalRead(5)

    analog = grovepi.analogRead(0)

    temperature, humidity = grovepi.dht(6, grovepi.DHT11)

---------------------------------------------------------------------------
SUPPORTED FUNCTIONS
---------------------------------------------------------------------------

Digital I/O:
    pinMode()
    digitalRead()
    digitalWrite()

    Can be used for digital sensors, leds, buttons, and actuators like buzzers.

Analog:
    analogRead()
    analogWrite()

    Can be used for analog sensors, potentiometers, and actuators like motors.

Sensors:
    dht()

---------------------------------------------------------------------------
PWM OUTPUT PINS
---------------------------------------------------------------------------

analogWrite() only works on GrovePi PWM-capable ports:

    D3
    D5
    D6

PWM range:

    0   = fully OFF
    255 = fully ON

---------------------------------------------------------------------------
ANALOG INPUT PINS
---------------------------------------------------------------------------

analogRead() works on:

    A0
    A1
    A2

Returned range:

    0 - 1023

---------------------------------------------------------------------------
DHT SENSOR TYPES
---------------------------------------------------------------------------

DHT11:
    grovepi.dht(pin, grovepi.DHT11)

DHT22:
    grovepi.dht(pin, grovepi.DHT22)

Returns:

    (temperature_celsius, humidity_percent)

On failure:

    (None, None)

---------------------------------------------------------------------------
AUTHOR
---------------------------------------------------------------------------

Kunaal Kiran Kumar
"""

import time
import struct
import smbus2

# ============================================================================
# CONSTANTS
# ============================================================================

GROVEPI_ADDR = 0x04

INPUT = 0
OUTPUT = 1

LOW = 0
HIGH = 1

DHT11 = 0
DHT22 = 1

# GrovePi firmware command bytes
_CMD_DIGITAL_READ = 1
_CMD_DIGITAL_WRITE = 2
_CMD_ANALOG_READ = 3
_CMD_ANALOG_WRITE = 4
_CMD_PIN_MODE = 5
_CMD_DHT = 40

# Global bus handle
_bus = None


# ============================================================================
# INITIALIZATION
# ============================================================================

def init(bus_number=1):
    """
    Initialize communication with the GrovePi.

    Parameters
    ----------
    bus_number : int, optional
        Linux I2C bus number. Raspberry Pi uses bus 1 by default.

    Examples
    --------
        import grovepi_driver as grovepi

        grovepi.init()

    Raises
    ------
    OSError
        If the GrovePi or I2C bus cannot be accessed.
    """
    global _bus
    _bus = smbus2.SMBus(bus_number)


def close():
    """
    Close the I2C bus.

    This is optional but recommended before application exit.

    Examples
    --------
        grovepi.close()
    """
    global _bus

    if _bus is not None:
        _bus.close()
        _bus = None


def _check_initialized():
    """Verify that init() has been called."""
    if _bus is None:
        raise RuntimeError(
            "GrovePi driver not initialized. "
            "Call grovepi.init() before using any GrovePi functions."
        )


# ============================================================================
# LOW-LEVEL HELPERS
# ============================================================================

def _send(data):
    """
    Send a 4-byte command frame to GrovePi firmware.
    """
    _check_initialized()
    _bus.write_i2c_block_data(GROVEPI_ADDR, 0, data)


def _receive(length):
    """
    Read bytes returned by GrovePi firmware.
    """
    _check_initialized()
    return _bus.read_i2c_block_data(GROVEPI_ADDR, 1, length)


# ============================================================================
# DIGITAL I/O
# ============================================================================

def pinMode(pin, mode):
    """
    Configure a GrovePi digital pin as INPUT or OUTPUT.

    Parameters
    ----------
    pin : int
        Grove digital port number.

    mode : int or str
        INPUT / OUTPUT or the strings "INPUT" / "OUTPUT".

    Examples
    --------
        grovepi.pinMode(5, grovepi.INPUT)
        grovepi.pinMode(3, grovepi.OUTPUT)
    """
    if isinstance(mode, str):
        mode = OUTPUT if mode.strip().upper() == "OUTPUT" else INPUT

    _send([_CMD_PIN_MODE, pin, mode, 0])


def digitalRead(pin):
    """
    Read a digital input pin.

    Parameters
    ----------
    pin : int
        Grove digital port number.

    Returns
    -------
    int
        LOW (0) or HIGH (1)

    Examples
    --------
        state = grovepi.digitalRead(5)
    """
    _send([_CMD_DIGITAL_READ, pin, 0, 0])
    time.sleep(0.1)

    return _receive(4)[1]


def digitalWrite(pin, value):
    """
    Set a digital output pin HIGH or LOW.

    Parameters
    ----------
    pin : int
        Grove digital port number.

    value : int
        HIGH or LOW

    Examples
    --------
        grovepi.digitalWrite(3, grovepi.HIGH)
        grovepi.digitalWrite(3, grovepi.LOW)
    """
    _send([_CMD_DIGITAL_WRITE, pin, HIGH if value else LOW, 0])


# ============================================================================
# ANALOG FUNCTIONS
# ============================================================================

def analogRead(pin):
    """
    Read an analog input.

    Parameters
    ----------
    pin : int
        Analog channel number (A0, A1, A2 represented as 0, 1, 2).

    Returns
    -------
    int
        Analog value in the range 0-1023.

    Examples
    --------
        value = grovepi.analogRead(0)
    """
    _send([_CMD_ANALOG_READ, pin, 0, 0])

    time.sleep(0.1)

    data = _receive(4)

    return (data[1] << 8) | data[2]


def analogWrite(pin, value):
    """
    Output PWM on a GrovePi PWM-capable pin.

    Supported pins:
        D3, D5, D6

    Parameters
    ----------
    pin : int
        PWM-capable Grove digital port.

    value : int
        PWM value from 0 to 255.

    Returns
    -------
    int
        Clamped PWM value actually transmitted.

    Examples
    --------
        grovepi.analogWrite(3, 128)
    """
    value = max(0, min(255, int(value)))

    _send([_CMD_ANALOG_WRITE, pin, value, 0])

    return value


# ============================================================================
# DHT SENSOR
# ============================================================================

def dht(pin, module_type=DHT11):
    """
    Read temperature and humidity from a Grove DHT sensor.

    Parameters
    ----------
    pin : int
        Grove digital port number.

    module_type : int
        DHT11 or DHT22.

    Returns
    -------
    tuple
        (temperature_celsius, humidity_percent)

    On failure:
        (None, None)

    Examples
    --------
        temperature, humidity = grovepi.dht(6, grovepi.DHT11)
    """
    _send([_CMD_DHT, pin, module_type, 0])

    time.sleep(0.6)

    data = _receive(9)

    if data[0] != _CMD_DHT:
        return None, None

    temperature = struct.unpack('f', bytes(data[1:5]))[0]
    humidity = struct.unpack('f', bytes(data[5:9]))[0]

    if temperature == -1 and humidity == -1:
        return None, None

    return round(temperature, 2), round(humidity, 2)
