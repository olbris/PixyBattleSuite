"""

shared constants


"""

# ------------------------- imports -------------------------
# std lib
import enum


# ----- general data
teamnames = {
    1: "Team 1",
    2: "Team 2",
    3: "Team 3",
    4: "Team 4",
    5: "Team 5",
    6: "Team 6",
}

# ----- general configuration
# logging
logformat = "%(asctime)s %(levelname)s: %(message)s"



# ----- game related
class GameState(enum.Enum):
    UNKNOWN = "unknown"
    TESTING = "testing"
    IDLE = "idle"  # maybe should be "preparing" instead?
    READY = "ready"
    RUNNING = "running"
    PAUSED = "paused"
    FINISHED = "finished"

class TeamColors(enum.Enum):
    RED = "red"
    BLUE = "blue"


# ----- hardware
# how often to request the score from hardware, ms:
hwscorepollinterval = 5000

# how often to look for any output from the hardware, ms:
hwoutputpollinterval = 250


class Commands(enum.Enum):
    RESET = b'RESET\r\n'
    START = b'START\r\n'
    STOP = b'STOP\r\n'
    SCORE = b'SCORE\r\n'
    TEST_RED = b'TEST_RED\r\n'
    TEST_BLUE = b'TEST_BLUE\r\n'
    TEST_GREEN = b'TEST_GREEN\r\n'
    TEST_RED_BLUE = b'TEST_RED_BLUE\r\n'

# ----- scorekeeper
# REST service; this is default for flask
apiurl = "http://127.0.0.1:5000"

# ----- scoreboard
# how often scoreboard should poll the score service, ms: 
scoreservicepollinterval = 3000


