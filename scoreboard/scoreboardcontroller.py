"""

scoreboardcontroller.py

model and controller for the scoreboard

"""

# ------------------------- imports -------------------------
# std lib
import logging
import time

# third party
import requests

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

        self.gamestate = const.GameState.UNKNOWN

        self.gamemetadata = {
            "red": 0,
            "blue": 0,
        }


        # bookkeeping
        self.scorechangelisteners = []


    # ----- various setup: listeners, etc.
    def addchangelistener(self, listener):
        self.scorechangelisteners.append(listener)

    def addroot(self, root):
        # add a Tk root so we can use the event loop
        self.root = root

    # ----- data retrieval
    def getgamemetadata(self):

        # retrieve the game data from the service

        # for testing, use the json; will wrap in a class

        url = "{}/{}".format(const.apiurl, "gamemetadata")
        r = requests.get(url)
        if r.status_code != 200:
            message = "error: status code {}".format(r.status_code)
        else:
            message = "game state: {}".format(r.json())
        logging.info("{}: {}".format(time.asctime(), message))

        # trigger the update
        self.updategamemetadata(r.json())

        # reschedule this call; if you like, put in a 
        #   test here so we can turn it off
        self.root.after(const.scoreservicepollinterval, self.getgamemetadata)


    def startpollingdata(self):
        self.root.after(const.scoreservicepollinterval, self.getgamemetadata)

    # ----- control stuff
    def setmessage(self, message):
        self.message = message
        self.messagechanged()

    def updategamemetadata(self, data):
        """
        update game metadata
        """

        # testing; should update, should check time stamp before notifying
        self.gamemetadata = data
        self.gamemetadatachanged()

        # this is going to be changed
        # self.gamestate = const.GameState(data["state"])
        # self.gamestatechanged()



    # ----- notifications
    def messagechanged(self):
        for l in self.scorechangelisteners:
            l.messagechanged(self.message)

    def gamestatechanged(self):
        for l in self.scorechangelisteners:
            l.gamestatechanged(self.gamestate)

    def gamemetadatachanged(self):
        for l in self.scorechangelisteners: 
            l.gamemetadatachanged(self.gamemetadata)





