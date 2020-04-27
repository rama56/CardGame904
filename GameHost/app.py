# app.py
# Rename the folder from 'GameHost' to 'Controller'

# In-project dependencies
from DataModel.game_state import GameState
from GameHost import session_helper

# External dependencies
from flask import Flask, request, session
from datetime import timedelta
import json
import os
from flask_cors import CORS, cross_origin
import jsonpickle

app = Flask(__name__)  # create an app instance
CORS(app, resources={r"/*": {"origins": "*"}})
app.config['CORS_HEADERS'] = 'Content-Type'
app.config['SESSION_PERMANENT'] = True
app.config['SESSION_TYPE'] = 'filesystem'
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=1200)
app.secret_key = os.urandom(16)

@app.route("/")  # at the end point /
def hello():  # call method hello
    return "Hello World!"  # which returns "hello world"


@app.route("/newgamedummy")  # at the end point /newgamedummy
@cross_origin(origin='*', headers=['Content-Type', 'Authorization'])
def create_new_game_test():

    game_state = GameState()
    game_state.populate_test_values()
    # Use JSON pickle to convert to JSON. Native json module can't handle complex classes.
    json_response = jsonpickle.encode(game_state)
    return json_response


@app.route("/newgame")  # at the end point /newgame
@cross_origin(supports_credentials=True)
def create_new_game():

    game_state = GameState()

    # Trim beliefs, save original.
    beliefs_json = session_helper.save_belief(game_state)
    session['beliefs'] = [beliefs_json]

    # Use JSON pickle to convert to JSON. Native json module can't handle complex classes.
    json_response = jsonpickle.encode(game_state)
    session['history'] = [jsonpickle.encode(game_state)]
    return json_response


@app.route("/restart")  # at the end point /restart
@cross_origin(supports_credentials=True)
def restart():
    if 'history' in session.keys() and len(session['history']) > 0:
        game_state = session.history[0]

        session.history = [session.history[0]]
        session.beliefs = [session.beliefs[0]]
        return jsonpickle.encode(game_state)
    # Use JSON pickle to convert to JSON. Native json module can't handle complex classes.
    return ""


@app.route("/undo")
@cross_origin(supports_credentials=True)
def undo():
    if ('history' not in session.keys()) or (len(session['history']) == 0):
        return ""
    if len(session['history']) <= 1:
        return session['history'][0]
    # Delete the latest state
    session['history'] = session['history'][:-1]
    session['beliefs'] = session['beliefs'][:-1]

    session.modified = True
    # Return the current latest state
    return session['history'][-1]


@app.route("/askcomp", methods=["POST"])
@cross_origin(support_credentials=True)
def ask_computer():
    # Use JSON pickle to convert JSON to Python object. Native json module can't handle complex classes.
    game_state = jsonpickle.decode(json.dumps(request.json))

    # Re-attach beliefs from session.
    beliefs_json = session['beliefs'][-1]
    session_helper.reattach_belief(game_state, beliefs_json)

    game_state.ask_player_engine()
    game_state.alter_state()

    # Trim beliefs, save original to session.
    beliefs_json = session_helper.save_belief(game_state)
    session['beliefs'] = [beliefs_json]

    # Use JSON pickle to convert to JSON. Native json module can't handle complex classes.
    json_response = jsonpickle.encode(game_state)
    session['history'].append(json_response)
    session.modified = True

    return json_response


@app.route("/move", methods=["POST"])  # at the end point /move
@cross_origin(origin='*', headers=['Content-Type', 'Authorization'])
@cross_origin(supports_credentials=True)
def make_move():
    # Use JSON pickle to convert JSON to Python object. Native json module can't handle complex classes.
    game_state = jsonpickle.decode(json.dumps(request.json))

    # Re-attach beliefs from session.
    x = session['history'][-1]
    beliefs_json = session['beliefs'][-1]
    session_helper.reattach_belief(game_state, beliefs_json)

    game_state.alter_state()

    # Trim beliefs, save original to session.
    beliefs_json = session_helper.save_belief(game_state)
    session['beliefs'] = [beliefs_json]

    # Use JSON pickle to convert to JSON. Native json module can't handle complex classes.
    json_response = jsonpickle.encode(game_state)
    session['history'].append(json_response)
    session.modified = True

    return json_response


if __name__ == "__main__":  # on running python app.py
    app.run(debug=True, host='0.0.0.0')  #run the flask app