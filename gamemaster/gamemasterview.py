"""

GamemasterView.py

UI for the game master

"""

# ------------------------- imports -------------------------
# std lib
import tkinter as tk


# local
from shared import constants as const
from gamemaster.gamechangelistener import GameChangeListener


# ------------------------- GamemasterView -------------------------
class GamemasterView(GameChangeListener, tk.Tk):
    def __init__(self, gamecontroller):
        super().__init__()

        self.gamecontroller = gamecontroller

        # set up UI
        tk.Label(self, text="\n\n\n\t\t\tplaceholder\t\t\t\n\n\n").pack()

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
    def setstateidle(self):
        self.gamecontroller.setstate(const.GameState.IDLE)

    def setstaterunning(self):
        self.gamecontroller.setstate(const.GameState.RUNNING)

    # ----- GameChangeListener methods
    def gamestatechanged(self, state):
        self.updatestatelabel(state)












