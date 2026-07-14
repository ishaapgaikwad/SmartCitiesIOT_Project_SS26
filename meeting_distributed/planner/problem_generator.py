import json
import config


def generate_problem():

    with open(config.STATE_FILE) as f:
        state = json.load(f)

    init = []
    goal = []

    # --------------------------
    # Occupancy
    # --------------------------

    if state["occupied"]:
        init.append("(occupied)")
        goal.append("(light-on)")
    else:
        init.append("(room-empty)")
        goal.append("(light-off)")

    # --------------------------
    # Light
    # --------------------------

    if state["light"]:
        init.append("(light-on)")
    else:
        init.append("(light-off)")

    # --------------------------
    # Temperature + Rotary Preference
    # --------------------------

    temperature = state["temperature"]
    desired_temperature = state["desired_temperature"]

    too_hot = (
        temperature is not None
        and desired_temperature is not None
        and temperature > desired_temperature
    )

    if too_hot:
        init.append("(too-hot)")
    else:
        init.append("(comfortable)")

    # --------------------------
    # Air Quality
    # --------------------------

    poor_air = (
        state["air_quality"] == "Poor"
    )

    if poor_air:
        init.append("(air-quality-poor)")
    else:
        init.append("(air-quality-good)")

    # --------------------------
    # Fan
    # --------------------------

    if state["fan"]:
        init.append("(fan-on)")
    else:
        init.append("(fan-off)")

    # --------------------------
    # Goal
    # --------------------------

    if too_hot or poor_air:
        goal.append("(fan-on)")
    else:
        goal.append("(fan-off)")

    problem = f"""
(define (problem meeting-room-problem)

(:domain meeting-room)

(:init
    {' '.join(init)}
)

(:goal
    (and
        {' '.join(goal)}
    )
)

)
"""

    with open(config.PROBLEM_FILE, "w") as f:
        f.write(problem)

    print(
        f"Problem generated. "
        f"Temperature={temperature}, "
        f"Desired={desired_temperature}, "
        f"Too hot={too_hot}"
    )