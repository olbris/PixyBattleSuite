"""

scoreboardview.py

this is the scoreboard itself (the visible part)

"""


# ------------------------- imports -------------------------
# std lib
import logging
import tkinter as tk


# local
from scoreboard.scorechangelistener import ScoreChangeListener


# ------------------------- ScoreboardView -------------------------
class ScoreboardView(ScoreChangeListener, tk.Toplevel):
    def __init__(self, root, identifier):
        super().__init__()
        
        # I *think* I need this...        
        self.root = root


        # set up UI
        tk.Label(self, 
            text="\n\n\n\t\t\tscoreboard view {}\t\t\t\n\n\n".format(identifier)).pack()


        # test message display
        self.messagelabel = tk.Label(self, text="(no message)")
        self.messagelabel.pack()


    # ----- ScoreChangeListener stuff
    def messagechanged(self, message):
        self.messagelabel.config(text=message)


