"""

GamemasterView.py

UI for the game master

"""

# ------------------------- imports -------------------------
# std lib
import tkinter


# local
from gamemaster.gamechangelistener import GameChangeListener


# ------------------------- GamemasterView -------------------------
class GamemasterView(GameChangeListener, tkinter.Tk):
    def __init__(self, gamecontroller):
        super().__init__()

        self.gamecontroller = gamecontroller

        # set up UI
        self.label = tkinter.Label(self, text="Hello World", padx=5, pady=5) 
        self.label.pack()


