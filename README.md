# PixyBattleSuite

This suite of programs run the Pixy Battle game and scoreboard.

The "gamemaster" runs the game and talks to the hardware.

The "scorekeeper" is a REST service.  It receives score data and game metadata from the game master and stores it.

The "scoreboard" reads score and game data from the scorekeeper service and displays it for the game officials and audience in separate displays.

## Requirements

The suite was developed and tested on Python 3.5.  I used the Anaconda distribution as my base, but I think the only library in there I used is requests.

Libraries needed:
* requests
* flask-restplus (for the REST service)
* PySerial (for hardware communication)

## Hardware setup

The targets should all be connected to the computer running the gamemaster.  

Technically, the three scripts can be run on three different computers, so long as the API URL is adjusted in the shared/constants.py file. However, the REST service runs in debug mode, has a swagger interface, and probably has other security issues. So it is recommended that all three scripts run on the same computer. I plan to be disconnected from the network when I run. 

## Running the scripts

In three separate terminals, cd into the directory containing the pixybattlesuite package.  Run:

* first the REST service: python scripts/startscorekeeper.py
* second: python scripts/startscoreboard.py
* third: python scripts/startgamemaster.py

The scorekeeper must go first. The other two probably don't matter in order.

## Running the game

The gamemaster UI is meant to guide you through running the game.

**Gamemaster, left side: hardware and testing**
* Everything on the left side is for testing. In normal operation, you don't need it.
** Click "discover" to find all connected targets.  Select the targets you want to send a command to, then click the button.
** Game state changes: *really* shouldn't be messed with. Some game state changes trigger other behaviors, and if you do them out of order, unpredictable things could happen.

**Gamemaster, right side: game controls**

The right-side UI is laid out in the order you will use things in the game.

Setup typically is only done once. Click "discover" to find connected hardware (the list at left will populate). Optionally set game mode to IDLE or TESTING.  It doesn't do anything except change the color indicator.

For each game, follow the steps from top to bottom. The game mode will be indicated in text on the gamemaster UI and by color on the scoreboard.

Note that some non-software reminders are displayed in the text of the UI (eg, reminding the referees to clear their hit counters).

The typical state cycle is: PREPARING - READY - RUNNING - FINISHED - FINAL

* PREPARING = resetting score, setting teams, robots being placed into the ring
* READY = start is imminent, within 10-15s
* RUNNING = timer is running, game is on
* FINISHED = timer has run out; scoring is over
* FINAL = robot hit scores reported and added in; score is final

There is no way to pause the game once started. That would not be easy...

**Logging** 

Everything that goes from the gamemaster to the scorekeeper is logged to a filed in the pixybattlesuite/logs directory.  All three components also send logging information to their terminals.

**Scoreboard**

The scoreboard consists of three windows: a control window, and two views (primary and secondary). The primary view is expected to be on a second display facing the audience.  The control window and secondary view are expected to be on the same screen as the gamemaster. Note that the primary view is a borderless window; use the controls to move it and hide/show it.

You may display a message on the scoreboard using the "set message" feature.

You may toggle a summary of the scoring scheme with the "toggle score key" button. 

There is an alternate primary scoreboard, the BigScoreboardView. It needs to be enabled/disabled by editing scoreboard.py. When it's active, it presents a much larger view, but it only shows the timer, team names, and total score. The top banner, bottom message, and subscores are not shown. As with the other primary view, it is borderless and positioned by the UI. When this view is active, the secondary view is not changed.

## Status

The 2017 event has been run. The software worked very well.

**Issues/feature**

* Score reset bug; when score is reset, it's still being cached somewhere in the gamecontroller, because it returns and is pushed back through to the scoreboard. The score resets correctly at the start of the game, so it's purely cosmetic.
* Moving the primary window: needs +/- 1000 in x (screens are wide); even better, have it remember the last used position and, on button press, restore it. 
* If team names are asymmetric, the team name display area will become uncentered.