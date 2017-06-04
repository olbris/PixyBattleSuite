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
from scoreboard.scoreboardview import ScoreboardView, ViewType



# ------------------------- functions, etc. -------------------------
def main():
    

    # configure logging
    logging.basicConfig(level=logging.INFO,
        format=const.logformat,
        )



    # start main controller
    sc = ScoreboardController()

    # start score watcher; hook to main controller


    # start main input controls, which is the Tk
    #   root window
    siv = ScoreboardInputView(sc)


    # start views; hook to main controller (add listeners)
    sv1 = ScoreboardView(siv, ViewType.PUBLIC)
    sv2 = ScoreboardView(siv, ViewType.PRIVATE)

    sc.addchangelistener(sv1)
    sc.addchangelistener(sv2)



    # run event loop
    logging.info("starting event loop")
    siv.mainloop()


# ------------------------- script start -------------------------
if __name__ == '__main__':
    main()

