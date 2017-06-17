"""

GamemasterView.py

UI for the game master

"""

# ------------------------- imports -------------------------
# std lib
import logging
import tkinter as tk
from tkinter import messagebox


# local
from shared import constants as const
from gamemaster.gamechangelistener import GameChangeListener
from gamemaster.hardwarechangelistener import HardwareChangeListener


# ------------------------- constants -------------------------

# I'm hardcoding the number of targets for now, to simplify
#   the layout (so I don't have to make it dynamic); I believe
#   there are only ten targets built
maxtargets = 10


# ------------------------- GamemasterView -------------------------
class GamemasterView(GameChangeListener, HardwareChangeListener, tk.Tk):
    def __init__(self, gamecontroller):
        super().__init__()

        self.gamecontroller = gamecontroller

        self.targetlist = []

        # target grid UI components
        self.targetcheckvars = {}
        self.targetnamelabels = {}
        self.targetpathlabels = {}

        # set up UI
        self.title("Gamemaster")
        # self.geometry("123x123")

        # top main frame will be split in two; direct hardware
        #   control on the left, mostly for testing, and 
        #   game control on the right

        self.mainframe = tk.Frame(self)
        self.mainframe.pack(side=tk.TOP, fill=tk.BOTH)

        # ----- hardware controls
        self.leftframe = tk.Frame(self.mainframe)
        self.leftframe.pack(side=tk.LEFT, fill=tk.BOTH)

        tk.Label(self.leftframe, text="Hardware controls").pack(side=tk.TOP)

        self.hwbuttonframe = tk.Frame(self.leftframe)
        self.hwbuttonframe.pack(side=tk.TOP)

        tk.Label(self.hwbuttonframe, text="Select:").pack(side=tk.LEFT)
        tk.Button(self.hwbuttonframe, text="All", command=self.selectalltargets).pack(side=tk.LEFT)
        tk.Button(self.hwbuttonframe, text="None", command=self.selectnonetargets).pack(side=tk.LEFT)
        tk.Button(self.hwbuttonframe, text="Discover", command=self.ondiscover).pack(side=tk.TOP)

        self.targetgrid = tk.Frame(self.leftframe)
        self.targetgrid.pack(side=tk.TOP)

        for row in range(maxtargets):
            self.targetcheckvars[row] = tk.IntVar()
            tk.Checkbutton(self.targetgrid, variable=self.targetcheckvars[row]).grid(row=row, column=0)

            self.targetnamelabels[row] = tk.Label(self.targetgrid, text="")
            self.targetnamelabels[row].grid(row=row, column=1, padx=5)

            self.targetpathlabels[row] = tk.Label(self.targetgrid, text="")
            self.targetpathlabels[row].grid(row=row, column=2)

        # two rows of command buttons
        self.commandframe1 = tk.Frame(self.leftframe)
        self.commandframe1.pack(side=tk.TOP)
        tk.Button(self.commandframe1, text="RESET", command=self.ontargetreset).pack(side=tk.LEFT)
        tk.Button(self.commandframe1, text="START", command=self.ontargetstart).pack(side=tk.LEFT)
        tk.Button(self.commandframe1, text="STOP", command=self.ontargetstop).pack(side=tk.LEFT)

        self.commandframe2 = tk.Frame(self.leftframe)
        self.commandframe2.pack(side=tk.TOP)
        tk.Button(self.commandframe2, text="TEST_RED", command=self.ontargettestred).pack(side=tk.LEFT)
        tk.Button(self.commandframe2, text="TEST_BLUE", command=self.ontargettestblue).pack(side=tk.LEFT)
        tk.Button(self.commandframe2, text="TEST_GREEN", command=self.ontargettestgreen).pack(side=tk.LEFT)
        tk.Button(self.commandframe2, text="TEST_REDBLUE", command=self.ontargettestredblue).pack(side=tk.LEFT)


        # ----- game controls
        self.rightframe = tk.Frame(self.mainframe)
        self.rightframe.pack(side=tk.RIGHT, fill=tk.BOTH)

        tk.Label(self.rightframe, text="Game controls").pack(side=tk.TOP)

        # team input:
        self.metadataframe = tk.Frame(self.rightframe)
        self.metadataframe.pack(side=tk.TOP)

        teamnumberlist = const.getteamnumberlist()

        tk.Label(self.metadataframe, text="RED team: ").pack(side=tk.LEFT)
        self.redteamvar = tk.IntVar()
        self.redteamvar.set(teamnumberlist[0])
        self.redteammenu = tk.OptionMenu(self.metadataframe, self.redteamvar,
            *teamnumberlist)
        self.redteammenu.pack(side=tk.LEFT)

        tk.Label(self.metadataframe, text="BLUE team: ").pack(side=tk.LEFT)
        self.blueteamvar = tk.IntVar()
        self.blueteamvar.set(teamnumberlist[0])
        self.blueteammenu = tk.OptionMenu(self.metadataframe, self.blueteamvar,
            *teamnumberlist)
        self.blueteammenu.pack(side=tk.LEFT)

        tk.Button(self.metadataframe, text="Set", command=self.onsetmetadata).pack(side=tk.LEFT)


        # robot hits
        tk.Label(self.rightframe, text="Robot hits").pack(side=tk.TOP, pady=20)

        self.robothitframe = tk.Frame(self.rightframe)
        self.robothitframe.pack(side=tk.TOP)

        tk.Label(self.robothitframe, text="RED: ").pack(side=tk.LEFT, padx=5)
        self.redrobothitsvar = tk.IntVar()
        self.redrobothitsvar.set(0)
        tk.Spinbox(self.robothitframe, from_=0, to=1000,
            textvariable=self.redrobothitsvar).pack(side=tk.LEFT)

        tk.Label(self.robothitframe, text="BLUE: ").pack(side=tk.LEFT, padx=5)
        self.bluerobothitsvar = tk.IntVar()
        self.bluerobothitsvar.set(0)
        tk.Spinbox(self.robothitframe, from_=0, to=1000,
            textvariable=self.bluerobothitsvar).pack(side=tk.LEFT)

        tk.Button(self.robothitframe, text="Set", 
            command=self.onsetrobothits).pack(side=tk.LEFT, padx=5)

        # ----- buttons at the bottom
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

    def getselectedtargets(self):
        # returns list of device paths that are selected
        result = []
        for row in range(maxtargets):
            devicepath = self.targetpathlabels[row].cget("text")
            if devicepath:
                if self.targetcheckvars[row].get():
                    result.append(devicepath)
        return result

    # ----- update routines
    def updatestatelabel(self, state):
        self.statelabel.config(text="State: {}".format(state.value))

    # ----- called by UI
    def onquit(self):

        # close serial ports (I don't think it's necessary, but
        #   try to be neat)
        self.gamecontroller.closealltargets()

        # we're done
        self.destroy()

    # hardware controls
    def ondiscover(self):
        self.gamecontroller.discovertargets()

    def ontargetreset(self):
        self.gamecontroller.targetcommand(self.getselectedtargets(), 
            const.Commands.RESET)

    def ontargetstart(self):
        self.gamecontroller.targetcommand(self.getselectedtargets(), 
            const.Commands.START)

    def ontargetstop(self):
        self.gamecontroller.targetcommand(self.getselectedtargets(), 
            const.Commands.STOP)

    def ontargettestred(self):
        self.gamecontroller.targetcommand(self.getselectedtargets(), 
            const.Commands.TEST_RED)

    def ontargettestblue(self):
        self.gamecontroller.targetcommand(self.getselectedtargets(), 
            const.Commands.TEST_BLUE)

    def ontargettestgreen(self):
        self.gamecontroller.targetcommand(self.getselectedtargets(), 
            const.Commands.TEST_GREEN)

    def ontargettestredblue(self):
        self.gamecontroller.targetcommand(self.getselectedtargets(), 
            const.Commands.TEST_RED_BLUE)

    def selectalltargets(self):
        for row in range(maxtargets):
            self.targetcheckvars[row].set(1)

    def selectnonetargets(self):
        for row in range(maxtargets):
            self.targetcheckvars[row].set(0)


    # game controls
    def onsetmetadata(self):
        redteamnumber = self.redteamvar.get()
        blueteamnumber = self.blueteamvar.get()
        if redteamnumber == blueteamnumber: 
            messagebox.showerror("Bad team numbers", "Team numbers can't be the same!")
            return

        metadata = {
            "redteam": redteamnumber,
            "blueteam": blueteamnumber,
        }
        self.gamecontroller.setmetadata(metadata)

    def onsetrobothits(self):
        self.gamecontroller.setrobothits(self.redrobothitsvar.get(),
            self.bluerobothitsvar.get())
        self.gamecontroller.scorechanged()

    # testing
    def setstateidle(self):
        self.gamecontroller.setstate(const.GameState.IDLE)

    def setstaterunning(self):
        self.gamecontroller.setstate(const.GameState.RUNNING)

    # ----- GameChangeListener methods
    def gamestatechanged(self, state):
        self.updatestatelabel(state)




    # ----- HardwareChangeListener methods
    def targetsdiscovered(self, targetlist):
        self.targetlist = sorted(targetlist, key=lambda item:item[0])

        # clear existing names, paths
        for row in range(maxtargets):
            self.targetnamelabels[row].config(text="")
            self.targetpathlabels[row].config(text="")

        # put in new ones
        for row, target in enumerate(self.targetlist):
            self.targetnamelabels[row].config(text=target[0])
            self.targetpathlabels[row].config(text=target[1])

        # deselect all
        self.selectnonetargets()








