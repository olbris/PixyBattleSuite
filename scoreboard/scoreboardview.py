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
from scoreboard.scorechangelistener import ScoreChangeListener

# ------------------------- constants -------------------------
class ViewType(enum.Enum):
    PUBLIC = "public"
    PRIVATE = "private"


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
        if self.viewtype is ViewType.PRIVATE:
            tk.Label(self, text="\n\n\t\tthis is a private view!\t\t\n\n").pack()


        # test message display
        self.messagelabel = tk.Label(self, text="(no message)")
        self.messagelabel.pack()

        # test game state
        self.gamestatelabel = tk.Label(self, text="")
        if self.viewtype is ViewType.PRIVATE:
            self.gamestatelabel.pack()


    # ----- ScoreChangeListener stuff
    def messagechanged(self, message):
        self.messagelabel.config(text=message)

    def gamestatechanged(self, state):
        self.gamestatelabel.config(text=state.value)


