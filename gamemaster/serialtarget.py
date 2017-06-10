"""

serialtarget.py

controls the target via serial interface

basic interface is:
Monitor communications:
TX:
  NEUTRAL,<LEFT/RIGHT>                   --> when going to default (green)
  HIT,<RED/BLUE,<LEFT/RIGHT>             --> when getting 1st or 2nd hit
  <RED/BLUE>:#1st hits,#2nd hits,#final  --> upon receiving 'SCORE' command
RX:
  START          --> starts the game
  STOP           --> stops the game
  SCORE          --> sends total hit counts
  TEST_RED       --> sets both sides to red
  TEST_BLUE      --> sets both sides to blue
  TEST_GREEN     --> sets both sides to green
  TEST_RED_BLUE  --> sets one side to red, one side to blue
  RESET          --> reset target (ready to receive 'START')
  HELP           --> list of commands
"""

# ------------------------- imports -------------------------
# std lib
import logging
import os

# third party
import serial

# local
from shared import constants as const

# ------------------------- constants -------------------------
# remove this prefix from name
portprefix = "tty."

# ------------------------- SerialTarget -------------------------
class SerialTarget:
    """
    control a target via the serial interface

    if you ever do a usb version, factor out the
    common stuff into an interface
    """
    def __init__(self, devicepath, name=None):
        """
        input: string path to serial device (eg, /dev/tty/whatver)
        """

        self.devicepath = devicepath
        self.device = None

        if name is None:
            self.name = os.path.basename(self.devicepath)
            self.name.replace(portprefix, "")
        else:
            self.name = name
        self.open()

    def open(self):
        # magic numbers taken from Cameron's code
        self.device = serial.Serial()
        self.device.baudrate = 115200
        self.device.port = self.devicepath
        self.device.timeout = 0.1
        self.device.write_timeout = 1   
        self.device.open()

    def close(self):
        # apparently this can be None sometimes?
        if self.device is not None:
            self.device.close()
        else:
            logging.info("device {} unexpectedly None".format(self.devicepath))

    def version(self):
        self.device.write(b'VERSION\r\n')
        self.device.flush()
        return str(self.device.readline().rstrip(),"utf-8") 

    def command(self, command):
        """
        perform simple command without output

        input: command enum member
        """
        self.device.write(command.value)
        self.device.flush()

    # I suspect these are all obsolete in favor of command():
    def start(self):
        self.device.write(b'START\r\n')
        self.device.flush()

    def stop(self):
        self.device.write(b'STOP\r\n')
        self.device.flush()

    def reset(self):
        self.device.write(b'RESET\r\n')
        self.device.flush()

    def testred(self):
        self.device.write(b'TEST_RED\r\n')
        self.device.flush()

    def testblue(self):
        self.device.write(b'TEST_BLUE\r\n')
        self.device.flush()

    def testgreen(self):
        self.device.write(b'TEST_GREEN\r\n')
        self.device.flush()

    def testredblue(self):
        self.device.write(b'TEST_RED_BLUE\r\n')
        self.device.flush()

    # untested: I suspect this isn't parsing right
    #   see format above
    def score(self):
        self.device.write(b'SCORE\r\n')
        redscore = str(self.device.readline().rstrip(),"utf-8")
        bluescore = str(self.device.readline().rstrip(),"utf-8")
        return redscore, bluescore

    # other transmit calls not done















