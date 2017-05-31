"""

shared constants


"""

# ------------------------- imports -------------------------
# std lib
import enum


# ------------------------- constants -------------------------

class GameState(enum.Enum):
    UNKNOWN = "unknown"
    IDLE = "idle"
    READY = "ready"
    RUNNING = "running"
    PAUSED = "paused"
    FINISHED = "finished"

# this is default for flask
apiurl = "http://127.0.0.1:5000"

