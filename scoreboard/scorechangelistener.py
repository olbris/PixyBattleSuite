"""

ScoreChangeListener

interface for anything that responds to score changes

"""

# ------------------------- imports -------------------------





# ------------------------- ScoreChangeListener -------------------------
class ScoreChangeListener:

    # all of these methods are optional to implement

    # metadata
    def messagechanged(self, message):
        pass

    def gamemetadatachanged(self, metadata):
        pass

    # score


    # game state and timer
    def gamestatechanged(self, state):
        pass
