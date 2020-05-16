from DataModel.card import get_significant_cards, get_deck
from Intelligence import arithmetic

import pandas as pd
import copy


class CommonKnowledge:

    # (EVERYONE KNOWS THAT)^inf EVERYONE KNOWS THE INFORMATION OF THIS CLASS OBJECT.

    def __init__(self):
        # Distribution of the hand's card set.
        self.nature_hands = {}  # TODO: [{}, {}, {}, {}] will still be required when learning from bids happen.

        # For each card, chance of it being in different hands.
        self.nature_cards = {}
        self.cards_per_hand = 8

        self._all_cards_still_out = []

    def set_common_prior(self):
        # At the beginning, the common prior is the uniform belief about the nature for any player,

        # Computing common prior of nature_hands
        _all_cards = get_deck()  # _significant_cards = get_significant_cards() get_deck()

        # COMMON PRIOR IS TOO EXPENSIVE - 1.05 X 10^7 ROWS.
        # _all_card_sets = []
        # fill_prior_hands([], _all_cards, 0, _all_card_sets)
        # self.nature_hands = pd.DataFrame(_all_card_sets, columns=['CardSet'])

        # prob = arithmetic.choose_prob(32, 8)
        # self.nature_hands['Probability'] = prob

        # TODO: Set strengths also here?

        # Common prior of cards still out there in the hands
        self._all_cards_still_out = _all_cards

        # Computing common prior of nature_cards
        for card in self._all_cards_still_out:
            eng = card.eng
            self.nature_cards[eng] = [0.25, 0.25, 0.25, 0.25]

    # END set_common_prior()

    def has_card(self, card_eng, posseser_id):

        self._all_cards_still_out = [x for x in self._all_cards_still_out if x.eng != card_eng]

        p_current = self.nature_cards[card_eng][posseser_id]
        rp_current = 1 - p_current

        p_new = 1  # surely 'posseser' has 'card'
        rp_new = 1 - p_new

        for i in range(4):
            if i == posseser_id:
                self.nature_cards[card_eng][i] = p_new
            else:
                original_prob = self.nature_cards[card_eng][i]
                if rp_current == 0:
                    raise Exception('Bad change div by zero', card_eng + " " + i)
                new_prob = original_prob * (rp_new / rp_current)
                self.nature_cards[card_eng][i] = new_prob
        # end for
    # end method

    # Observation - 'posseser' does not have 'card'
    def not_has_card(self, card_eng, posseser_id, situation=None):
        p_current = self.nature_cards[card_eng][posseser_id]
        rp_current = 1 - p_current

        p_new = 0  # surely 'posseser' does not have 'card'
        rp_new = 1 - p_new

        for i in range(4):
            if i == posseser_id:
                self.nature_cards[card_eng][i] = p_new
            else:
                original_prob = self.nature_cards[card_eng][i]
                if rp_current == 0:
                    raise Exception('Bad change div by zero', card_eng + " " + i)
                new_prob = original_prob * (rp_new / rp_current)
                self.nature_cards[card_eng][i] = new_prob
        # end for
        return
    # END not_has_card()

    # Observation - 'posseser' does not have any card from 'suite'
    def not_has_suite(self, player, suite):
        suite_cards_out_eng = [x.eng for x in self._all_cards_still_out if x.suite == suite]

        for card_eng in suite_cards_out_eng:
            self.not_has_card(card_eng, player)

        return
    # end function


def fill_prior_hands(taken_cards, _all_cards, index, _all_card_sets):

    # Stop recursing if 8 cards are already taken
    if len(taken_cards) == 8:
        engs = [x.eng for x in taken_cards]
        _all_card_sets.append(str(engs))
        return

    # Take the next card from one of the positions from index
    # (which is the position of last taken card)
    for i in range(index, len(_all_cards)):
        taken_cards.append(_all_cards[i])
        fill_prior_hands(taken_cards, _all_cards, i+1, _all_card_sets)
        taken_cards.pop()

    return  # Necessary?


def fill_prior_hands_simple(taken_cards, _all_cards, index, _all_card_sets):

    # Stop recursing if 8 cards can no longer be taken
    if index - len(taken_cards) > 23:
        return

    # Stop recursing if 8 cards are already taken
    if len(taken_cards) == 8:
        _all_card_sets.append(str(taken_cards))
        return

    # Take the next card from one of the positions from index
    # (which is the position of last taken card)
    for i in reversed(range(index, len(_all_cards))):
        taken_cards.append(_all_cards[i])
        fill_prior_hands_simple(taken_cards, _all_cards, i+1, _all_card_sets)
        taken_cards.pop()

    return  # Necessary?


def precompute_fill_prior_hands(taken_cards, index, _all_card_sets, mask=0):

    # # Stop recursing if 8 cards can no longer be taken
    if 8 - len(taken_cards) > index:
        return

    # Stop recursing if 8 cards are already taken
    if len(taken_cards) == 8:
        # _y = str(taken_cards.sort(reverse=True))
        # _all_card_sets.append(_y)
        _all_card_sets.append((str(taken_cards), mask))
        return

    # Take the next card from one of the positions from index
    # (which is the position of last taken card)
    for i in range(index, 0, -1):
        taken_cards.append(i)
        mask = mask + 2 ** i
        precompute_fill_prior_hands(taken_cards, i-1, _all_card_sets, mask)
        mask = mask - 2 ** i
        taken_cards.pop()

    return  # Necessary?