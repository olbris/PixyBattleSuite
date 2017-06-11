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

# local
from shared import constants as const


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

        # game data
        self.state = const.GameState.IDLE


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

    # ----- notification routines
    def statechanged(self):
        for listener in self.gamechangelisteners:
            listener.gamestatechanged(self.state)


