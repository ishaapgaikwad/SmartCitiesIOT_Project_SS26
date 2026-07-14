from datetime import datetime

from mqtt.publisher import publish_notification


def send_notification(action, state):

    temperature = state.get("temperature")
    desired_temperature = state.get("desired_temperature")
    air_quality = state.get("air_quality")
    humidity = state.get("humidity")

    too_hot = (
        temperature is not None
        and desired_temperature is not None
        and temperature > desired_temperature
    )

    poor_air = air_quality == "Poor"

    messages = []

    if action == "switch-light-on":

        messages.append("Meeting room occupied.")
        messages.append("Lights switched ON.")

    elif action == "switch-light-off":

        messages.append("Meeting room empty.")
        messages.append("Lights switched OFF.")

    elif action == "switch-fan-on":

        if too_hot and poor_air:

            messages.append(
                "High temperature and poor air quality detected."
            )

            messages.append(
                f"Room temperature: {temperature:.1f}°C"
            )

            messages.append(
                f"Desired temperature: {desired_temperature:.1f}°C"
            )

            messages.append(
                "Fan switched ON for cooling and ventilation."
            )

        elif too_hot:

            messages.append(
                "Room temperature is above the user's desired temperature."
            )

            messages.append(
                f"Room temperature: {temperature:.1f}°C"
            )

            messages.append(
                f"Desired temperature: {desired_temperature:.1f}°C"
            )

            messages.append(
                "Fan switched ON for thermal comfort."
            )

        elif poor_air:

            messages.append(
                "Poor air quality detected."
            )

            messages.append(
                "Fan switched ON for ventilation."
            )

        else:

            messages.append(
                "Fan switched ON."
            )

    elif action == "switch-fan-off":

        messages.append(
            "Room conditions are comfortable."
        )

        messages.append(
            "Air quality is good."
        )

        if temperature is not None:

            messages.append(
                f"Room temperature: {temperature:.1f}°C"
            )

        if desired_temperature is not None:

            messages.append(
                f"Desired temperature: {desired_temperature:.1f}°C"
            )

        messages.append(
            "Fan switched OFF."
        )

    else:

        return

    if humidity is not None and humidity > 65:

        messages.append("")

        messages.append(
            f"Humidity Alert: {humidity:.1f}%"
        )

        messages.append(
            "High humidity detected."
        )

        messages.append(
            "Consider ventilating the meeting room."
        )

    message = "\n".join(messages)

    # Terminal notification

    print()
    print("===================================")
    print("         NOTIFICATION")
    print("===================================")

    print(message)

    print("===================================")
    print()

    # MQTT notification for dashboard

    notification = {

        "action": action,

        "message": message,

        "timestamp": datetime.now().strftime(
            "%Y-%m-%d %H:%M:%S"
        )

    }

    publish_notification(notification)
