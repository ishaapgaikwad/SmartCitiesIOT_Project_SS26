import time
import grovepi_driver as grovepi

BUZZER_PORT = 7

grovepi.init()

grovepi.pinMode(BUZZER_PORT, grovepi.OUTPUT)

print("=== Grove Buzzer Test ===")

try:

    while True:

        print("BEEP")

        grovepi.digitalWrite(BUZZER_PORT, grovepi.HIGH)

        time.sleep(0.3)

        grovepi.digitalWrite(BUZZER_PORT, grovepi.LOW)

        time.sleep(1)

except KeyboardInterrupt:

    grovepi.digitalWrite(BUZZER_PORT, grovepi.LOW)

    print("\nStopped.")
