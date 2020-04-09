# app.py
# Rename the folder from 'GameHost' to 'Controller'

# In-project dependencies
from DataModel.GameState import GameState

# External dependencies
from flask import Flask  # import flask
import jsonpickle

app = Flask(__name__)  # create an app instance


@app.route("/")  # at the end point /
def hello():  # call method hello
    return "Hello World!"  # which returns "hello world"


@app.route("/newgame")  # at the end point /newgame
def create_new_game():

    game_state = GameState()

    # Use JSON pickle to convert to JSON. Native json module can't handle complex classes.
    json_response = jsonpickle.encode(game_state)
    return json_response


@app.route("/restart")  # at the end point /restart
def restart(game_state):
    game_state = GameState()

    game_state.restart()
    # Use JSON pickle to convert to JSON. Native json module can't handle complex classes.

    return game_state


@app.route("/move/<gameState>")  # at the end point /move
def make_move(request):

    # Use JSON pickle to convert JSON to Python object. Native json module can't handle complex classes.
    game_state = jsonpickle.decode(request)

    game_state.alter_state()

    # Use JSON pickle to convert to JSON. Native json module can't handle complex classes.
    json_response = jsonpickle.encode(game_state)
    return json_response


if __name__ == "__main__":  # on running python app.py
    app.run(debug=True)  # run the flask app