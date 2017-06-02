"""

GameChangeListener

interface for anything that responds to game change
events from the game controller

"""

# ------------------------- imports -------------------------





# ------------------------- GameChangeListener -------------------------
class GameChangeListener:

    # all of these methods are optional to implement
    def gamestatechanged(self, state):
        pass