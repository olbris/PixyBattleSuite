"""

bigscoreboardview.py

alternate scoreboard, with bigger but less text

"""


# ------------------------- imports -------------------------
# std lib
import enum
import logging
import tkinter as tk


# local
from shared import constants as const
from scoreboard.scorechangelistener import ScoreChangeListener

# ------------------------- constants -------------------------

# rows in score grid; only one now
TROW = 0

# columns in score grid:
REDCOL = 0
ICONCOL = 1
BLUECOL = 2

# lots of appearance values

# placeholder value, just listing them for now
bgcolor = "black"
fgcolor = "white"

# team names:
teamredcolor = "red"
teambluecolor = "blue"
teamnamecolor = "white"


spacerfont = ("Gill Sans", 32)
textfont = ("Gill Sans", 72)
teamnamefont = ("Gill Sans", 96)
mainscorefont = ("Gill Sans", 256)
timerfont = ("Gill Sans", 168)
barfont = ("Gill Sans", 36)

# game state colors
gamestatecolors = {
    const.GameState.UNKNOWN: "red",
    const.GameState.TESTING: "brown",
    const.GameState.IDLE: "gray70",
    const.GameState.PREPARING: "yellow",
    const.GameState.READY: "orange",
    const.GameState.RUNNING: "green",
    const.GameState.PAUSED: "red",
    const.GameState.FINISHED: "blue",
    const.GameState.FINAL: "purple",
}
gamestatebartext = "                             "


# ------------------------- BigScoreboardView -------------------------
class BigScoreboardView(ScoreChangeListener, tk.Toplevel):
    def __init__(self, root, viewtype):
        super().__init__()
        
        # I *think* I need this...        
        self.root = root
        self.viewtype = viewtype

        # this should only be a primary view, but I'm
        #   leaving all the machinary in just in case I
        #   change my mind later
        if self.viewtype is not const.ViewType.PRIMARY:
            raise ValueError("BigScoreboardView must be a primary view!")


        # game state
        # we need this for calculating correct score
        self.gamestate = const.GameState.UNKNOWN

        # set up UI
        self.scorekeyvisible = False

        # make the primary window borderless
        if self.isprimaryview():
            # got this from the Internet; I wasn't sure which parts
            #   were vital or not, so I copied them all and tested;
            # strangely enough, the only thing that seems necessary
            #   is the single command that's *supposed* to work, but
            #   is (a) reputed to be flaky on Mac, and (b) didn't
            #   work in initial testing

            # Hide the root window drag bar and close button
            self.overrideredirect(True)
            # Make the root window always on top
            # self.wm_attributes("-topmost", True)
            # Make the window content area transparent
            # self.wm_attributes("-transparent", True)
            # Set the root window background color to a transparent color
            # self.config(bg='systemTransparent')
        

        if self.isprimaryview():
            self.geometry("1500x1000")
        else:
            self.geometry("1000x1000+900+10")


        self.mainframe = tk.Frame(self, bg=bgcolor)
        self.mainframe.pack(side=tk.TOP, expand=1, fill=tk.BOTH)

        # spacer
        tk.Label(self.mainframe, text="   ", 
            font=spacerfont, bg=bgcolor).pack(side=tk.TOP)

        # timer area, plus game state color bars
        self.statebar1 = tk.Label(self.mainframe, 
            text=gamestatebartext, font=barfont,
            bg=gamestatecolors[const.GameState.UNKNOWN])
        self.statebar1.pack(side=tk.TOP)

        self.timerlabel = tk.Label(self.mainframe,
            fg=fgcolor, bg=bgcolor, font=timerfont)
        self.timerlabel.pack(side=tk.TOP, pady=5)
        self.updatetimer(0)

        self.statebar2 = tk.Label(self.mainframe, 
            text=gamestatebartext, font=barfont,
            bg=gamestatecolors[const.GameState.UNKNOWN])
        self.statebar2.pack(side=tk.TOP)

        # spacer
        tk.Label(self.mainframe, text="   ", 
            font=spacerfont, bg=bgcolor).pack(side=tk.TOP)


        # team names: switch to a grid for this view
        self.teamnameframe = tk.Frame(self.mainframe, bg=bgcolor)
        self.teamnameframe.pack(side=tk.TOP, pady=5)


        self.redteamlabel = tk.Label(self.teamnameframe, text="",
            bg=bgcolor, fg=fgcolor, font=teamnamefont)
        self.redteamlabel.grid(row=0, column=REDCOL, padx=10, sticky=tk.E)
        
        tk.Label(self.teamnameframe, text=" vs ", bg=bgcolor,
            fg=fgcolor, font=textfont).grid(row=0, column=ICONCOL)

        self.blueteamlabel = tk.Label(self.teamnameframe, text="",
            bg=bgcolor, fg=fgcolor, font=teamnamefont)
        self.blueteamlabel.grid(row=0, column=BLUECOL, padx=10, sticky=tk.W)

        tk.Label(self.teamnameframe, text="RED", bg=teamredcolor,
            fg=teamnamecolor, font=textfont).grid(row=1, column=REDCOL, 
            padx=10, pady=10, sticky=tk.E)

        tk.Label(self.teamnameframe, text="BLUE", bg=teambluecolor,
            fg=teamnamecolor, font=textfont).grid(row=1, column=BLUECOL, 
            padx=10, pady=10, sticky=tk.W)
        

        # score area: only total score now
        self.scoreframe = tk.Frame(self.mainframe, bg=bgcolor)
        self.scoreframe.pack(side=tk.TOP)

        # T = total score; no "icon", maybe bigger font...
        self.redTscore = tk.Label(self.scoreframe, text=0,
            bg=bgcolor, fg=fgcolor, font=mainscorefont)
        self.redTscore.grid(row=TROW, column=REDCOL)
        tk.Label(self.scoreframe, text=" ",
            bg=bgcolor, fg=fgcolor, font=mainscorefont).grid(row=TROW, column=ICONCOL, padx=20)
        self.blueTscore = tk.Label(self.scoreframe, text=0,
            bg=bgcolor, fg=fgcolor, font=mainscorefont)
        self.blueTscore.grid(row=TROW, column=BLUECOL)


    def isprimaryview(self):
        return self.viewtype is const.ViewType.PRIMARY

    def updatetimer(self, value):
        minutes = int(value // 60)
        seconds = int(value % 60)
        if value < 0:
            minutes = 0
            seconds = 0
        if minutes < 0:
            minutes = 0
        if seconds < 0:
            seconds = 0
        self.timerlabel.config(text="{}:{:0>2}".format(minutes,seconds))

    def togglescorekey(self):
        pass

    # ----- ScoreChangeListener stuff
    def messagechanged(self, message):
        pass

    def gamemetadatachanged(self, data):
        self.redteamlabel.config(text=const.teamnames[data["redteam"]])
        self.blueteamlabel.config(text=const.teamnames[data["blueteam"]])

    def gamestatechanged(self, data):
        self.gamestate = const.GameState(data["state"])
        self.statebar1.config(bg=gamestatecolors[self.gamestate])
        self.statebar2.config(bg=gamestatecolors[self.gamestate])
        # self.statebar1.config(bg=gamestatecolors[const.GameState(data["state"])])
        # self.statebar2.config(bg=gamestatecolors[const.GameState(data["state"])])

    def gamescorechanged(self, data):

        redN, redO, redR, redF = data["redscore"]
        blueN, blueO, blueR, blueF = data["bluescore"]

        # print("bigscoreview: red: ", redN, redO, redR, redF)
        # print("bigscoreview: blue: ", blueN, blueO, blueR, blueF)
        # don't show final hits until final game states
        # print("gamestate: ", self.gamestate.value)
        if (self.gamestate is const.GameState.FINAL or 
            self.gamestate is const.GameState.FINISHED):
            redtotal = redN + redO + redR + redF
            bluetotal = blueN + blueO + blueR + blueF
        else:
            # could leave out robot scores, too, as they
            #   aren't expected to be filled in until the
            #   end, but it doesn't really matter
            redtotal = redN + redO + redR
            bluetotal = blueN + blueO + blueR

        '''
        # does this work if we always add?
        redtotal = redN + redO + redR + redF
        bluetotal = blueN + blueO + blueR + blueF
        '''
        # print("totals: ", redtotal, bluetotal)

        self.redTscore.config(text=str(redtotal))
        self.blueTscore.config(text=str(bluetotal))

    def timervaluechanged(self, timervalue):
        self.updatetimer(timervalue)



