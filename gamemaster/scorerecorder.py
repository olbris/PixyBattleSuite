"""

scorerecorder.py

writes any score updates etc. to the scorekeeper service

"""

# ------------------------- imports -------------------------
# std lib
import json
import logging

# third party
import requests

# local
from shared import constants as const
from gamemaster.gamechangelistener import GameChangeListener


# ------------------------- ScoreRecorder -------------------------
class ScoreRecorder(GameChangeListener):
    """
    this class records all score updates in the scorekeeper service
    """
    def __init__(self):
        pass
        

    def scorekeeperget(self, callstring):
        """
        used for bare gets
        """
        url = "{}/{}".format(const.apiurl, callstring)
        try:
            r = requests.get(url)
        except requests.exceptions.ConnectionError:
            logging.exception("cannot connect to {}".format(url))
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
        if r.status_code != 200:
            logging.error("error {} when posting {}".format(r.status_code, url))



    # ----- GameChangeListener methods
    def gamestatechanged(self, state):
        self.scorekeeperpost("state", data={"state": state.value})
        logging.info("game state changed to {}".format(state.value))




