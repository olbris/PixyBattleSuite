"""

gamemaster.py

this GUI application does provides an interface with the arena hardware, 
and provides a UI through which the user controls the PixyBattle game;
I decided to fuse them rather than separate them because hardware can 
be a pain to debug, and it'll be easier without adding an extra layer
of separation between the hardware and its control; also, there is
never any intent to have more than one controller for the hardware,
so there's no pressing need to separate them; contrast the scoreboard,
which could conceivably be one of several clients monitoring the score
feed from the scorekeeper (which is why they are separated)

"""

# ------------------------- imports -------------------------
# std lib
import logging


# local
from shared import constants as const
from gamemaster.gamecontroller import GameController
from gamemaster.gamemasterview import GamemasterView
from gamemaster.scorerecorder import ScoreRecorder


# ------------------------- functions, etc. -------------------------
def main():
    

    # configure logging
    logging.basicConfig(level=logging.INFO,
        format=const.logformat,
        )



    # start main controller
    gc = GameController()

    # start hw controller; hook to main controller

    # start score reporter; hook to main controller
    sr = ScoreRecorder()
    gc.addchangelistener(sr)

    # start view (ie, set up UI); hook to main controller
    gmv = GamemasterView(gc)
    gc.addchangelistener(gmv)


    # run event loop
    logging.info("starting event loop")
    gmv.mainloop()


# ------------------------- script start -------------------------
if __name__ == '__main__':
    main()

