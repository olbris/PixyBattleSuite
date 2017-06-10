"""

GamemasterView.py

UI for the game master

"""

# ------------------------- imports -------------------------
# std lib
import logging
import tkinter as tk


# local
from shared import constants as const
from gamemaster.gamechangelistener import GameChangeListener
from gamemaster.hardwarechangelistener import HardwareChangeListener


# ------------------------- GamemasterView -------------------------
class GamemasterView(GameChangeListener, HardwareChangeListener, tk.Tk):
    def __init__(self, gamecontroller):
        super().__init__()

        self.gamecontroller = gamecontroller

        self.targetlist = []

        # set up UI
        self.title("Gamemaster")
        # self.geometry("123x123")

        # top main frame will be split in two; direct hardware
        #   control on the left, mostly for testing, and 
        #   game control on the right

        self.mainframe = tk.Frame(self)
        self.mainframe.pack(side=tk.TOP, fill=tk.BOTH)

        # hardware controls
        self.leftframe = tk.Frame(self.mainframe)
        self.leftframe.pack(side=tk.LEFT, fill=tk.BOTH)

        tk.Label(self.leftframe, text="\n\n\n\t\thardware controls\t\t\t\n\n\n").pack()

        tk.Button(self.leftframe, 
            text="Discover", command=self.ondiscover).pack(side=tk.TOP)


        self.targetcountlabel = tk.Label(self.leftframe,
            text="# targets = (unknown)")
        self.targetcountlabel.pack(side=tk.TOP)

        # game controls
        self.rightframe = tk.Frame(self.mainframe)
        self.rightframe.pack(side=tk.RIGHT, fill=tk.BOTH)

        tk.Label(self.rightframe, text="\n\n\n\t\tgame controls\t\t\t\n\n\n").pack()


        # buttons at the bottom
        self.buttonframe = tk.Frame(self)
        self.buttonframe.pack(side=tk.BOTTOM, fill=tk.X)

        tk.Button(self.buttonframe, 
            text="Quit", command=self.onquit).pack(side=tk.RIGHT)


        # leftover test stuff; remove when totally unneeded

        # test game state controls: output label and input buttons
        # should really have a frame here
        self.statelabel = tk.Label(self)
        self.statelabel.pack()

        tk.Button(self, text="Idle", command=self.setstateidle).pack()
        tk.Button(self, text="Running", command=self.setstaterunning).pack()


        # populate initial data here (eg, fill in game state label)
        self.updatestatelabel(const.GameState.UNKNOWN)

    # ----- update routines
    def updatestatelabel(self, state):
        self.statelabel.config(text="State: {}".format(state.value))

    # ----- called by UI
    def ondiscover(self):
        self.gamecontroller.discovertargets()

    def onquit(self):

        # close serial ports

        # we're done
        self.destroy()


    def setstateidle(self):
        self.gamecontroller.setstate(const.GameState.IDLE)

    def setstaterunning(self):
        self.gamecontroller.setstate(const.GameState.RUNNING)

    # ----- GameChangeListener methods
    def gamestatechanged(self, state):
        self.updatestatelabel(state)




    # ----- HardwareChangeListener methods
    def targetsdiscovered(self, targetlist):
        self.targetlist = targetlist
        self.targetcountlabel.config(text="# targets = {}".format(len(self.targetlist)))








