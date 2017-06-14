"""

scorekeeper.py

service that keeps score and makes it available for display


"""

# ------------------------- imports -------------------------
# stdlib
import time

# flask
from flask import Flask, request
from flask_restplus import Resource, Api

# local
from shared import constants as const


# ------------------------- data store -------------------------
# we're just holding the data in module level variables

# game metadata (?)
metadata = {
    const.TeamColors.RED: 0,
    const.TeamColors.BLUE: 0,    
}

# ------------------------- data store -------------------------
# data is entirely transient; just store in-memory
#   in module variables 

# game metadata
gamemetadata = {
    "time": time.time(),
    "red": 0,
    "blue": 0,
}



gamestate = const.GameState.UNKNOWN


# ------------------------- server -------------------------
# app creation; would you normally put this in a function?
app = Flask(__name__)
api = Api(app)


# test endpoint
@api.route("/hello")
class HelloWorld(Resource):
    def get(self):
        return {"hello": "world"}


@api.route("/state")
class GameState(Resource):
    def get(self):
        return {"state": gamestate.value}

    def post(self):
        """
        expects: {"state": "idle" (etc)}
        """
        data = request.get_json()
        global gamestate
        gamestate = const.GameState(data["state"])
        return {"state": gamestate.value}

@api.route("/gamemetadata")
class GameData(Resource):
    def get(self):
        return gamemetadata

    def put(self):
        gamemetadata.update(request.get_json())
        gamemetadata["time"] = time.time()

        return gamemetadata


def main():
    app.run(debug=True)

# ------------------------- script starts here -------------------------
if __name__ == '__main__':
    main()




