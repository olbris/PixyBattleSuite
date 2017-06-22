"""

GameChangeListener

interface for anything that responds to game change
events from the game controller

"""

# ------------------------- GameChangeListener -------------------------
class GameChangeListener:

    # all of these methods are optional to implement
    def gamestatechanged(self, state):
        pass

    def gamemetadatachanged(self, metadata):
        pass

    def gamescorechanged(self, scoredata):
        pass
    
    def timervaluechanged(self, timervalue):
        pass

    def timermaxchanged(self, timermax):
        pass

    def timerstarted(self, starttime):
        pass