"""

scoreboardview.py

this is the scoreboard itself (the visible part)

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
class ViewType(enum.Enum):
    PUBLIC = "public"
    PRIVATE = "private"

# rows in score grid
NROW = 0
OROW = 1
RROW = 2
FROW = 3
TROW = 4

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


textfont = ("Gill Sans", 60)
scorefont = ("Gill Sans", 72)
timerfont = ("Gill Sans", 96)




# ------------------------- ScoreboardView -------------------------
class ScoreboardView(ScoreChangeListener, tk.Toplevel):
    def __init__(self, root, viewtype):
        super().__init__()
        
        # I *think* I need this...        
        self.root = root
        self.viewtype = viewtype



        # set up UI
        
        self.geometry("1500x1000")

        self.mainframe = tk.Frame(self, bg=bgcolor)
        self.mainframe.pack(side=tk.TOP, expand=1, fill=tk.BOTH)

        # top label
        tk.Label(self.mainframe, text="PixyBattle 2017",
            fg=fgcolor, bg=bgcolor, font=("Gill Sans", 96)).pack(side=tk.TOP, pady=20)


        # timer area
        # placeholder
        # maybe color bars above and below?
        tk.Label(self.mainframe, text="0:00",
            fg=fgcolor, bg=bgcolor, font=scorefont).pack(side=tk.TOP, pady=20)

        # team names: the trick is to keep this centered on the "vs"
        #   when the team names are dissimilar lengths
        # for now, don't worry about it
        self.teamnameframe = tk.Frame(self.mainframe, bg=bgcolor)
        # self.teamnameframe.pack(side=tk.TOP, expand=1, fill=tk.X)
        self.teamnameframe.pack(side=tk.TOP)


        self.redteamlabel = tk.Label(self.teamnameframe, text="",
            bg=bgcolor, fg=fgcolor, font=textfont)
        self.redteamlabel.pack(side=tk.LEFT)
        
        tk.Label(self.teamnameframe, text="RED", bg=teamredcolor,
            fg=teamnamecolor, font=textfont).pack(side=tk.LEFT, padx=10)

        tk.Label(self.teamnameframe, text="vs", bg=bgcolor,
            fg=fgcolor, font=textfont).pack(side=tk.LEFT)

        tk.Label(self.teamnameframe, text="BLUE", bg=teambluecolor,
            fg=teamnamecolor, font=textfont).pack(side=tk.LEFT, padx=10)
        
        self.blueteamlabel = tk.Label(self.teamnameframe, text="",
            bg=bgcolor, fg=fgcolor, font=textfont)
        self.blueteamlabel.pack(side=tk.LEFT)

        # score area: big stack!  grid in new frame
        self.scoreframe = tk.Frame(self.mainframe, bg=bgcolor)
        self.scoreframe.pack(side=tk.TOP)

        # N = score off neutral targets
        self.redNscore = tk.Label(self.scoreframe, text=0,
            bg=bgcolor, fg=fgcolor, font=scorefont)
        self.redNscore.grid(row=NROW, column=REDCOL)
        tk.Label(self.scoreframe, text="N",
            bg=bgcolor, fg=fgcolor, font=scorefont).grid(row=NROW, column=ICONCOL)
        self.blueNscore = tk.Label(self.scoreframe, text=0,
            bg=bgcolor, fg=fgcolor, font=scorefont)
        self.blueNscore.grid(row=NROW, column=BLUECOL)

        # O = score off opposing team targets
        self.redOscore = tk.Label(self.scoreframe, text=0,
            bg=bgcolor, fg=fgcolor, font=scorefont)
        self.redOscore.grid(row=OROW, column=REDCOL)
        tk.Label(self.scoreframe, text="O",
            bg=bgcolor, fg=fgcolor, font=scorefont).grid(row=OROW, column=ICONCOL)
        self.blueOscore = tk.Label(self.scoreframe, text=0,
            bg=bgcolor, fg=fgcolor, font=scorefont)
        self.blueOscore.grid(row=OROW, column=BLUECOL)

        # R = score off opposing team robots
        self.redRscore = tk.Label(self.scoreframe, text=0,
            bg=bgcolor, fg=fgcolor, font=scorefont)
        self.redRscore.grid(row=RROW, column=REDCOL)
        tk.Label(self.scoreframe, text="R",
            bg=bgcolor, fg=fgcolor, font=scorefont).grid(row=RROW, column=ICONCOL)
        self.blueRscore = tk.Label(self.scoreframe, text=0,
            bg=bgcolor, fg=fgcolor, font=scorefont)
        self.blueRscore.grid(row=RROW, column=BLUECOL)

        # F = score off final target ownership
        self.redFscore = tk.Label(self.scoreframe, text=0,
            bg=bgcolor, fg=fgcolor, font=scorefont)
        self.redFscore.grid(row=FROW, column=REDCOL)
        tk.Label(self.scoreframe, text="F",
            bg=bgcolor, fg=fgcolor, font=scorefont).grid(row=FROW, column=ICONCOL)
        self.blueFscore = tk.Label(self.scoreframe, text=0,
            bg=bgcolor, fg=fgcolor, font=scorefont)
        self.blueFscore.grid(row=FROW, column=BLUECOL)

        # T = total score; maybe no "icon", maybe bigger font...
        self.redTscore = tk.Label(self.scoreframe, text=0,
            bg=bgcolor, fg=fgcolor, font=scorefont)
        self.redTscore.grid(row=TROW, column=REDCOL)
        tk.Label(self.scoreframe, text="",
            bg=bgcolor, fg=fgcolor, font=scorefont).grid(row=TROW, column=ICONCOL)
        self.blueTscore = tk.Label(self.scoreframe, text=0,
            bg=bgcolor, fg=fgcolor, font=scorefont)
        self.blueTscore.grid(row=TROW, column=BLUECOL)





        # test message display
        # maybe put right under timer, or over timer/under top label>
        self.messagelabel = tk.Label(self.mainframe, text="",
            bg=bgcolor, fg=fgcolor, font=textfont)
        self.messagelabel.pack(side=tk.TOP, pady=40)


    def ispublicview(self):
        return self.viewtype is ViewType.PUBLIC
    def isprivateview(self):
        return self.viewtype is ViewType.PRIVATE

    # ----- ScoreChangeListener stuff
    def messagechanged(self, message):
        self.messagelabel.config(text=message)

    def gamemetadatachanged(self, data):
        self.redteamlabel.config(text=const.teamnames[data["redteam"]])
        self.blueteamlabel.config(text=const.teamnames[data["blueteam"]])

    def gamestatechanged(self, data):
        pass

    def gamescorechanged(self, data):

        redN, redO, redR, redF = data["redscore"]
        blueN, blueO, blueR, blueF = data["bluescore"]

        redtotal = redN + redO + redR + redF
        bluetotal = blueN + blueO + blueR + blueF

        # maybe don't show final hits in some game states?

        self.redNscore.config(text=redN)
        self.redOscore.config(text=redO)
        self.redRscore.config(text=redR)
        self.redFscore.config(text=redF)
        self.redTscore.config(text=redtotal)

        self.blueNscore.config(text=blueN)
        self.blueOscore.config(text=blueO)
        self.blueRscore.config(text=blueR)
        self.blueFscore.config(text=blueF)
        self.blueTscore.config(text=bluetotal)





