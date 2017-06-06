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

# ----- scorekeeper
# REST service; this is default for flask
apiurl = "http://127.0.0.1:5000"

# ----- scoeboard
# how often scoreboard should poll the score service, ms: 
scorepollinterval = 3000