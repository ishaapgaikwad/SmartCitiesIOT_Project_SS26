import time
import grovepi_driver as grovepi

BUZZER_PORT = 7


def setup():

    grovepi.pinMode(BUZZER_PORT, grovepi.OUTPUT)

    grovepi.digitalWrite(BUZZER_PORT, grovepi.LOW)


def beep():

    grovepi.digitalWrite(BUZZER_PORT, grovepi.HIGH)

    time.sleep(0.2)

    grovepi.digitalWrite(BUZZER_PORT, grovepi.LOW)
