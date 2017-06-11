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


    # ----- hardware polling
    def startscorepolling(self):
        logging.info("starting score polling")
        self.root.after(0, self.pollscore)

    def pollscore(self):
        # this is just a request to generate the score; 
        #   the output is read from a different scheduled call

        self.targetcommand(self.targets.values(), const.Commands.SCORE)
        
        # check if you should stop (?)

        self.root.after(const.hwscorepollinterval, self.pollscore)

    def startoutputpolling(self):
        logging.info("starting output polling")
        self.root.after(0, self.polloutput)

    def polloutput(self):
        # look for any output and parse whatever you get

        for target in self.targets.values():
            # line = str(self.device.readline().rstrip(),"utf-8")
            line = target.read()
            line2 = ""

            # parse; I believe we can dispatch neatly on the first
            #   character, unless I'm missing something:
            if line:
                signature = line[0]
                if signature == 'N':
                    # return to neutral: currently do nothing
                    pass
                elif signature == 'H':
                    # hit: currently do nothing
                    pass
                elif signature == 'B' or signature == 'R':
                    # first line of two line score; get second line
                    #   and report it
                    line2 = str(self.device.readline().rstrip(),"utf-8")
                     # parse and report score
                     # hmm, looks like we'll be reporting scores up 
                     #  to the controller per target and do the summing
                     #  up there


                else:
                    # who knows, ignore it
                    pass

            # testing: log everything
            logging.info("{} output: {}".format(target.name, line))
            if line2:
                logging.info("{} output2: {}".format(target.name, line2))

        # check if you should stop (?)

        self.root.after(const.hwoutputpollinterval, self.polloutput)















