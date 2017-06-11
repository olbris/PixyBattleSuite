# PixyBattleSuite

This suite of programs run the Pixy Battle game and scoreboard.

The "gamemaster" runs the game and talks to the hardware.

The "scorekeeper" is a REST service.  It receives score data and game metadata from the game master and stores it.

The "scoreboard" reads score and game data from the scorekeeper service and displays it for the game officials and audience in separate displays.

## Requirements

* Anaconda Python distribution 3.5
* flask-restplus
* PySerial


## Running

In three separate terminals, cd into the directory containing the pixybattlesuite package.  Run:

* first: python pixybattlesuite/scripts/startscorekeeper.py
* second: python pixybattlesuite/scripts/startscoreboard.py
* third: python pixybattlesuite/scripts/startgamemaster.py

The scorekeeper should go first; the other two probably don't matter in order.

When the gamemaster is up, click the "Discover" button to find and start up the hardware.
