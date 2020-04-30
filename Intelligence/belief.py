import copy

from DataModel.card import *
from Intelligence import arithmetic
from DataModel import ux_printable


class Belief:
    def __init__(self, player_id):
        self.player_id = player_id
        self.cards_per_hand = 4

        # UX printable object
        self.ux_printable = ux_printable.UxBelief()

        # At the beginning, the common prior is the uniform belief about the nature for any player,
        # as there is no private information.
        self.common_prior = {}

        # Belief after cards are dealt. Even at this stage,
        # for a given player, his belief about others is uniform.
        self.private_interim = {}
        self.impossible = {}    # Temp debugging stuff..

        # Belief of nature will take shape as game is played and information is gained.
        # Belief about different players shall diverge.
        self.nature_hands = [{}, {}, {}, {}]

        # Belief about with whom each card is.
        self.nature_cards = {}

        # Computing common prior
        self._significant_cards = get_significant_cards()  # card.get_significant_cards() get_deck()
        self.fill_prior([], self._significant_cards, 0)

        # Fill chance of hands in which every card is present.
        self._all_cards_still_out = get_deck()
        for card in self._all_cards_still_out:
            eng = card.eng
            self.nature_cards[eng] = [0.25, 0.25, 0.25, 0.25]

        # Common prior is the initial state of nature.
        for i in range(4):
            prior_copy = copy.deepcopy(self.common_prior)
            self.nature_hands[i] = prior_copy

        # end __init

    def fill_prior(self, taken_cards, cards, index):

        prob = arithmetic.probability_prior(len(taken_cards))
        # self.common_prior[tuple(taken_cards)] = prob
        engs = [x.eng for x in taken_cards]
        self.common_prior[tuple(engs)] = prob

        # Stop recursing if 8 cards are already taken.
        if len(taken_cards) == self.cards_per_hand:
            return

        # Take the next card from one of the positions from index
        # (which is the position of last taken card)
        for i in range(index, len(cards)):
            taken_cards.append(cards[i])
            self.fill_prior(taken_cards, cards, i+1)
            taken_cards.pop()

        return  # Necessary?

    def get_capacity(self, cards):
        # TODO : Use belief to get a more appropriate capacity.
        # TODO : Measure strength based on cards in hand.
        strength = [0, 0, 0, 0]
        for x in cards:
            x = Card()
            suite = x.suite.value

        # TEMP : Return constant 500 always.
        return 500

    # Bayes Theorem :
    # Theta is the belief distribution. (of a parameter)
    # X is the event observed (evidence), doesn't mean X happened.
    # Just that we know for sure now if X happened or not. ??
    # Posterior P(Theta | X) = Likelihood (X | Theta) *  Prior P(Theta) / Evidence's earlier probability P(X).
    def my_cards(self, cards_in_hand):
        significant_cards = [x for x in cards_in_hand if x.is_significant_card()]   # cards

        for key, value in self.common_prior.items():
            p_prior = value
            p_posterior = p_prior
            for x in significant_cards:
                # Evidence is that card 'x' is not with a particular opponent.
                p_evidence = 0.75

                # Probability that 'x' is not with a particular person given he has the cards 'key'.
                p_likelihood = 1
                for val in key:
                    if x.eng == val:
                        p_likelihood = 0  # If 'key' has card 'x', P ('x' absent given key) = 0

                p_posterior = arithmetic.calc_posterior(p_likelihood, p_evidence, p_prior)

                if p_posterior == 0:
                    self.impossible[key] = p_posterior
                    break

                p_prior = p_posterior

            if p_posterior != 0:
                self.private_interim[key] = p_posterior

    def my_cards_2(self, cards_in_hand):

        sig_cards_in_hand = [c.eng for c in cards_in_hand if c.is_significant_card()]

        remaining_cards = get_remaining_significant_cards(sig_cards_in_hand)

        for c in remaining_cards:
            # nature_1 = self.nature_hands[1]
            # nature_2 = self.nature_hands[2]
            # sum1 = sum(nature_1.values())
            # sum2 = sum(nature_2.values())
            self.not_has_card(c, self.player_id)

        for c in sig_cards_in_hand:
            # nature_1 = self.nature_hands[1]
            # nature_2 = self.nature_hands[2]
            # sum1 = sum(nature_1.values())
            # sum2 = sum(nature_2.values())
            self.has_card(c, self.player_id)

        # What to do with the remaining cards that we know are present/absent??
        # They need to be used at some point! TODO : Atleast update the nature_cards and later update nature_hands.

    #  Observation - 'posseser' has 'card'.
    def has_card(self, card_eng, posseser_id):
        # Remove the has_card from _all_cards_still_out.
        # TODO : This is okay because has_card is called whenever any card is played out.
        #  but, is this one place sufficient? should I trim the _all_cards_still_out anywhere else?
        self._all_cards_still_out = [x for x in self._all_cards_still_out if x.eng != card_eng]

        p_current = self.nature_cards[card_eng][posseser_id]
        rp_current = 1 - p_current

        p_new = 1   # surely 'posseser' has 'card'
        rp_new = 1 - p_new

        for i in range(4):
            if i == posseser_id:
                self.nature_cards[card_eng][i] = p_new
                # Alter nature_hand[i]
                self.card_prob_change(card_eng, i, p_current, p_new)
            else:
                original_prob = self.nature_cards[card_eng][i]
                new_prob = original_prob * (rp_new/rp_current)
                self.nature_cards[card_eng][i] = new_prob
                # Alter nature_hand[i]
                self.card_prob_change(card_eng, i, original_prob, new_prob)
        # end for
    # end function

    # Observation - 'posseser' does not have 'card'
    def not_has_card(self, card_eng, posseser_id):

        p_current = self.nature_cards[card_eng][posseser_id]
        rp_current = 1 - p_current

        p_new = 0  # surely 'posseser' has 'card'
        rp_new = 1 - p_new

        for i in range(4):
            if i == posseser_id:
                self.nature_cards[card_eng][i] = p_new
                # Alter nature_hand[i]
                self.card_prob_change(card_eng, i, p_current, p_new)
            else:
                original_prob = self.nature_cards[card_eng][i]
                new_prob = original_prob * (rp_new / rp_current)
                self.nature_cards[card_eng][i] = new_prob
                # Alter nature_hand[i]
                self.card_prob_change(card_eng, i, original_prob, new_prob)
        # end for
        return
    # end function

    # Observation - 'posseser' does not have 'card'
    def not_has_suite(self, suite, posseser_id):
        suite_cards_out_eng = [x.eng for x in self._all_cards_still_out if x.suite == suite]

        for card_eng in suite_cards_out_eng:
            self.not_has_card(card_eng, posseser_id)

        return
    # end function

    # Knowledge is gained that (Event X = player_i's having card_eng)'s probability has changed from
    # p_old to p_new.
    def card_prob_change(self, card_eng, player_i, p_old, p_new):
        # If p_old is 0 or 1 and if there's a consideration of it being moved to p_new,
        # somethings wrong.
        if p_old == 0 or p_old == 1:
            raise Exception('Bad prob change', card_eng + " " +  str(player_i) +
                            " " + str(p_old) + " " + str(p_new) )

        card_set_distribution = self.nature_hands[player_i]
        # Update belief about every card_set_distribution's card_set based on the 'Knowledge' gained.

        temp = {}

        for card_set, prob_val in card_set_distribution.items():

            # Now, I don't know Bayes theorem for this. As we don't observe a clear evidence.
            # It's just a change in probability of the card (evidence)
            # Assume X is true, calculate posterior, use it with p_new prob &
            # Assume X is false, calculate posterior, use it with 1 - p_new prob. Okay?
            p_prior = prob_val

            # Evidence is that 'card' is with 'posseser'/'p'.
            p_evidence = p_old

            # Likelihood that 'card' is with player_i if 'card_set' is what he has.
            p_likelihood = 0
            if card_eng in card_set:
                p_likelihood = 1

            p_posterior_positive = arithmetic.calc_posterior(p_likelihood, p_evidence, p_prior)

            # Evidence is that 'card' is not with 'p'.
            p_evidence = 1 - p_old

            # Likelihood that 'card' is not present in 'card_set'
            p_likelihood = 1
            if card_eng in card_set:
                p_likelihood = 0

            p_posterior_negative = arithmetic.calc_posterior(p_likelihood, p_evidence, p_prior)

            p_posterior = (p_posterior_positive * p_new) + (p_posterior_negative * (1-p_new))

            if p_posterior != 0:
                temp[card_set] = p_posterior
            else:
                self.impossible[card_set] = 0

        # I observe that the prob values don't sum up to 1. They begin at 0.999999 for a card_set,
        # but, slowly get lower and lower even upto 0.6 and then again shoot up to 1.3 for 50% has cards,
        # and 50% 'not has cards'. Hence, I'm going to do the sin of normalization.
        total = sum(temp.values())

        temp2 = {k: v/total for k, v in temp.items()}
        self.nature_hands[player_i] = temp2


