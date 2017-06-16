"""

gamecontroller.py

technically it's the model and controller for the game software

- keeps game state
- when hardware changes come in, it updates game state and notifies listeners
- when UI input come in, it updates game state and notifies listeners

"""

# ------------------------- imports -------------------------
# std lib
import logging
import time

# local
from shared import constants as const

# ------------------------- utility functions -------------------------
def add3tuple(t1, t2):
    return t1[0] + t2[0], t1[1] + t2[1], t1[2] + t2[2]

# ------------------------- GameController -------------------------
class GameController:
    """
    this class is the model and controller for the game software
    """
    def __init__(self):
        
        # internal stuff
        self.gamechangelisteners = []
        self.hardwarechangelisteners = []
        self.arenacontroller = None

        # for controlling score report timing; last time score received,
        #   and last time score sent out
        # times are in seconds since the epoch
        self.lastscorerecorded = time.time()
        self.lasthitsreported = time.time()

        # game metadata
        self.gamemetadata = {}

        # game running data
        self.state = const.GameState.IDLE
        self.targethits = {}


    # ----- various setup: listeners, etc.
    def addchangelistener(self, listener):
        self.gamechangelisteners.append(listener)

    def addhardwarechangelistener(self, listener):
        self.hardwarechangelisteners.append(listener)

    def connectarenacontroller(self, arenacontroller):
        self.arenacontroller = arenacontroller


    # ----- UI and game control stuff
    # called by (eg) view either as a results of user input,
    #   or to get state independent of changes
    def setstate(self, state):
        """
        change the game state to the input value
        """

        if state is not self.state:
            self.state = state
            logging.info("state changed to {}".format(self.state))

            # notify listeners
            self.statechanged()

    def setmetadata(self, metadata):
        self.metadata = metadata
        self.metadatachanged()

    # ----- hardware controls stuff
    def discovertargets(self):
        self.arenacontroller.requestdiscover()

    def targetcommand(self, targetlist, command):
        self.arenacontroller.requesttargetcommand(targetlist, command)


    def closealltargets(self):
        self.arenacontroller.closealltargets()

    # ----- called by arena controller
    def targetsdiscovered(self, targetlist):
        for listener in self.hardwarechangelisteners:
            listener.targetsdiscovered(targetlist)

        # is this the right place for this?
        if len(targetlist) > 0:
            self.arenacontroller.startscorepolling()
            self.arenacontroller.startoutputpolling()

    def reporthits(self, hits):
        """
        input: hits tuple: (devicepath, TeamColors.RED, #neutral, #opposing, #final)
        """

        # testing:
        # logging.info("score received: {}".format(score))


        # store hits, covert to score right before reporting



        # store most recent hits line for each target,  
        #   keyed on path and team color; then sum up and notify
        self.targethits[hits[:2]] = hits[2:]
        now = time.time()

        # not 100% sure this is a good idea...I don't want to delay 
        #   scores, but I don't want to flood the system, either
        if now - self.lasthitsreported > 0.25:
            redtotal = (0, 0, 0)
            bluetotal = (0, 0, 0)
            for devicepath, color in self.targethits.keys():
                if color is const.TeamColors.RED:
                    redtotal = add3tuple(redtotal, self.targethits[devicepath, color])
                elif color is const.TeamColors.BLUE:
                    bluetotal = add3tuple(bluetotal, self.targethits[devicepath, color])

            # notify:
            # (still to come)
            # need to mutliply out score from hits

            # test:
            logging.info("hits updated: red = {}, blue = {}".format(redtotal, bluetotal))

            self.lasthitsreported = time.time()



    # ----- notification routines
    def statechanged(self):
        for listener in self.gamechangelisteners:
            listener.gamestatechanged(self.state)

    def metadatachanged(self):
        for listener in self.gamechangelisteners:
            listener.gamemetadatachanged(self.metadata)

