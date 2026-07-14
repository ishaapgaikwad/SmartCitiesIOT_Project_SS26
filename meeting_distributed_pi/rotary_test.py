#!/usr/bin/env python3

import time
import grovepi_driver as grovepi

ROTARY_PORT = 0  # A0


def main():
    grovepi.init()

    print("Rotary sensor test started.")
    print("Rotate the knob. Press Ctrl+C to stop.")

    try:
        while True:
            raw_value = grovepi.analogRead(ROTARY_PORT)

            # Map raw range 0-1023 to desired temperature 18-28 °C
            desired_temperature = 18 + (raw_value / 1023.0) * 10

            print(
                f"Raw value: {raw_value:4d} | "
                f"Desired temperature: {desired_temperature:.1f} °C"
            )

            time.sleep(0.5)

    except KeyboardInterrupt:
        print("\nStopped.")

    finally:
        grovepi.close()


if __name__ == "__main__":
    main()
