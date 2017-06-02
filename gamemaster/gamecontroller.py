"""

gamecontroller.py

technically it's the model and controller for the game software

- keeps game state
- when hardware changes come in, it updates game state and notifies listeners
- when UI input come in, it updates game state and notifies listeners

"""

class GameController:
    def __init__(self):
        

        self.gamechangelisteners = []



    def addchangelistener(listener):
        self.gamechangelisteners.append(listener)

    

