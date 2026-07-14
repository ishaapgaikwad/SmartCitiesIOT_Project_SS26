from context.state import get_state

from sensors.led import light_on, light_off
from sensors.fan import fan_on, fan_off

from actuators.logger import log_event
from actuators.notifier import send_notification


def execute_action(action):

    state = get_state()

    if action == "switch-light-on":

        print("Planner: Turning LIGHT ON")

        light_on()

    elif action == "switch-light-off":

        print("Planner: Turning LIGHT OFF")

        light_off()

    elif action == "switch-fan-on":

        print("Planner: Turning FAN ON")

        fan_on()

    elif action == "switch-fan-off":

        print("Planner: Turning FAN OFF")

        fan_off()

    else:

        print("Planner: No action required")
        return

    # -----------------------------
    # Software actuators
    # -----------------------------

    log_event(action, state)

    send_notification(action, state)
