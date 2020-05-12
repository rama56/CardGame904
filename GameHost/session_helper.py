import jsonpickle
import pandas as pd
from flask import session
from DataModel.game_state import *
from io import StringIO


# Save the belief to session, and trim the belief in the original object to something printable.
def save_belief(game_state):
    # Save beliefs to session.
    # game_state = GameState()
    beliefs = [p.belief for p in game_state.players]

    # session['belief'].append(belief_json)

    # Trim beliefs to make it displayable.
    for p in game_state.players:
        belief = p.belief
        belief.ux_printable.set_printable_hands_belief(belief.nature_hands)
        belief.ux_printable.set_printable_cards_belief(belief.nature_cards)

        for i in range(len(belief.nature_hands)):
            x = belief.nature_hands[i]
            y = x.to_csv(index=False, header=False)
            belief.nature_hands[i] = y
        # end for
    # end for

    belief_json = jsonpickle.encode(beliefs)

    for p in game_state.players:
        # belief.private_interim = None
        # belief.common_prior = None
        # belief.impossible = None
        belief.bid_strength = None
        belief.cards_per_hand = None
        belief.nature_cards = None
        belief._all_cards_still_out = None
        # belief._significant_cards = None
        p.belief.nature_hands = None

    ck = game_state.common_knowledge
    ck_json = jsonpickle.encode(ck)

    game_state.common_knowledge = None

    return belief_json, ck_json
# end function


def reattach_belief(game_state, beliefs_json, ck_json):
    beliefs = jsonpickle.decode(beliefs_json)
    for i in range(4):
        p = game_state.players[i]
        p.belief = beliefs[i]
        for j in range(len(p.belief.nature_hands)):
            y = p.belief.nature_hands[j]
            x = pd.read_csv(StringIO(y), names=['CardSet', 'Probability', 'Strength', 'TrumpCandidate'],
                            dtype={'CardSet': object, 'Probability': float, 'Strength': float, 'TrumpCandidate': int})
            p.belief.nature_hands[j] = x

    ck = jsonpickle.decode(ck_json)
    game_state.common_knowledge = ck

