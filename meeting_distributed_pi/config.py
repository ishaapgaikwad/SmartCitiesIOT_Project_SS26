# Grove Digital Ports
PIR_PORT = 4
LED_PORT = 3
FAN_PORT = 6
TEMP_PORT = 5

# Grove Analog Ports
ROTARY_PORT = 0  # A0

# Sensor Timing
PIR_READ_DELAY = 1

# Temperature threshold
TEMP_THRESHOLD = 25.0

# Rotary sensor desired temperature range
MIN_DESIRED_TEMP = 18.0
MAX_DESIRED_TEMP = 28.0

# Data Files
STATE_FILE = "data/occupancy.json"
PLAN_FILE = "data/plan.txt"
PROBLEM_FILE = "data/problem.pddl"

# Log File
LOG_DIR = "logs"
LOG_FILE = "logs/events.csv"

# MQTT
MQTT_BROKER = "192.168.50.1"

MQTT_STATE_TOPIC = "meetingroom/state"
MQTT_ACTION_TOPIC = "meetingroom/action"

DOMAIN_FILE = "planner/domain.pddl"

MQTT_NOTIFICATION_TOPIC = "meetingroom/notification"
