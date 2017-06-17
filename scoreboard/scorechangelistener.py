"""

ScoreChangeListener

interface for anything that responds to score changes, 
on the scoreboard side

"""

# ------------------------- ScoreChangeListener -------------------------
class ScoreChangeListener:

    # all of these methods are optional to implement

    # metadata
    def messagechanged(self, message):
        pass

    def gamemetadatachanged(self, metadata):
        pass

    # score
    def gamescorechanged(self, score):
        pass

    # game state
    def gamestatechanged(self, state):
        pass
