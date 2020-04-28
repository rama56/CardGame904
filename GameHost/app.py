# app.py
# Rename the folder from 'GameHost' to 'Controller'

# In-project dependencies
from flask import g
from GameHost.session_manager import add_to_beliefs, add_to_history, get_beliefs, get_history, reset_beliefs, \
    reset_history, pop_beliefs, pop_history
from DataModel.game_state import GameState
from GameHost import session_helper

# External dependencies
from flask import Flask, request
import json
import os
from flask_cors import CORS
import jsonpickle

app = Flask(__name__)  # create an app instance
CORS(app, resources={r"/*": {"origins": '*'}})
app.config['CORS_HEADERS'] = 'Content-Type'
app.secret_key = os.urandom(4)


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
    reset_history()
    game_state = GameState()
    # Trim beliefs, save original.
    beliefs_json = session_helper.save_belief(game_state)
    add_to_beliefs(beliefs_json)

    # Use JSON pickle to convert to JSON. Native json module can't handle complex classes.
    json_response = jsonpickle.encode(game_state)
    add_to_history(json_response)
    return json_response


@app.route("/restart")  # at the end point /restart
def restart():
    history = get_history()
    beliefs = get_beliefs()
    if history:
        game_state = history[0]
        reset_history()
        add_to_history([history[0]])
    else:
        game_state = GameState()
    reset_beliefs()
    add_to_beliefs(beliefs[0])
    return jsonpickle.encode(game_state)


@app.route("/undo")
def undo():
    history = get_history()
    pop_beliefs()

    if history and len(history) <= 1:
        return history[0]
    # Delete the latest state
    pop_history()

    # Return the current latest state
    return get_history()[-1]


# @app.route("/askcomp", methods=["POST"])
# def ask_computer():
#     # Use JSON pickle to convert JSON to Python object. Native json module can't handle complex classes.
#     game_state = jsonpickle.decode(json.dumps(request.json))
#
#     # Re-attach beliefs from session.
#     beliefs_json = session['beliefs'][-1]
#     session_helper.reattach_belief(game_state, beliefs_json)
#
#     game_state.ask_player_engine()
#     game_state.alter_state()
#
#     # Trim beliefs, save original to session.
#     beliefs_json = session_helper.save_belief(game_state)
#     session['beliefs'] = [beliefs_json]
#
#     # Use JSON pickle to convert to JSON. Native json module can't handle complex classes.
#     json_response = jsonpickle.encode(game_state)
#     session['history'].append(json_response)
#     session.modified = True
#
#     return json_response


@app.route("/move", methods=["POST"])  # at the end point /move
def make_move():
    # Use JSON pickle to convert JSON to Python object. Native json module can't handle complex classes.
    game_state = jsonpickle.decode(json.dumps(request.json))

    # Re-attach beliefs from session.
    beliefs = get_beliefs()
    if beliefs:
        beliefs_json = beliefs[-1]
        session_helper.reattach_belief(game_state, beliefs_json)

    game_state.alter_state()

    if beliefs:
        # Trim beliefs, save original to session.
        beliefs_json = session_helper.save_belief(game_state)
        add_to_beliefs(beliefs_json)

    # Use JSON pickle to convert to JSON. Native json module can't handle complex classes.
    json_response = jsonpickle.encode(game_state)
    add_to_history(json_response)

    return json_response


if __name__ == "__main__":  # on running python app.py
    app.run(debug=True, host='0.0.0.0')  # run the flask app
