import subprocess
import config


def run_planner():

    command = [
        "python",
        "-m",
        "pyperplan",
        config.DOMAIN_FILE,
        config.PROBLEM_FILE,
    ]

    subprocess.run(
        command,
        capture_output=True,
        text=True,
    )

    soln_file = config.PROBLEM_FILE + ".soln"

    try:

        with open(soln_file) as f:

            lines = f.readlines()

    except FileNotFoundError:

        return []

    actions = []

    for line in lines:

        line = line.strip()

        if not line:
            continue

        line = line.replace("(", "").replace(")", "")

        actions.append(line)

    return actions