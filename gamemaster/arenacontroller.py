"""

arenacontroller.py

this is the hardware interface 

"""

# ------------------------- imports -------------------------
# std lib
import glob
import logging

# third party
import serial

# local
from shared import constants as const
from gamemaster.serialtarget import SerialTarget


# ------------------------- constants -------------------------

# targets seem to all contain this string:
#   (I'm hoping USB hubs don't!)
devicesignature = "usbmodem"

# use this to give targets nicer names; maps device name to
#   nice name; I'm assuming the device name is unique and unchanging
targetnames = {
    "/dev/tty.usbmodem2936451": "target 6",
    "/dev/tty.usbmodem2937361": "target 3",
    
}


# ------------------------- ArenaController -------------------------
class ArenaController:
    def __init__(self, gamecontroller):
        self.gamecontroller = gamecontroller

        self.targets = {}

        self.pendingcommand = None


    # ----- setup stuff
    def addroot(self, root):
        # tk root, so we can use event loop
        self.root = root


    # ----- startup
    def requestdiscover(self):
        # do this asynchronously
        self.root.after(0, self.discover)

    def discover(self):
        """
        find and setup the serial devices
        """

        # close any existing ports and start from scratch
        for target in self.targets.values():
            target.close()
        self.targets.clear()

        devicepaths = [d for d in glob.glob("/dev/tty.*") 
            if devicesignature in d]

        for devicepath in devicepaths:
            try:
                target = SerialTarget(devicepath)
                self.targets[devicepath] = target
                if devicepath in targetnames:
                    self.targets[devicepath].name = targetnames[devicepath]
            except (OSError, serial.SerialException):
                pass

        # send notification
        # return list of (devicepath, nice name)
        found = [(t.name, t.devicepath) for t in self.targets.values()]

        logging.info("discovered {} targets".format(len(found)))

        # send it off...
        self.gamecontroller.targetsdiscovered(found)

    def closealltargets(self):
        # synchronous, called on quit (I don't think it's needed,
        #   but let's try to be neat)
        for target in self.targets.values():
            target.close()

    # ----- async commands
    def requesttargetcommand(self, targetlist, command):
        self.root.after(0, self.targetcommand, targetlist, command)

    def targetcommand(self, targetlist, command):
        for targetpath in targetlist:
            logging.info("sending command {} to {}".format(command.name, targetpath))
            self.targets[targetpath].command(command)


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









