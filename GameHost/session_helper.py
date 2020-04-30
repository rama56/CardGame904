import jsonpickle

from flask import session
from DataModel.game_state import *


# Save the belief to session, and trim the belief in the original object to something printable.
def save_belief(game_state):
    # Save beliefs to session.
    # game_state = GameState()
    beliefs = [p.belief for p in game_state.players]
    belief_json = jsonpickle.encode(beliefs)
    # session['belief'].append(belief_json)

    # Trim beliefs to make it displayable.
    for p in game_state.players:
        belief = p.belief
        belief.ux_printable.set_printable_hands_belief(belief.nature_hands)
        belief.ux_printable.set_printable_cards_belief(belief.nature_cards)

        belief.private_interim = None
        belief.common_prior = None
        belief.impossible = None
        belief.cards_per_hand = None
        belief.nature_cards = None
        belief.nature_hands = None
        belief._all_cards = None
        belief._significant_cards = None
        # end for
    # end for

    return belief_json
# end function


def reattach_belief(game_state, beliefs_json):
    beliefs = jsonpickle.decode(beliefs_json)
    for i in range(4):
        p = game_state.players[i]
        p.belief = beliefs[i]
