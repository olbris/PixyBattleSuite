"""

ScoreboardInputView.py

controls for the scoreboard; only buttons and input, 
nothing displayed (it's only displayed on the scoreboard views)

"""

# ------------------------- imports -------------------------
# std lib
import tkinter as tk


# local
from shared import constants as const


# ------------------------- ScoreboardInputView -------------------------
class ScoreboardInputView(tk.Tk):
    def __init__(self, scoreboardcontroller):
        super().__init__()

        self.scoreboardcontroller = scoreboardcontroller

        # set up UI
        tk.Label(self, text="\n\n\n\t\t\tscoreboardinputview\t\t\t\n\n\n").pack()


        # test message setter:
        tk.Label(self, text="Set messsage:").pack()
        self.messageentry = tk.Entry(self)
        self.messageentry.pack()
        tk.Button(self, text="Submit", command=self.setmessage).pack()

        # ----- buttons at the bottom
        self.buttonframe = tk.Frame(self)
        self.buttonframe.pack(side=tk.BOTTOM, fill=tk.X)

        tk.Button(self.buttonframe, 
            text="Quit", command=self.onquit).pack(side=tk.RIGHT)



    def setmessage(self):
        message = self.messageentry.get()
        if message:
            self.scoreboardcontroller.setmessage(message)

    # ----- called by UI
    def onquit(self):
        self.destroy()
