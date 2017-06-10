"""

shared constants


"""

# ------------------------- imports -------------------------
# std lib
import enum


# ----- general configuration
# logging
logformat = "%(asctime)s %(levelname)s: %(message)s"



# ----- game related
class GameState(enum.Enum):
    UNKNOWN = "unknown"
    IDLE = "idle"
    READY = "ready"
    RUNNING = "running"
    PAUSED = "paused"
    FINISHED = "finished"

class TeamColors(enum.Enum):
    RED = "red"
    BLUE = "blue"


# ----- hardware
# how often to poll the hardware, ms:
hwpollinterval = 100

# these are the simple commands with no output
class Commands(enum.Enum):
    RESET = b'RESET\r\n'
    START = b'START\r\n'
    STOP = b'STOP\r\n'
    TEST_RED = b'TEST_RED\r\n'
    TEST_BLUE = b'TEST_BLUE\r\n'
    TEST_GREEN = b'TEST_GREEN\r\n'
    TEST_RED_BLUE = b'TEST_RED_BLUE\r\n'

# ----- scorekeeper
# REST service; this is default for flask
apiurl = "http://127.0.0.1:5000"

# ----- scoeboard
# how often scoreboard should poll the score service, ms: 
scorepollinterval = 3000