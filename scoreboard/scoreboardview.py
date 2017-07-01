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
    PRIMARY = "primary"
    SECONDARY = "secondary"

# rows in score grid
# version with subscores above, total below:
# NROW = 0
# OROW = 1
# RROW = 2
# FROW = 3
# TROW = 4

# version with total score at top, subscores below:
NROW = 1
OROW = 2
RROW = 3
FROW = 4
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


headerfont = ("Gill Sans", 96)
textfont = ("Gill Sans", 60)
# first draft had all scores at 72
subscorefont = ("Gill Sans", 60)
mainscorefont = ("Gill Sans", 96)
timerfont = ("Gill Sans", 72)
barfont = ("Gill Sans", 18)

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
gamestatebartext = "                         "


# "icon" related
class IconType(enum.Enum):
    INITIAL = "initial"
    WORD = "word"
    CANVAS ="canvas"
# icon = IconType.INITIAL
# icon = IconType.WORD
icon = IconType.CANVAS

# icon drawn on tk Canvas:
canvassize = 64


# ------------------------- ScoreboardView -------------------------
class ScoreboardView(ScoreChangeListener, tk.Toplevel):
    def __init__(self, root, viewtype):
        super().__init__()
        
        # I *think* I need this...        
        self.root = root
        self.viewtype = viewtype


        # game state
        # we need this for calculating correct score
        self.gamestate = const.GameState.UNKNOWN

        # set up UI

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

        # top label
        tk.Label(self.mainframe, text="PixyBattle 2017",
            fg=fgcolor, bg=bgcolor, font=headerfont).pack(side=tk.TOP, pady=20)


        # timer area, plus game state color bars

        self.statebar1 = tk.Label(self.mainframe, 
            text=gamestatebartext, font=barfont,
            bg=gamestatecolors[const.GameState.UNKNOWN])
        self.statebar1.pack(side=tk.TOP)

        # placeholder
        self.timerlabel = tk.Label(self.mainframe,
            fg=fgcolor, bg=bgcolor, font=timerfont)
        self.timerlabel.pack(side=tk.TOP, pady=5)
        self.updatetimer(0)

        self.statebar2 = tk.Label(self.mainframe, 
            text=gamestatebartext, font=barfont,
            bg=gamestatecolors[const.GameState.UNKNOWN])
        self.statebar2.pack(side=tk.TOP)



        # team names: the trick is to keep this centered on the "vs"
        #   when the team names are dissimilar lengths
        # for now, don't worry about it
        self.teamnameframe = tk.Frame(self.mainframe, bg=bgcolor)
        # self.teamnameframe.pack(side=tk.TOP, expand=1, fill=tk.X)
        self.teamnameframe.pack(side=tk.TOP, pady=25)


        self.redteamlabel = tk.Label(self.teamnameframe, text="",
            bg=bgcolor, fg=fgcolor, font=textfont)
        self.redteamlabel.pack(side=tk.LEFT, padx=10)
        
        tk.Label(self.teamnameframe, text="RED", bg=teamredcolor,
            fg=teamnamecolor, font=textfont).pack(side=tk.LEFT, padx=10)

        tk.Label(self.teamnameframe, text="vs", bg=bgcolor,
            fg=fgcolor, font=textfont).pack(side=tk.LEFT)

        tk.Label(self.teamnameframe, text="BLUE", bg=teambluecolor,
            fg=teamnamecolor, font=textfont).pack(side=tk.LEFT, padx=10)
        
        self.blueteamlabel = tk.Label(self.teamnameframe, text="",
            bg=bgcolor, fg=fgcolor, font=textfont)
        self.blueteamlabel.pack(side=tk.LEFT, padx=10)

        # score area: big stack!  grid in new frame
        self.scoreframe = tk.Frame(self.mainframe, bg=bgcolor)
        self.scoreframe.pack(side=tk.TOP)

        # N = score off neutral targets
        self.redNscore = tk.Label(self.scoreframe, text=0,
            bg=bgcolor, fg=fgcolor, font=subscorefont)
        self.redNscore.grid(row=NROW, column=REDCOL)
        self.geticon("N").grid(row=NROW, column=ICONCOL, padx=20)
        self.blueNscore = tk.Label(self.scoreframe, text=0,
            bg=bgcolor, fg=fgcolor, font=subscorefont)
        self.blueNscore.grid(row=NROW, column=BLUECOL)

        # O = score off opposing team targets
        self.redOscore = tk.Label(self.scoreframe, text=0,
            bg=bgcolor, fg=fgcolor, font=subscorefont)
        self.redOscore.grid(row=OROW, column=REDCOL)
        self.geticon("O").grid(row=OROW, column=ICONCOL, padx=20)
        self.blueOscore = tk.Label(self.scoreframe, text=0,
            bg=bgcolor, fg=fgcolor, font=subscorefont)
        self.blueOscore.grid(row=OROW, column=BLUECOL)

        # R = score off opposing team robots
        self.redRscore = tk.Label(self.scoreframe, text=0,
            bg=bgcolor, fg=fgcolor, font=subscorefont)
        self.redRscore.grid(row=RROW, column=REDCOL)
        self.geticon("R").grid(row=RROW, column=ICONCOL, padx=20)
        self.blueRscore = tk.Label(self.scoreframe, text=0,
            bg=bgcolor, fg=fgcolor, font=subscorefont)
        self.blueRscore.grid(row=RROW, column=BLUECOL)

        # F = score off final target ownership
        self.redFscore = tk.Label(self.scoreframe, text=0,
            bg=bgcolor, fg=fgcolor, font=subscorefont)
        self.redFscore.grid(row=FROW, column=REDCOL)
        self.geticon("F").grid(row=FROW, column=ICONCOL, padx=20)
        self.blueFscore = tk.Label(self.scoreframe, text=0,
            bg=bgcolor, fg=fgcolor, font=subscorefont)
        self.blueFscore.grid(row=FROW, column=BLUECOL)

        # T = total score; no "icon", maybe bigger font...
        self.redTscore = tk.Label(self.scoreframe, text=0,
            bg=bgcolor, fg=fgcolor, font=mainscorefont)
        self.redTscore.grid(row=TROW, column=REDCOL)
        tk.Label(self.scoreframe, text="",
            bg=bgcolor, fg=fgcolor, font=mainscorefont).grid(row=TROW, column=ICONCOL, padx=20)
        self.blueTscore = tk.Label(self.scoreframe, text=0,
            bg=bgcolor, fg=fgcolor, font=mainscorefont)
        self.blueTscore.grid(row=TROW, column=BLUECOL)


        # message
        self.messagelabel = tk.Label(self.mainframe, text="",
            bg=bgcolor, fg=fgcolor, font=textfont)
        self.messagelabel.pack(side=tk.TOP, pady=40)


    def isprimaryview(self):
        return self.viewtype is ViewType.PRIMARY

    def updatetimer(self, value):
        minutes = int(value // 60)
        seconds = int(value % 60)
        if minutes <= 0 and seconds < 0:
            seconds = 0
        self.timerlabel.config(text="{}:{:0>2}".format(minutes,seconds))

    # "icon" creation calls
    def geticon(self, which):
        # which = initial code = one of N, O, R, F
        if icon is IconType.INITIAL:
            return self.geticoninitial(which)
        elif icon is IconType.WORD:
            return self.geticonword(which)
        elif icon is IconType.CANVAS:
            return self.geticoncanvas(which)
        
    def geticoninitial(self, which):
        return tk.Label(self.scoreframe, text=which, bg=bgcolor, fg=fgcolor, font=subscorefont)

    def geticonword(self, which):
        if which == "N":
            word = "neutral"
        elif which == "O":
            word = "opposing"
        elif which == "R":
            word = "robot"
        elif which == "F":
            word = "final"
        else:
            word = "unknown"
        return tk.Label(self.scoreframe, text=word, bg=bgcolor, fg=fgcolor, font=subscorefont)
    def geticoncanvas(self, which):
        delta = 10
        iconbounds = delta, delta, canvassize - delta -1, canvassize - delta - 1
        c = tk.Canvas(self.scoreframe, 
            width=canvassize, height=canvassize,
            bg=bgcolor,
            # this line removes a white border around the canvas
            highlightthickness=0,
            )
        if which == "N":
            # green circle
            c.create_arc(*iconbounds, 
                fill="green",
                outline="green",
                start=0.0, 
                extent=359.0,
                )
        elif which == "O":
            # half red/half blue circle
            c.create_arc(*iconbounds,
                fill="red",
                outline="red",
                start=-90.0, 
                extent=180.0,
                )
            c.create_arc(*iconbounds, 
                fill="blue",
                outline="blue",
                start=90.0, 
                extent=180.0,
                )
        elif which == "R":
            # would like a robot silhouette in red/blue
            '''
            #    just do a yellow circle as a placeholder
            c.create_arc(*iconbounds, 
                fill="yellow",
                outline="yellow",
                start=0.0, 
                extent=359.0,
                )
            '''
            # do a yellow star-like zap/explosion icon
            x1, y1, x2, y2 = iconbounds
            dx = x2 - x1
            dy = y2 - y1
            c.create_polygon(
                x1, y1, 
                x1 + dx // 2, y1 + dy // 3,
                x2, y1, 
                x2 - dx // 3, y1 + dy //2,
                x2, y2,
                x1 + dx // 2, y2 - dy // 3,
                x1, y2, 
                x1 + dx // 3, y1 + dy // 2,

                fill="yellow",
                outline="red",
                width=3,
                )

        elif which == "F":
            # little arena layout schematic
            x1, y1, x2, y2 = iconbounds
            dx = x2 - x1
            dy = y2 - y1
            r = 4
            # left edge, halfway down
            c.create_arc(
                x1 - r, y1 + dy // 2 - r, 
                x1 + r, y1 + dy // 2 + r, 
                fill="red",
                outline="red",
                start=0.0, 
                extent=359.0,
                )
            # quarter over, quarter down
            c.create_arc(
                x1 + dx // 4 - r, y1 + dy // 4 - r, 
                x1 + dx // 4 + r, y1 + dy // 4 + r, 
                fill="blue",
                outline="blue",
                start=0.0, 
                extent=359.0,
                )
            # quarter over, quarter up
            c.create_arc(
                x1 + dx // 4 - r, y2 - dy // 4 - r, 
                x1 + dx // 4 + r, y2 - dy // 4 + r, 
                fill="green",
                outline="green",
                start=0.0, 
                extent=359.0,
                )
            # middle, halfway down
            c.create_arc(
                x1 + dx // 2 - r, y1 + dy // 2 - r, 
                x1 + dx // 2 + r, y1 + dy // 2 + r, 
                fill="green",
                outline="green",
                start=0.0, 
                extent=359.0,
                )
            # three quarter over, quarter down
            c.create_arc(
                x2 - dx // 4 - r, y1 + dy // 4 - r, 
                x2 - dx // 4 + r, y1 + dy // 4 + r, 
                fill="red",
                outline="red",
                start=0.0, 
                extent=359.0,
                )
            # three quarter over, quarter up
            c.create_arc(
                x2 - dx // 4 - r, y2 - dy // 4 - r, 
                x2 - dx // 4 + r, y2 - dy // 4 + r, 
                fill="blue",
                outline="blue",
                start=0.0, 
                extent=359.0,
                )
            # right edge, halfway down
            c.create_arc(
                x2 - r, y1 + dy // 2 - r, 
                x2 + r, y1 + dy // 2 + r, 
                fill="green",
                outline="green",
                start=0.0, 
                extent=359.0,
                )
        return c               



    # ----- ScoreChangeListener stuff
    def messagechanged(self, message):
        self.messagelabel.config(text=message)

    def gamemetadatachanged(self, data):
        self.redteamlabel.config(text=const.teamnames[data["redteam"]])
        self.blueteamlabel.config(text=const.teamnames[data["blueteam"]])

    def gamestatechanged(self, data):
        self.statebar1.config(bg=gamestatecolors[const.GameState(data["state"])])
        self.statebar2.config(bg=gamestatecolors[const.GameState(data["state"])])

    def gamescorechanged(self, data):

        redN, redO, redR, redF = data["redscore"]
        blueN, blueO, blueR, blueF = data["bluescore"]

        # don't show final hits until final game states
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

    def timervaluechanged(self, timervalue):
        self.updatetimer(timervalue)



