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
        
        # UI stuff
        # primary is intended to be public view, secondary is
        #   the view for the organizers
        self.views = {}

        # view properties
        self.viewvisibility = {}


        # message to display on views
        self.message = ""


        # all the game data
        self.gamedata = const.getdefaultdata()

        # timer data
        self.timermax = const.defaultgamelength
        self.timermaxtime = time.time()
        self.starttime = time.time()
        self.starttimetime = time.time()
        self.timerrunning = False

        # bookkeeping
        self.scorechangelisteners = []


    # ----- various setup: listeners, etc.
    def addview(self, view, viewtype):
        self.views[viewtype] = view
        self.viewvisibility[viewtype] = True
        self.addchangelistener(view)

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

        # do timer max stuff here, too
        url = "{}/{}".format(const.apiurl, "timer/max")
        r = requests.get(url)
        if r.status_code != 200:
            logging.error("error: status code {}".format(r.status_code))
            return
        timerdata = r.json()
        if timerdata["timermaxtime"] > self.timermaxtime:
            self.timermax = timerdata["timermax"]
            self.timermaxtime = timerdata["timermaxtime"]
            self.timervaluechanged(self.timermax)

        # reschedule this call; if you like, put in a 
        #   test here so we can turn it off
        self.root.after(const.scoreservicepollinterval, self.getgamedata)


    def startpollingdata(self):
        self.root.after(const.scoreservicepollinterval, self.getgamedata)

    def timerloop(self):
        
        if self.timerrunning:
            # if running: increment and update
            remaining = self.starttime + self.timermax - time.time()
            self.timervaluechanged(remaining)
            if remaining <= const.timeepsilon:
                self.timerrunning = False

        else:
            # if not running: poll service to see if we should start running
            url = "{}/{}".format(const.apiurl, "timer/start")
            r = requests.get(url)
            if r.status_code != 200:
                logging.error("error: status code {}".format(r.status_code))
                return
            timerdata = r.json()
            if timerdata["starttimetime"] > self.starttimetime:
                self.starttime = timerdata["starttime"]
                self.starttimetime = timerdata["starttimetime"]
                self.timerrunning = True
                self.timervaluechanged(self.timermax)

        self.root.after(const.timerservicepollinterval, self.timerloop)

    def startpollingtimer(self):
        self.root.after(const.timerservicepollinterval, self.timerloop)

    # ----- control stuff
    def setmessage(self, message):
        self.message = message
        self.messagechanged()

    def toggleviewvisibility(self, viewtype):
        if self.viewvisibility[viewtype]:
            self.views[viewtype].withdraw()
            self.viewvisibility[viewtype] = False
        else:
            self.views[viewtype].deiconify()
            self.viewvisibility[viewtype] = True


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

    def timervaluechanged(self, timervalue):
        for l in self.scorechangelisteners: 
            l.timervaluechanged(timervalue)        



