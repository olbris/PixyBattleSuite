"""

scorekeeper.py

service that keeps score and makes it available for display


"""

# ------------------------- imports -------------------------
# stdlib

# flask
from flask import Flask, request
from flask_restplus import Resource, Api

# local
from shared import constants as const


# app creation; would you normally put this in a function?
app = Flask(__name__)
api = Api(app)


# test endpoint
@api.route("/hello")
class HelloWorld(Resource):
    def get(self):
        return {"hello": "world"}


# probably should make a class to hold state, but
#    for now, global variable:
gamestate = const.GameState.UNKNOWN

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


def main():
    app.run(debug=True)

# ------------------------- script starts here -------------------------
if __name__ == '__main__':
    main()