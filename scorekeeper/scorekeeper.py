"""

scorekeeper.py

service that keeps score and makes it available for display


"""

# ------------------------- imports -------------------------

from flask import Flask, request
from flask_restplus import Resource, Api

from shared import constants as sharedconst


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
gamestate = sharedconst.GameState.UNKNOWN

@api.route("/memo/<string:memoname>")
class SimpleMemo(Resource):
    def get(self, memoname):
        return {memoname: memos[memoname]}

    def put(self, memoname):
        memos[memoname] = request.form["data"]
        return {memoname: memos[memoname]}

@api.route("/state")
class SimpleMemo(Resource):
    def get(self):
        return {"state": gamestate.value}

def main():
    app.run(debug=True)

# ------------------------- script starts here -------------------------
if __name__ == '__main__':
    main()