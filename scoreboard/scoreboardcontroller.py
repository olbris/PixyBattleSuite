"""

scoreboardcontroller.py

model and controller for the scoreboard

"""

# ------------------------- imports -------------------------
# std lib
import logging

# local
from shared import constants as const


# ------------------------- ScoreboardController -------------------------
class ScoreboardController:
    """
    controller for scoreboard
    """

    def __init__(self):
        

        # state
        self.message = ""


        # bookkeeping
        self.scorechangelisteners = []


    # ----- various setup: listeners, etc.
    def addchangelistener(self, listener):
        self.scorechangelisteners.append(listener)

    # ----- control stuff
    def setmessage(self, message):
        self.message = message
        self.messagechanged()



    # ----- notifications
    def messagechanged(self):
        for l in self. scorechangelisteners:
            l.messagechanged(self.message)