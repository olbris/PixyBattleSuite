"""

arenacontroller.py

this is the hardware interface 

"""

# ------------------------- imports -------------------------
# std lib
import logging

# local
from shared import constants as const


# ------------------------- constants -------------------------


# ------------------------- ArenaController -------------------------
class ArenaController:
    def __init__(self, gamecontroller):
        self.gamecontroller = gamecontroller

        self.pendingcommand = None


    # ----- setup stuff
    def addroot(self, root):
        # tk root, so we can use event loop
        self.root = root


    # ----- communication loop stuff
    def starthardwareloop(self):
        self.root.after(const.hwpollinterval, self.pollhardware)

    def pollhardware(self):
        
        # send commands, then clear pending command
        if self.pendingcommand is not None:
            # send

            # clear
            self.pendingcommand = None

        # log

        # read score

        # log

        # send score updates to gamecontroller
        
        
        # check if you should stop (?)

        self.root.after(const.hwpollinterval, self.pollhardware)





    # ----- game commands
    def start(self):

        # self.pendingcommand = "start"
        pass

    def stop(self):

        # self.pendingcommand = "stop"
        pass




