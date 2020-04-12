# app.py
# Rename the folder from 'GameHost' to 'Controller'

# In-project dependencies
from DataModel.game_state import GameState

# External dependencies
from flask import Flask  # import flask
from flask import request
import json
from flask_cors import CORS, cross_origin
import jsonpickle

app = Flask(__name__)  # create an app instance
CORS(app, resources={r"/*": {"origins": "*"}})
app.config['CORS_HEADERS'] = 'Content-Type'


@app.route("/")  # at the end point /
def hello():  # call method hello
    return "Hello World!"  # which returns "hello world"


@app.route("/newgamedummy")  # at the end point /newgamedummy
def create_new_game_test():

    game_state = GameState()
    game_state.populate_test_values()

    # Use JSON pickle to convert to JSON. Native json module can't handle complex classes.
    json_response = jsonpickle.encode(game_state)
    return json_response


@app.route("/newgame")  # at the end point /newgame
def create_new_game():

    game_state = GameState()

    # Use JSON pickle to convert to JSON. Native json module can't handle complex classes.
    json_response = jsonpickle.encode(game_state)
    return json_response


@app.route("/restart")  # at the end point /restart
def restart():
    game_state = GameState()

    game_state.restart()
    # Use JSON pickle to convert to JSON. Native json module can't handle complex classes.

    return game_state


@app.route("/move", methods=["POST"])  # at the end point /move
def make_move():
    state_dict = request.json
    # Use JSON pickle to convert JSON to Python object. Native json module can't handle complex classes.
    game_state = jsonpickle.decode(json.dumps(state_dict))
    game_state.alter_state()

    # Use JSON pickle to convert to JSON. Native json module can't handle complex classes.
    json_response = jsonpickle.encode(game_state)
    return json_response


if __name__ == "__main__":  # on running python app.py
    app.run(debug=True, host='0.0.0.0')  # run the flask app