"""

scorestream.py

simple script to poll a REST interface and report results, for testing

"""


# ------------------------- imports -------------------------
# std lib
import argparse
import logging
import sys
import time


# third party
import requests

# local
from shared import constants as const




def main():
    # just a dumb loop that hits the scorekeeper over and over
    parser = argparse.ArgumentParser(description='report data from scorekeeper')
    parser.add_argument("interval", help="print interval (s)",
        type=int, default=3)
    args = parser.parse_args()

    # configure logging
    logging.basicConfig(level=logging.INFO,
        format=const.logformat,
        )

    # test connection here, using "hello" endpoint
    try:
        r = requests.get("{}/hello".format(const.apiurl))
    except requests.exceptions.ConnectionError:
        logging.exception("cannot connect to {}; quitting".format(const.apiurl))
        sys.exit()

    while True:
        
        url = "{}/{}".format(const.apiurl, "state")
        r = requests.get(url)
        if r.status_code != 200:
            message = "error: status code {}".format(r.status_code)
        else:
            message = "game state: {}".format(r.json())
        logging.info("{}: {}".format(time.asctime(), message))

        time.sleep(args.interval)




if __name__ == '__main__':
    main()
