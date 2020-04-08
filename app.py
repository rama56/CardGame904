# app.py

# In-project dependencies
from GameState import GameState

# External dependencies
from flask import Flask  # import flask
import jsonpickle

app = Flask(__name__)  # create an app instance


@app.route("/")  # at the end point /
def hello():  # call method hello
    return "Hello World!"  # which returns "hello world"

@app.route("/newgame")  # at the end point /newgame
def createNewGame():

    game_state = GameState()

    # Use JSON pickle to convert to JSON. Native json module can't handle complex classes.
    json_response = jsonpickle.encode(game_state)
    return json_response

@app.route("/restart")  # at the end point /restart
def restart(gameState):
    game_state = GameState()

    gameState.restart()
    # Use JSON pickle to convert to JSON. Native json module can't handle complex classes.

    return game_state


@app.route("/move")  # at the end point /move
def makeMove(gameState, somethingSpecifyingMoveMade):

    # Use JSON pickle to convert JSON to Python object. Native json module can't handle complex classes.
    game_state = GameState(gameState)
    game_state.move(somethingSpecifyingMoveMade)

    # Use JSON pickle to convert to JSON. Native json module can't handle complex classes.

    return game_state


if __name__ == "__main__":  # on running python app.py
    app.run(debug=True)  # run the flask app