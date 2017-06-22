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
        self.state = const.GameState.UNKNOWN

        # timer
        self.timermax = const.defaultgamelength
        self.timerstart = 0


        self.resetstoredscores()


    # ----- various setup: listeners, etc.
    def addchangelistener(self, listener):
        self.gamechangelisteners.append(listener)

    def addhardwarechangelistener(self, listener):
        self.hardwarechangelisteners.append(listener)

    def connectarenacontroller(self, arenacontroller):
        self.arenacontroller = arenacontroller

    def addroot(self, root):
        # tk root, so we can use event loop
        self.root = root

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

    def setrobothits(self, redhits, bluehits):
        self.robothits[const.TeamColors.RED] = redhits
        self.robothits[const.TeamColors.BLUE] = bluehits

    def resetscores(self):
        self.resetstoredscores()
        self.resetalltargets()

    def resetstoredscores(self):
        # holds hit data from targets, per device and team color
        # also holds summed under device = "total", which we seed
        self.targethits = {
            ("total", const.TeamColors.RED): (0, 0, 0),
            ("total", const.TeamColors.BLUE): (0, 0, 0),
        }
        self.robothits = {
            const.TeamColors.RED: 0,
            const.TeamColors.BLUE: 0,
        }

    def settimermax(self, timermax):
        self.timermax = timermax
        self.timervaluechanged(self.timermax)
        self.timermaxchanged(self.timermax)

    # running the game
    def startgame(self):

        # state to running
        self.setstate(const.GameState.RUNNING)

        # start timer
        self.timerstart = time.time()
        self.root.after(0, self.timerloop)
        self.timerstarted(self.timerstart)

        # start targets    
        self.startalltargets()

    def stopgame(self):

        # called when timer ends

        # state to finished
        self.setstate(const.GameState.FINISHED)

        # stop targets
        self.stopalltargets()

    def timerloop(self):

        # calculate new time left
        remaining = self.timerstart + self.timermax - time.time()
        self.timervaluechanged(remaining)

        if remaining <= const.timeepsilon:
            self.stopgame()
        else:
            self.root.after(const.timerupdateinterval, self.timerloop)

    # ----- hardware controls stuff
    def discovertargets(self):
        self.arenacontroller.requestdiscover()

    def targetcommand(self, targetlist, command):
        self.arenacontroller.requesttargetcommand(targetlist, command)

    def resetalltargets(self):
        self.arenacontroller.resetalltargets()

    def closealltargets(self):
        self.arenacontroller.closealltargets()

    def startalltargets(self):
        self.arenacontroller.startalltargets()

    def stopalltargets(self):
        self.arenacontroller.stopalltargets()

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
        # logging.info("score received: {}".format(hits))

        # store most recent hits line for each target,  
        #   keyed on path and team color; then sum up and notify
        self.targethits[hits[:2]] = hits[2:]
        now = time.time()

        # not 100% sure this is a good idea...I don't want to delay 
        #   scores, but I don't want to flood the system, either
        if now - self.lasthitsreported > 0.25:
            # these are neutral, opposing, final hits
            redtotal = (0, 0, 0)
            bluetotal = (0, 0, 0)
            for devicepath, color in self.targethits.keys():
                if color is const.TeamColors.RED:
                    redtotal = add3tuple(redtotal, self.targethits[devicepath, color])
                elif color is const.TeamColors.BLUE:
                    bluetotal = add3tuple(bluetotal, self.targethits[devicepath, color])

            # store the totals, too:
            self.targethits["total", const.TeamColors.RED] = redtotal
            self.targethits["total", const.TeamColors.BLUE] = bluetotal

            # notify:
            self.scorechanged()

            # test:
            logging.info("hits updated: red = {}, blue = {}".format(redtotal, bluetotal))

            self.lasthitsreported = time.time()

    def getscore(self):
        
        # generate score data from hit data; get robot hits from UI;
        #   multiply out hits to scores

        redhits = self.targethits["total", const.TeamColors.RED]
        bluehits = self.targethits["total", const.TeamColors.BLUE]
        
        # robot hits = 0 for now (UI not connected)
        redscore = (
            redhits[0] * const.ScoreValues.NEUTRAL.value,
            redhits[1] * const.ScoreValues.OPPOSED.value,
            self.robothits[const.TeamColors.RED] * const.ScoreValues.ROBOT.value,
            redhits[2] * const.ScoreValues.FINAL.value,
            )
        bluescore = (
            bluehits[0] * const.ScoreValues.NEUTRAL.value,
            bluehits[1] * const.ScoreValues.OPPOSED.value,
            self.robothits[const.TeamColors.BLUE] * const.ScoreValues.ROBOT.value,
            bluehits[2] * const.ScoreValues.FINAL.value,
            )

        return {
            "redscore": redscore,
            "bluescore": bluescore,
        }


    # ----- notification routines
    def statechanged(self):
        for listener in self.gamechangelisteners:
            listener.gamestatechanged(self.state)

    def metadatachanged(self):
        for listener in self.gamechangelisteners:
            listener.gamemetadatachanged(self.metadata)

    def scorechanged(self):
        for listener in self.gamechangelisteners:
            listener.gamescorechanged(self.getscore())

    def timervaluechanged(self, timervalue):
        for listener in self.gamechangelisteners:
            listener.timervaluechanged(timervalue)

    def timermaxchanged(self, timermax):
        for listener in self.gamechangelisteners:
            listener.timermaxchanged(timermax)

    def timerstarted(self, starttime):
        for listener in self.gamechangelisteners:
            listener.timerstarted(starttime)
