
from DataModel.card import *
from GameHost.perf import parallelize_dataframe
from Intelligence import arithmetic
from DataModel import ux_printable
from Intelligence import common_knowledge
from Intelligence import belief_helper
from GameHost import session_helper

import copy
import pandas as pd
import numpy as np
from timeit import default_timer as timer
import logging

import ast


class Belief:
    def __init__(self, player_id):
        self.player_id = player_id
        self.cards_per_hand = 8

        # UX printable object
        self.ux_printable = ux_printable.UxBelief()

        # Private Knowledge
        # self.cards_in_hand = []

        # Belief about distribution of every hand's card set.
        self.nature_hands = [None, None, None, None]  # [{}, {}, {}, {}]

        # Belief about with whom each card is.
        self.nature_cards = {}
        self._all_cards_still_out = []

        # Belief about strength of hands (bid range)
        self.bid_strength = [None, None, None, None]

        # Belief of nature will take shape as game is played and information is gained.
        # Belief about different players shall diverge.

        # end __init

    def my_hand_cards(self, cards_in_hand, ck):

        logging.info('Belief - Inside my_hand_cards')

        _card_ids_in_hand = [x.id for x in cards_in_hand]
        _card_engs_in_hand = [x.eng for x in cards_in_hand]
        # Capture information from common knowledge.
        self._all_cards_still_out = copy.deepcopy(ck._all_cards_still_out)
        self.nature_cards = copy.deepcopy(ck.nature_cards)

        self._all_cards_still_out = [x for x in self._all_cards_still_out if x.id not in _card_ids_in_hand]

        _all_cards_out_ids = [x.id for x in self._all_cards_still_out]
        _all_cards_out_ids.sort(reverse=True)
        # SHAPE NATURE HANDS
        _all_card_sets = []
        # common_knowledge.fill_prior_hands([], self._all_cards_still_out, 0, _all_card_sets)

        # common_knowledge.fill_prior_hands_simple([], _all_cards_out_ids, 0, _all_card_sets)
        # individual_prior = pd.DataFrame(_all_card_sets, columns=['CardSet'])
        # individual_prior.astype(str)
        # individual_prior_store = session_helper.join_for_belief_scores(individual_prior)

        _card_ids_in_hand_mask = arithmetic.get_mask(_card_ids_in_hand)
        individual_prior_store = session_helper.filter_cardsets_out(_card_ids_in_hand_mask)

        # prob = arithmetic.choose_prob(24, 8)
        # individual_prior_store['Probability'] = prob

        # individual_prior['Strength'] = individual_prior['CardSet'].swifter.apply(
        #     get_strength_from_cardset_string)  # takes 2.4 minutes.

        # individual_prior['CardSetList'] = individual_prior['CardSet'].apply(get_list_from_engs)
        # individual_prior['CardSetIds'] = individual_prior['CardSetList'].apply(get_ids_from_list)

        # individual_prior_store = belief_helper.fill_strength_and_trump_choice(individual_prior)
        # trying out parallel execution.
        # ----- individual_prior_store = parallelize_dataframe(individual_prior, belief_helper.fill_strength_and_trump_choice)

        # top_20 = individual_prior.nlargest(20, 'Strength', keep='all')
        # last_20 = individual_prior.nsmallest(20, 'Strength', keep='all')

        for i in range(4):
            if i == self.player_id:
                _self_card_set = [str([x.id for x in cards_in_hand])]
                self_prior = pd.DataFrame(_self_card_set, columns=['CardSet'])

                strength, trump_card = get_strength(cards_in_hand)
                self_prior['Strength'] = strength
                self_prior['TrumpCandidate'] = trump_card.suite.value
                self_prior['Mask'] = arithmetic.get_mask(_card_ids_in_hand)
                self_prior['Probability'] = 1
                self_prior = self_prior[['Probability', 'Strength', 'TrumpCandidate', 'Mask']]

                # self_prior = self_prior.set_index('CardSet')
                self.nature_hands[i] = self_prior
            else:
                prior_copy = copy.deepcopy(individual_prior_store)
                self.nature_hands[i] = prior_copy

        # SHAPE NATURE CARDS
        deck_eng = [x.eng for x in get_deck()]

        # hard-coding instead of the elaborate formula
        for c_eng in deck_eng:
            for i in range(4):
                if i == self.player_id:
                    self.nature_cards[c_eng][i] = 1 if c_eng in _card_engs_in_hand else 0
                else:
                    self.nature_cards[c_eng][i] = 0 if c_eng in _card_engs_in_hand else 1 / 3
            # end for
        # end for

    # end my_hand_cards()

    def bidding_over(self):
        # _nature_cards_symmetric = {'Two': [0, 0, 0, 0], 'Three': [0, 0, 0, 0], 'Jack': [0, 0, 0, 0],
        # 'Nine': [0, 0, 0, 0],  'Ace': [0, 0, 0, 0], 'Ten': [0, 0, 0, 0], 'King': [0, 0, 0, 0], 'Queen': [0, 0, 0, 0]}
        # copy.deepcopy(self.nature_cards) # nature_cards is gonna go for a toss now !

        for i in range(4):
            if i == self.player_id:
                # I have nothing to do about my belief about myself. They're full set (deterministic - prob 0 or 1)
                continue

            if self.bid_strength[i] is None:
                # Some earlier player has bid 904. Nothing to do.
                # TODO: Shouldn't others naturally get weaker?
                continue

            min_val, max_val = self.bid_strength[i]

            distribution = self.nature_hands[i]

            # row_count = distribution.shape[0]

            heavy_flag = (min_val <= distribution['Strength']) & (distribution['Strength'] <= max_val)
            dist_heavy = distribution.loc[heavy_flag]
            dist_light = distribution.loc[~heavy_flag]

            heavy_sum = dist_heavy['Probability'].sum()
            light_sum = dist_light['Probability'].sum()

            heavy_mass = 0.9
            light_mass = 0.1

            if min_val == 0:
                heavy_mass = 0.999
                light_mass = 0.001

            heavy_factor = heavy_mass / heavy_sum
            light_factor = light_mass / light_sum

            dist_heavy['Probability'] = dist_heavy['Probability'] * heavy_factor
            dist_light['Probability'] = dist_light['Probability'] * light_factor

            new_distribution = pd.concat([dist_heavy, dist_light])
            new_sum = new_distribution['Probability'].sum()
            assert 0.999 < new_sum < 1.001

            self.nature_hands[i] = new_distribution
            # # TODO : Work on how nature_cards gets affected. My approach feels wrong. Maybe, get it from
            # #  the fraction in nature_hands.
            # heavy_count = dist_heavy['Probability'].shape[0]
            # light_count = dist_light['Probability'].shape[0]

    #  Observation - 'posseser' has 'card'. ENG_TO_ID
    def has_card(self, card_id, posseser_id, situation=None):

        card_eng = id_eng_mapping[card_id]

        # Remove the has_card from _all_cards_still_out.
        # TODO : This is okay because has_card is called whenever any card is played out.
        #  but, is this one place sufficient? should I trim the _all_cards_still_out anywhere else?
        self._all_cards_still_out = [x for x in self._all_cards_still_out if x.eng != card_eng]

        p_current = self.nature_cards[card_eng][posseser_id]
        rp_current = 1 - p_current

        p_new = 1  # surely 'posseser' has 'card'
        rp_new = 1 - p_new

        for i in range(4):
            if self.player_id == posseser_id and situation != "CardsDealt":
                # If this is not the cards dealing phase, then nothing is to be changed in belief
                # about his own card possession.
                continue
            if i == self.player_id and situation != "CardsDealt":
                # If this is not the cards dealing phase, then nothing is to be done about belief of oneself's cards.
                continue

            if i == posseser_id:
                self.nature_cards[card_eng][i] = p_new
                # Alter nature_hand[i]
                if p_current != p_new:  # posseser ideally knows he has the card, so it's of no use in card play phase, only useful in cards dealt phase.
                    self.card_prob_change(card_id, i, p_current, p_new)
            else:
                original_prob = self.nature_cards[card_eng][i]
                if rp_current == 0:
                    raise Exception('Bad change div by zero', card_eng + " " + i)
                new_prob = original_prob * (rp_new / rp_current)
                self.nature_cards[card_eng][i] = new_prob
                # Alter nature_hand[i]
                if original_prob != new_prob:  # posseser ideally knows this i doesn't have the card , so it's of no use in card play phase, only useful in cards dealt phase.
                    self.card_prob_change(card_id, i, original_prob, new_prob)
        # end for

    # end method

    # Observation - 'posseser' does not have 'card'
    def not_has_card(self, card_id, posseser_id, situation=None):

        if self.player_id == posseser_id and situation != "CardsDealt":
            # If this is not the cards dealing phase, then nothing is to be changed in belief
            # about his own card absence.
            return

        card_eng = id_eng_mapping[card_id]

        p_current = self.nature_cards[card_eng][posseser_id]
        rp_current = 1 - p_current

        p_new = 0  # surely 'posseser' has 'card'
        rp_new = 1 - p_new

        for i in range(4):

            if i == self.player_id and situation != "CardsDealt":
                # If this is not the cards dealing phase, then nothing is to be done about belief of oneself's cards.
                continue

            if i == posseser_id:
                self.nature_cards[card_eng][i] = p_new
                # Alter nature_hand[i]
                if p_current != p_new:
                    self.card_prob_change(card_id, i, p_current, p_new)
            else:
                original_prob = self.nature_cards[card_eng][i]
                if rp_current == 0:
                    raise Exception('Bad change div by zero', card_eng + " " + i)
                new_prob = original_prob * (rp_new / rp_current)
                self.nature_cards[card_eng][i] = new_prob
                # Alter nature_hand[i]
                if original_prob != new_prob:
                    self.card_prob_change(card_id, i, original_prob, new_prob)
        # end for

    # end not_has_card()

    # Observation - 'posseser' does not have any card from 'suite' # ENG_TO_ID
    def not_has_suite(self, player, suite):
        suite_cards_out_id = [x.id for x in self._all_cards_still_out if x.suite == suite]

        for card_id in suite_cards_out_id:
            self.not_has_card(card_id, player)

        return

    # end function

    # Bayes Theorem : my_cards()
    # Theta is the belief distribution. (of a parameter)
    # X is the event observed (evidence), doesn't mean X happened.
    # Just that we know for sure now if X happened or not. ??
    # Posterior P(Theta | X) = Likelihood (X | Theta) *  Prior P(Theta) / Evidence's earlier probability P(X).

    # Knowledge is gained that (Event X = player_i's having card_eng)'s probability has changed from
    # p_old to p_new.
    def card_prob_change(self, card_id, player_i, p_old, p_new):
        # If p_old is 0 or 1 and if there's a consideration of it being moved to p_new,
        # somethings wrong.
        if p_old == 0 or p_old == 1:
            raise Exception('Bad prob change', card_id + " " + str(self.player_id) + " " + str(player_i) +
                            " " + str(p_old) + " " + str(p_new))

        card_set_distribution = self.nature_hands[player_i]

        # Update belief card_set_distribution's CardSet based on the 'Knowledge' gained.

        # none_rows = card_set_distribution[card_set_distribution['CardSet'].isnull()]
        # none_rows = card_set_distribution[card_set_distribution.index.isnull()]
        #
        # if none_rows.shape[0] > 0:
        #     a = 5

        start = timer()
        has_card_id = belief_helper.get_has_card_id_flag(card_set_distribution, card_id)    # parallelize_dataframe(card_set_distribution, belief_helper.get_has_card_id_flag, param=card_id)
        end = timer()
        elapsed = end - start
        logging.info('get_has_card_id_flag completed. Time elapsed = ' + str(elapsed))

        # has_card_id = belief_helper.get_has_card_id_flag(card_set_distribution, card_id)

        # Now, I don't know Bayes theorem for this. As we don't observe a clear evidence.
        # It's just a change in probability of the card (evidence)
        # Assume X is true, calculate posterior, use it with p_new prob &
        # Assume X is false, calculate posterior, use it with 1 - p_new prob. Okay?
        p_prior = card_set_distribution['Probability']

        # POSITIVE
        # Evidence is that 'card' is with 'posseser'/'p'.
        p_evidence = p_old

        # Likelihood that 'card' is with player_i if 'card_set' is what he has.
        p_likelihood = has_card_id * 1

        p_posterior_pos = arithmetic.calc_posterior(p_likelihood, p_evidence, p_prior)

        # NEGATIVE
        # Evidence is that 'card' is not with 'p'.
        p_evidence = 1 - p_old

        # Likelihood that 'card' is not present in 'card_set'
        p_likelihood = 1 - (has_card_id * 1)

        p_posterior_neg = arithmetic.calc_posterior(p_likelihood, p_evidence, p_prior)

        card_set_distribution['Probability'] = (p_posterior_pos * p_new) + (p_posterior_neg * (1 - p_new))

        total = card_set_distribution['Probability'].sum()
        card_set_distribution['Probability'] = card_set_distribution['Probability'] / total

        non_zero_rows_flag = card_set_distribution['Probability'] != 0
        non_zero_rows = card_set_distribution[non_zero_rows_flag]


        self.nature_hands[player_i] = non_zero_rows

    def trump_revealed(self, _trump_setter, _card_played_id):
        distribution = self.nature_hands[_trump_setter]

        _suite = (_card_played_id - 1) // 8

        trump_flag = distribution['TrumpCandidate'] == _suite

        dist_heavy = distribution.loc[trump_flag]
        dist_light = distribution.loc[~trump_flag]

        heavy_sum = dist_heavy['Probability'].sum()
        light_sum = dist_light['Probability'].sum()

        heavy_mass = 0.99
        light_mass = 0.01

        heavy_factor = heavy_mass / heavy_sum
        light_factor = light_mass / light_sum

        dist_heavy['Probability'] = dist_heavy['Probability'] * heavy_factor
        dist_light['Probability'] = dist_light['Probability'] * light_factor

        new_distribution = pd.concat([dist_heavy, dist_light])
        assert 0.99 < sum(new_distribution['Probability']) < 1.01

        self.nature_hands[_trump_setter] = new_distribution

# ORIGINAL CODE

def get_strength_from_cardset_string(cardset):
    card_list = ast.literal_eval(cardset)
    cards = [get_card_from_eng(x) for x in card_list]
    return get_strength(cards)


# Now, this is some unjustified heuristic!
def get_strength(cards, f=None):
    # TODO : Use belief to get a more appropriate strength?
    if f is None:
        f = [-1, 3, 2.5, 1.8, 1.5, 1.5, 1.5, 1.2]

    buckets = [[], [], [], []]
    trump_card = None
    cards.sort(key=lambda c: c.points, reverse=True)

    for x in cards:
        suite = x.suite.value
        buckets[suite].append(x)

    # strength = [[], [], [], []]
    strength = 0
    max_val = 0
    for b in buckets:
        if len(b) == 0:
            continue

        s = 0
        same_suite_count = 0
        for c in b:
            s = s * f[same_suite_count] + c.points  # s = s + (1 + same_suite_count * 2) * c.points
            same_suite_count = same_suite_count + 1

        suit_strength = s / len(b)

        strength = strength + suit_strength
        if suit_strength > max_val:
            # trump_suite = b[0].suite
            card_number = len(b) - 1
            trump_card = b[card_number]
            max_val = suit_strength

    value = (strength // 10) * 10
    value = min(904, value)

    return value, trump_card
