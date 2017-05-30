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
