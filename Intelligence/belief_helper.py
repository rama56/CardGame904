import ast
import numpy as np
from DataModel.card import eng_id_mapping, value_points_mapping


# HELP 1 - AT THE BEGINNING OF THE GAME, COMPUTE STRENGTHS OF DIFFERENT CARD SETS.
def fill_strength_and_trump_choice(individual_prior):
    individual_prior['CardSetIds'] = individual_prior['CardSet'].apply(get_idlist_from_idstr)

    individual_prior['SpadeIds'] = individual_prior['CardSetIds'].apply(get_suite_bucket, suite_id=0)
    individual_prior['HeartsIds'] = individual_prior['CardSetIds'].apply(get_suite_bucket, suite_id=1)
    individual_prior['DiceIds'] = individual_prior['CardSetIds'].apply(get_suite_bucket, suite_id=2)
    individual_prior['CloverIds'] = individual_prior['CardSetIds'].apply(get_suite_bucket, suite_id=3)

    individual_prior['SpadePoints'] = individual_prior['SpadeIds'].apply(get_points)
    individual_prior['HeartsPoints'] = individual_prior['HeartsIds'].apply(get_points)
    individual_prior['DicePoints'] = individual_prior['DiceIds'].apply(get_points)
    individual_prior['CloverPoints'] = individual_prior['CloverIds'].apply(get_points)

    individual_prior['SpadeStrengthSum'] = individual_prior['SpadePoints'].apply(get_strength_sum,
                                                                                 f=[-1, 3, 2.5, 1.8, 1.5, 1.5, 1.5,
                                                                                    1.2])
    individual_prior['HeartsStrengthSum'] = individual_prior['HeartsPoints'].apply(get_strength_sum,
                                                                                   f=[-1, 3, 2.5, 1.8, 1.5, 1.5, 1.5,
                                                                                      1.2])
    individual_prior['DiceStrengthSum'] = individual_prior['DicePoints'].apply(get_strength_sum,
                                                                               f=[-1, 3, 2.5, 1.8, 1.5, 1.5, 1.5, 1.2])
    individual_prior['CloverStrengthSum'] = individual_prior['CloverPoints'].apply(get_strength_sum,
                                                                                   f=[-1, 3, 2.5, 1.8, 1.5, 1.5, 1.5,
                                                                                      1.2])

    individual_prior['SpadeLen'] = individual_prior['SpadePoints'].apply(get_length)
    individual_prior['HeartsLen'] = individual_prior['HeartsPoints'].apply(get_length)
    individual_prior['DiceLen'] = individual_prior['DicePoints'].apply(get_length)
    individual_prior['CloverLen'] = individual_prior['CloverPoints'].apply(get_length)

    individual_prior['SpadeStrength'] = individual_prior['SpadeStrengthSum'] / individual_prior['SpadeLen']
    individual_prior['HeartsStrength'] = individual_prior['HeartsStrengthSum'] / individual_prior['HeartsLen']
    individual_prior['DiceStrength'] = individual_prior['DiceStrengthSum'] / individual_prior['DiceLen']
    individual_prior['CloverStrength'] = individual_prior['CloverStrengthSum'] / individual_prior['CloverLen']

    individual_prior['SpadeStrength'].fillna(0, inplace=True)
    individual_prior['HeartsStrength'].fillna(0, inplace=True)
    individual_prior['DiceStrength'].fillna(0, inplace=True)
    individual_prior['CloverStrength'].fillna(0, inplace=True)

    individual_prior['Strength'] = individual_prior['SpadeStrength'] + individual_prior['HeartsStrength'] + \
                                   individual_prior['DiceStrength'] + individual_prior['CloverStrength']

    individual_prior['Strength'] = individual_prior['Strength'].apply(np.round)
    individual_prior_for_trump = individual_prior[['SpadeStrength', 'HeartsStrength', 'DiceStrength',
                                                   'CloverStrength']]

    individual_prior_for_trump.rename(
        columns={'SpadeStrength': 0, 'HeartsStrength': 1, 'DiceStrength': 2, 'CloverStrength': 3}, inplace=True)

    individual_prior['TrumpCandidate'] = individual_prior_for_trump.idxmax(axis=1)

    individual_prior_store = individual_prior[['CardSet', 'Probability', 'Strength', 'TrumpCandidate']]

    return individual_prior_store

# ATTEMPTING TO MAKE THE BELOW FUNCTIONS GRANULAR IN A HOPE THAT DATA-FRAME APPLY RUNS QUICKLY THAN THIS.


def get_list_from_engs(cardset):
    return ast.literal_eval(cardset)


def get_idlist_from_idstr(cardset):
    return ast.literal_eval(cardset)


def get_ids_from_list(cardset_list):
    return [eng_id_mapping[x] for x in cardset_list]


def get_suite_bucket(card_ids, suite_id=0):
    return [x for x in card_ids if (x - 1) // 8 == suite_id]


def get_points(card_ids):
    return [value_points_mapping[(x-1) % 8 + 1] for x in card_ids]


def get_length(suit_points):
    return len(suit_points)


def sort_points(suit_points):
    return suit_points.sort(reverse=True)


def get_strength_sum(suit_points, f):
    same_suite_count = 0
    s = 0
    for c in suit_points:
        s = s * f[same_suite_count] + c  # s = s + (1 + same_suite_count * 2) * c.points
        same_suite_count = same_suite_count + 1

    return s


# HELP 2 - CHECK IF A CARDSET HAS A PARTICULAR CARD
def get_has_card_id_flag(card_set_distribution, card_id):
    card_set_distribution_dupe = card_set_distribution['CardSet'].apply(get_idlist_from_idstr)
    flag = card_set_distribution_dupe.apply(contains_card_id, args=(card_id,))
    return flag


def contains_card_id(cardset_list, card_id):
    return card_id in cardset_list


# HELP 3 - REMOVE A CARD FROM A CARDSET
def get_card_id_removed_from_cardset(cardset_strings, card_id):
    return cardset_strings.apply(remove_card_from_cardset, args=(card_id,))


# ENG_TO_ID
def remove_card_from_cardset(cardset, card_id):
    card_list = ast.literal_eval(cardset)
    card_list.remove(card_id)
    return str(card_list)