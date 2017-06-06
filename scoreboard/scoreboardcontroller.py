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


        # bookkeeping
        self.scorechangelisteners = []


    # ----- various setup: listeners, etc.
    def addchangelistener(self, listener):
        self.scorechangelisteners.append(listener)

    def addroot(self, root):
        # add a Tk root so we can use the event loop
        self.root = root

    # ----- data retrieval
    def getgamedata(self):

        # retrieve the game data from the service

        # for testing, use the json; will wrap in a class

        url = "{}/{}".format(const.apiurl, "gamedata")
        r = requests.get(url)
        if r.status_code != 200:
            message = "error: status code {}".format(r.status_code)
        else:
            message = "game state: {}".format(r.json())
        logging.info("{}: {}".format(time.asctime(), message))

        # trigger the update
        self.updategamedata(r.json())

        # reschedule this call; if you like, put in a 
        #   test here so we can turn it off
        self.root.after(const.scorepollinterval, self.getgamedata)


    def startpollingdata(self):
        self.root.after(const.scorepollinterval, self.getgamedata)

    # ----- control stuff
    def setmessage(self, message):
        self.message = message
        self.messagechanged()

    def updategamedata(self, data):
        """
        update all the game data
        """

        # for testing: data = json;
        #   eventually, it'll be a nice class
        # not sure I want to de-granularize it...should
        #   really have separate updates?
        self.gamestate = const.GameState(data["state"])

        self.gamestatechanged()



    # ----- notifications
    def messagechanged(self):
        for l in self.scorechangelisteners:
            l.messagechanged(self.message)

    def gamestatechanged(self):
        for l in self.scorechangelisteners:
            l.gamestatechanged(self.gamestate)






