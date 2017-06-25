"""

scorerecorder.py

writes any score updates etc. to the scorekeeper service

"""

# ------------------------- imports -------------------------
# std lib
import json
import logging
import os
import time

# third party
import requests

# local
from shared import constants as const
from gamemaster.gamechangelistener import GameChangeListener

# ------------------------- constants -------------------------
logbasename = "scorerecorder-{}"
timeformat = "%Y%m%d%H%M"

logdivider = "--------------------------------------------------"


# ------------------------- ScoreRecorder -------------------------
class ScoreRecorder(GameChangeListener):
    """
    this class records all score updates in the scorekeeper service
    """
    def __init__(self):
        
        # this class also logs to file
        logdirpath = const.getlogpath()
        logfilepath = os.path.join(logdirpath, logbasename.format(time.strftime(timeformat)))
        self.filelogger = logging.getLogger('scorerecorder')
        handler = logging.FileHandler(logfilepath)
        handler.setLevel(logging.INFO)
        formatter = logging.Formatter(const.logformat)
        handler.setFormatter(formatter)
        self.filelogger.addHandler(handler)


    def scorekeeperget(self, callstring):
        """
        used for bare gets
        """
        url = "{}/{}".format(const.apiurl, callstring)
        try:
            r = requests.get(url)
        except requests.exceptions.ConnectionError:
            logging.exception("cannot connect to {}".format(url))
            return
        if r.status_code != 200:
            logging.error("error {} when getting {}".format(r.status_code, url))

    def scorekeeperpost(self, callstring, data):
        """
        used for posts
        """
        url = "{}/{}".format(const.apiurl, callstring)
        try:
            r = requests.post(url, json=data)
        except requests.exceptions.ConnectionError:
            logging.exception("cannot connect to {}".format(url))
            return
        if r.status_code != 200:
            logging.error("error {} when posting {}".format(r.status_code, url))

    def scorekeeperput(self, callstring, data):
        """
        used for puts
        """
        url = "{}/{}".format(const.apiurl, callstring)
        try:
            r = requests.put(url, json=data)
        except requests.exceptions.ConnectionError:
            logging.exception("cannot connect to {}".format(url))
            return
        if r.status_code != 200:
            logging.error("error {} when posting {}".format(r.status_code, url))



    # ----- GameChangeListener methods
    # note on logging: there's probably a better way to do it, but
    #   I'm just duplicating the log output for my two logs

    def gamestatechanged(self, state):
        self.scorekeeperpost("state", data={"state": state.value})
        logging.info("game state changed to {}".format(state.value))

        # as a help in spotting game boundaries, add a visual
        #   marker before "preparing" and after "final"
        if state is const.GameState.PREPARING:
            self.filelogger.info(logdivider)
        self.filelogger.info("game state changed to {}".format(state.value))
        if state is const.GameState.FINAL:
            self.filelogger.info(logdivider)

    def gamemetadatachanged(self, metadata):
        self.scorekeeperput("metadata", data=metadata)
        logging.info("game metadata changed to {}".format(metadata))
        self.filelogger.info("game metadata changed to {}".format(metadata))

    def gamescorechanged(self, scoredata):
        self.scorekeeperput("score", data=scoredata)
        logging.info("game score changed to {}".format(scoredata))
        self.filelogger.info("game score changed to {}".format(scoredata))

    def timermaxchanged(self, timermax):
        self.scorekeeperput("timer/max", data={"timermax": timermax})
        logging.info("timer max changed to {}".format(timermax))
        self.filelogger.info("timer max changed to {}".format(timermax))

    def timerstarted(self, starttime):
        self.scorekeeperput("timer/start", data={"starttime": starttime})
        logging.info("timer started at {}".format(starttime))

