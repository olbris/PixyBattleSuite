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
from scoreboard.scoreboardview import ViewType


# ------------------------- ScoreboardInputView -------------------------
class ScoreboardInputView(tk.Tk):
    def __init__(self, scoreboardcontroller):
        super().__init__()

        self.scoreboardcontroller = scoreboardcontroller

        # set up UI
        self.title("Scoreboard control")
        self.geometry("+200+900")


        # message setter:
        self.messageframe = tk.Frame(self)
        self.messageframe.pack(side=tk.TOP, pady=20)

        tk.Label(self.messageframe, text="Set messsage:").pack(side=tk.LEFT)
        self.messageentry = tk.Entry(self.messageframe)
        self.messageentry.pack(side=tk.LEFT)
        tk.Button(self.messageframe, text="Set", command=self.setmessage).pack(side=tk.LEFT)
        tk.Button(self.messageframe, text="Clear/Set", command=self.setclearmessage).pack(side=tk.LEFT)

        # visibility
        tk.Label(self, text="Window visibility:").pack(side=tk.TOP)
        self.visibilityframe = tk.Frame(self)
        self.visibilityframe.pack(side=tk.TOP)

        tk.Button(self.visibilityframe, text="Toggle primary",
            command=self.toggleprimaryvisibility).pack(side=tk.LEFT)
        tk.Button(self.visibilityframe, text="Toggle secondary",
            command=self.togglesecondaryvisibility).pack(side=tk.LEFT)



        # ----- buttons at the bottom
        self.buttonframe = tk.Frame(self)
        self.buttonframe.pack(side=tk.BOTTOM, fill=tk.X)

        tk.Button(self.buttonframe, 
            text="Quit", command=self.onquit).pack(side=tk.RIGHT)



    def setmessage(self):
        message = self.messageentry.get()
        self.scoreboardcontroller.setmessage(message)

    def setclearmessage(self):
        self.messageentry.delete(0, tk.END)
        self.scoreboardcontroller.setmessage("")

    def toggleprimaryvisibility(self):
        self.scoreboardcontroller.toggleviewvisibility(ViewType.PRIMARY)

    def togglesecondaryvisibility(self):
        self.scoreboardcontroller.toggleviewvisibility(ViewType.SECONDARY)

    # ----- called by UI
    def onquit(self):
        self.destroy()
