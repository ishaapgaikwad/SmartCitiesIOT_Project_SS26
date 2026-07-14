from sensors.led import light_on, light_off


def execute_plan(action):

    if action == "switch-light-on":
        print("Planner: Turning light ON")
        light_on()

    elif action == "switch-light-off":
        print("Planner: Turning light OFF")
        light_off()

    else:
        print("Planner: No action required")
