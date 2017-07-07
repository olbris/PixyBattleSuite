"""

scoreboard.py

"""

# ------------------------- imports -------------------------
# std lib
import logging


# local
from shared import constants as const
from scoreboard.scoreboardcontroller import ScoreboardController
from scoreboard.scoreboardinputview import ScoreboardInputView
from scoreboard.scoreboardview import ScoreboardView
from scoreboard.bigscoreboardview import BigScoreboardView



# ------------------------- functions, etc. -------------------------
def main():
    

    # configure logging
    logging.basicConfig(level=logging.INFO,
        format=const.logformat,
        )

    # start main controller
    sc = ScoreboardController()


    # start main input controls, which is the Tk
    #   root window; give it to the controller
    siv = ScoreboardInputView(sc)
    sc.addroot(siv)


    # start views; hook to main controller
    # sc.addview(ScoreboardView(siv, const.ViewType.PRIMARY), const.ViewType.PRIMARY)

    # alternate, much bigger text primary view:
    sc.addview(BigScoreboardView(siv, const.ViewType.PRIMARY), const.ViewType.PRIMARY)

    sc.addview(ScoreboardView(siv, const.ViewType.SECONDARY), const.ViewType.SECONDARY)


    # run event loop
    logging.info("starting event loop")
    sc.startpollingdata()
    sc.startpollingtimer()
    siv.mainloop()


# ------------------------- script start -------------------------
if __name__ == '__main__':
    main()

