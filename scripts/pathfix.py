"""

adjust the sys.path so scripts can find our modules

"""

import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(__file__)))

