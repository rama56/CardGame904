# app.py
# Rename the folder from 'GameHost' to 'Controller'

# In-project dependencies
import copy

from flask import g
from GameHost.session_manager import reset_history_new, add_to_new_history, \
    peek_history_new, pop_history_new, get_first_of_history
from DataModel.game_state import GameState
from GameHost import session_helper

# External dependencies
from flask import Flask, request
import json
import os
from flask_cors import CORS
import jsonpickle
from timeit import default_timer as timer

import logging
logging.getLogger().setLevel(logging.DEBUG)

app = Flask(__name__)  # create an app instance
CORS(app, resources={r"/*": {"origins": '*'}})
app.config['CORS_HEADERS'] = 'Content-Type'
app.secret_key = os.urandom(4)


@app.route("/")  # at the end point /
def hello():  # call method hello
    return "Hello World!"  # which returns "hello world"



@app.route("/newgame")  # at the end point /newgame
def create_new_game():
    with open('helloworld.txt', 'r') as file:
        logging.info('File contents: {}'.format(file.read()))
    start = timer()
    reset_history_new()
    end = timer()
    elapsed = end - start
    logging.info('Reset history/beliefs. Time elapsed = ' + str(elapsed))

    start = timer()
    game_state = GameState()
    end = timer()
    elapsed = end - start
    logging.info('Created GameState object. Time elapsed = ' + str(elapsed))

    # Save History, retain a live object,
    start = timer()
    game_state_for_history = copy.deepcopy(game_state)
    add_to_new_history(game_state_for_history)
    end = timer()
    elapsed = end - start
    logging.info('Saved GameState object to history. Time elapsed = ' + str(elapsed))

    # trim a copy and jsonify it to send to client.
    # Use JSON pickle to convert to JSON. Native json module can't handle complex classes.

    start = timer()
    session_helper.get_printable_beliefs(game_state)
    json_response = jsonpickle.encode(game_state)
    end = timer()
    elapsed = end - start
    logging.info('Trimmed belief. Converted to JSON for return to client. Time elapsed = ' + str(elapsed))

    return json_response


@app.route("/restart")  # at the end point /restart
def restart():

    start = timer()

    initial_state = get_first_of_history()
    reset_history_new()

    state_to_return = None

    if initial_state is not None:
        state_to_return = initial_state
    else:
        new_game_state = GameState()
        state_to_return = new_game_state

    game_state_for_history = copy.deepcopy(state_to_return)
    add_to_new_history(game_state_for_history)

    session_helper.get_printable_beliefs(state_to_return)
    json_response = jsonpickle.encode(state_to_return)

    end = timer()
    elapsed = end - start
    logging.info('Restart game completed. Time elapsed = ' + str(elapsed))

    return json_response


@app.route("/undo")
def undo():
    start = timer()

    current_state = pop_history_new()
    previous_state = peek_history_new()

    state_to_return = None

    if previous_state is not None:
        state_to_return = previous_state
    else:
        state_to_return = current_state

    game_state_for_history = copy.deepcopy(state_to_return)
    add_to_new_history(game_state_for_history)

    session_helper.get_printable_beliefs(state_to_return)
    json_response = jsonpickle.encode(state_to_return)

    end = timer()
    elapsed = end - start
    logging.info('Undo completed. Time elapsed = ' + str(elapsed))

    return json_response


@app.route("/askcomp", methods=["POST"])
def ask_computer():
    # Use JSON pickle to convert JSON to Python object. Native json module can't handle complex classes.
    start = timer()
    _game_state_from_client = jsonpickle.decode(json.dumps(request.json))
    end = timer()
    elapsed = end - start
    logging.info('Gamestate decoded from json. Time elapsed = ' + str(elapsed))

    # Fetch gamestate from history and assign the move.
    start = timer()
    game_state_peeked = peek_history_new()
    game_state = copy.deepcopy(game_state_peeked)
    end = timer()
    elapsed = end - start
    logging.info('Get GameState from history and put in move. Time elapsed = ' + str(elapsed))

    start = timer()
    game_state.ask_player_engine()
    end = timer()
    elapsed = end - start
    logging.info('Computer picked it\'s move. Time elapsed = ' + str(elapsed))

    # Alter the state based on move.
    start = timer()
    game_state.alter_state()
    end = timer()
    elapsed = end - start
    logging.info('Altered state. Time elapsed = ' + str(elapsed))

    # Save History, retain a live object,
    start = timer()
    game_state_for_history = copy.deepcopy(game_state)
    add_to_new_history(game_state_for_history)
    end = timer()
    elapsed = end - start
    logging.info('Saved GameState object to history. Time elapsed = ' + str(elapsed))

    # trim a copy and jsonify it to send to client.
    # Use JSON pickle to convert to JSON. Native json module can't handle complex classes.

    start = timer()
    session_helper.get_printable_beliefs(game_state)
    json_response = jsonpickle.encode(game_state)
    end = timer()
    elapsed = end - start
    logging.info('Trimmed belief. Converted to JSON for return to client. Time elapsed = ' + str(elapsed))

    return json_response



@app.route("/move", methods=["POST"])  # at the end point /move
def make_move():
    # Use JSON pickle to convert JSON to Python object. Native json module can't handle complex classes.
    start = timer()
    _game_state_from_client = jsonpickle.decode(json.dumps(request.json))
    end = timer()
    elapsed = end - start
    logging.info('Gamestate decoded from json. Time elapsed = ' + str(elapsed))

    # Fetch gamestate from history and assign the move.
    start = timer()
    game_state_peeked = peek_history_new()
    game_state = copy.deepcopy(game_state_peeked)
    _move = _game_state_from_client.move
    game_state.move = _move
    end = timer()
    elapsed = end - start
    logging.info('Get GameState from history and put in move. Time elapsed = ' + str(elapsed))

    # Alter the state based on move.
    start = timer()
    game_state.alter_state()
    end = timer()
    elapsed = end - start
    logging.info('Altered state. Time elapsed = ' + str(elapsed))

    # Save History, retain a live object,
    start = timer()
    game_state_for_history = copy.deepcopy(game_state)
    add_to_new_history(game_state_for_history)
    end = timer()
    elapsed = end - start
    logging.info('Saved GameState object to history. Time elapsed = ' + str(elapsed))

    # trim a copy and jsonify it to send to client.
    # Use JSON pickle to convert to JSON. Native json module can't handle complex classes.

    start = timer()
    session_helper.get_printable_beliefs(game_state)
    json_response = jsonpickle.encode(game_state)
    end = timer()
    elapsed = end - start
    logging.info('Trimmed belief. Converted to JSON for return to client. Time elapsed = ' + str(elapsed))

    return json_response


if __name__ == "__main__":  # on running python app.py

    # logging.info('Precomputation of beliefs started.')
    # start = timer()
    # session_helper.precompute_beliefs()
    # end = timer()
    # elapsed = end - start
    # logging.info('Precomputation of beliefs completed. Time elapsed = ' + str(elapsed))

    app.run(debug=True, host='0.0.0.0')  # run the flask app
