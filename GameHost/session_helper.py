
import jsonpickle
import pandas as pd
import numpy as np
import glob
from flask import session
from DataModel.game_state import *
from io import StringIO
from os import path
import os
import logging

# Dependencies from within project
from GameHost.perf import parallelize_dataframe
from Intelligence import arithmetic, belief_helper
from Intelligence.common_knowledge import precompute_fill_prior_hands

precomputed_strengths = None


def get_printable_beliefs(game_state):
    # Save beliefs to session.
    beliefs = [p.belief for p in game_state.players]

    # Trim beliefs to make it displayable.
    for belief in beliefs:
        belief.ux_printable.set_printable_cards_belief(belief.nature_cards)
        belief.ux_printable.set_printable_hands_belief(belief.nature_hands)

        belief.bid_strength = None
        belief.cards_per_hand = None
        belief.nature_cards = None
        belief._all_cards_still_out = None
        belief.nature_hands = None


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
            cols = ['Probability', 'Strength', 'TrumpCandidate', 'Mask']    # 'CardSet',
            x = x[cols]
            y = x.to_csv(index=True, header=False)
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
            x = pd.read_csv(StringIO(y), names=['CardSet', 'Probability', 'Strength', 'TrumpCandidate', 'Mask'],
                            dtype={'CardSet': object, 'Probability': float, 'Strength': int, 'TrumpCandidate': int,
                                   'Mask': int}).set_index('CardSet')
            p.belief.nature_hands[j] = x

    ck = jsonpickle.decode(ck_json)
    game_state.common_knowledge = ck


def precompute_beliefs():

    # if os.path.exists("local_data.csv"):
    #     os.remove("local_data.csv")

    if path.exists('local_data.csv'):
        return

    _index = 32
    _taken_cards = []
    _all_card_sets = []

    precompute_fill_prior_hands(_taken_cards, _index, _all_card_sets, 0)

    _all_card_sets_nparr = np.array(_all_card_sets)

    individual_prior = pd.DataFrame(_all_card_sets_nparr, columns=['CardSet', 'Mask'])

    individual_prior_store = parallelize_dataframe(individual_prior, belief_helper.fill_strength_and_trump_choice)

    individual_prior_store.to_csv('local_data.csv', index=False, header=False)

    cwd = os.getcwd()
    logging.info('Folder path of precomputed data. ' + cwd)

    # # File will have only Cardset, Strength, and TrumpCandidate. Not Probability.
    # prob = arithmetic.choose_prob(24, 8)
    # individual_prior['Probability'] = prob


def join_for_belief_scores(individual_prior):
    # precomputed_strengths = pd.read_csv('local_data.csv', names=['CardSet', 'Strength', 'TrumpCandidate'],
    #                                     dtype={'CardSet': str, 'Strength': int, 'TrumpCandidate': int})

    global precomputed_strengths

    if precomputed_strengths is None:
        data_files = glob.glob('local_data_*')
        precomputed_strengths = pd.concat(pd.read_csv(file, names=['CardSet', 'Strength', 'TrumpCandidate', 'Mask'],
                                                      dtype={'CardSet': str, 'Strength': int, 'TrumpCandidate': int,
                                                             'Mask': int}).set_index('CardSet') for file in data_files)

    card_set = individual_prior['CardSet'].values
    return precomputed_strengths.loc[card_set, :]
    # Join with individual_prior based on Cardset.

    # joined = individual_prior.set_index('CardSet').join(precomputed_strengths, how='left', on='CardSet')

    # return joined


def filter_cardsets_out(_card_ids_in_hand_mask):
    logging.info('session_helper - Inside filter_cardsets_out')

    global precomputed_strengths

    if precomputed_strengths is None:
        logging.info('session_helper - Inside if block')

        data_files = glob.glob('local_data_1*')
        logging.info('session_helper - after glob.glob')

        precomputed_strengths = pd.concat(pd.read_csv(file, names=['CardSet', 'Strength', 'TrumpCandidate', 'Mask'],
                                            dtype={'CardSet': str, 'Strength': int, 'TrumpCandidate': int,
                                                   'Mask': int}).set_index('CardSet') for file in data_files)

        logging.info('session_helper - finished reading the data files')

    logging.info('session_helper - outside if')

    flag = np.bitwise_and(precomputed_strengths['Mask'], _card_ids_in_hand_mask)

    filtered = precomputed_strengths[flag == 0]
    prob = arithmetic.choose_prob(24, 8)
    filtered['Probability'] = prob

    return filtered


