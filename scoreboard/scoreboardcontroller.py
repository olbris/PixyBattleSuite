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
        
        # UI message
        self.message = ""

        # all the game data
        self.gamedata = const.getdefaultdata()

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
        url = "{}/{}".format(const.apiurl, "data")
        r = requests.get(url)
        if r.status_code != 200:
            logging.error("error: status code {}".format(r.status_code))
            return

        # check out which updates we need to do
        newdata = r.json()

        metadataupdated = newdata["metadatatime"] > self.gamedata["metadatatime"]
        scoreupdated = newdata["scoretime"] > self.gamedata["scoretime"]
        stateupdated = newdata["statetime"] > self.gamedata["statetime"]
        if any([metadataupdated, scoreupdated, stateupdated]):
            self.gamedata.update(newdata)

            if metadataupdated:
                self.gamemetadatachanged()

            if scoreupdated:
                self.gamescorechanged()

            if stateupdated:
                self.gamestatechanged()



        # reschedule this call; if you like, put in a 
        #   test here so we can turn it off
        self.root.after(const.scoreservicepollinterval, self.getgamedata)


    def startpollingdata(self):
        self.root.after(const.scoreservicepollinterval, self.getgamedata)

    # ----- control stuff
    def setmessage(self, message):
        self.message = message
        self.messagechanged()


    # ----- notifications
    def messagechanged(self):
        for l in self.scorechangelisteners:
            l.messagechanged(self.message)

    def gamestatechanged(self):
        for l in self.scorechangelisteners:
            l.gamestatechanged(self.gamedata)

    def gamemetadatachanged(self):
        for l in self.scorechangelisteners: 
            l.gamemetadatachanged(self.gamedata)

    def gamescorechanged(self):
        for l in self.scorechangelisteners: 
            l.gamescorechanged(self.gamedata)





