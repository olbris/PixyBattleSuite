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

# lots of appearance values

# placeholder value, just listing them for now
bgcolor = 1
textcolor = 1

scorefont = 1
timerfont = 1




# ------------------------- ScoreboardView -------------------------
class ScoreboardView(ScoreChangeListener, tk.Toplevel):
    def __init__(self, root, viewtype):
        super().__init__()
        
        # I *think* I need this...        
        self.root = root

        self.viewtype = viewtype


        # set up UI
        tk.Label(self, 
            text="\n\n\n\t\t\tscoreboard view\t\t\t\n\n\n").pack()

        # testing: 
        if isprivateview():
            tk.Label(self, text="\n\n\t\tthis is a private view!\t\t\n\n").pack()


        # test message display
        self.messagelabel = tk.Label(self, text="(no message)")
        self.messagelabel.pack()

        # test team name display
        self.teamnameframe = tk.Frame(self)
        self.teamnameframe.pack()
        tk.Label(self.teamnameframe, text="RED team: ").pack(side=tk.LEFT)
        self.redteamlabel = tk.Label(self.teamnameframe, text="")
        self.redteamlabel.pack(side=tk.LEFT)
        tk.Label(self.teamnameframe, text="BLUE team: ").pack(side=tk.LEFT)
        self.blueteamlabel = tk.Label(self.teamnameframe, text="")
        self.blueteamlabel.pack(side=tk.LEFT)

        # test game state
        self.gamestatelabel = tk.Label(self, text="")
        if isprivateview():
            self.gamestatelabel.pack()

    def ispublicview(self):
        return self.viewtype is ViewType.PUBLIC
    def isprivateview(self):
        return self.viewtype is ViewType.PRIVATE

    # ----- ScoreChangeListener stuff
    def messagechanged(self, message):
        self.messagelabel.config(text=message)

    def gamemetadatachanged(self, metadata):
        self.redteamlabel.config(text=const.teamnames[metadata["red"]])
        self.blueteamlabel.config(text=const.teamnames[metadata["blue"]])


    def gamestatechanged(self, state):
        self.gamestatelabel.config(text=state.value)


