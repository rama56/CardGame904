import copy

from DataModel.card import *
from Intelligence import arithmetic
from DataModel import ux_printable
from Intelligence.common_knowledge import CommonKnowledge


class Belief:
    def __init__(self, player_id):
        self.player_id = player_id
        self.cards_per_hand = 8

        # UX printable object
        self.ux_printable = ux_printable.UxBelief()

        # Private Knowledge
        # self.cards_in_hand = []

        # Belief about distribution of every hand's card set.
        self.nature_hands = [{}, {}, {}, {}]

        # Belief about with whom each card is.
        self.nature_cards = {}
        self._all_cards_still_out = []

        # Belief of nature will take shape as game is played and information is gained.
        # Belief about different players shall diverge.

        # end __init


    def get_capacity(self, cards):
        # TODO : Use belief to get a more appropriate capacity.
        # TODO : Measure strength based on cards in hand.
        strength = [0, 0, 0, 0]
        for x in cards:
            x = Card()
            suite = x.suite.value

        # TEMP : Return constant 500 always.
        return 500

    # Bayes Theorem : my_cards()
    # Theta is the belief distribution. (of a parameter)
    # X is the event observed (evidence), doesn't mean X happened.
    # Just that we know for sure now if X happened or not. ??
    # Posterior P(Theta | X) = Likelihood (X | Theta) *  Prior P(Theta) / Evidence's earlier probability P(X).

    def my_hand_cards(self, cards_in_hand, common_knowledge):

        # Capture information from common knowledge.
        self._all_cards_still_out = copy.deepcopy(common_knowledge.all_cards_still_out)
        self.nature_cards = copy.deepcopy(common_knowledge.nature_cards)

        for i in range(4):
            prior_copy = copy.deepcopy(common_knowledge.nature_hands)
            self.nature_hands[i] = prior_copy

        # Capture information from private information.
        # self.cards_in_hand = copy.deepcopy(cards_in_hand)

        # Shape belief with private knowledge.
        sig_cards_in_hand = [c.eng for c in cards_in_hand]   # No longer restrict to sig cards only.  if c.is_significant_card()]
        remaining_cards = get_remaining_cards_engs(sig_cards_in_hand)    # get_remaining_significant_cards(sig_cards_in_hand)

        for c in remaining_cards:
            # nature_1 = self.nature_hands[1]
            # nature_2 = self.nature_hands[2]
            # sum1 = sum(nature_1.values())
            # sum2 = sum(nature_2.values())
            self.not_has_card(c, self.player_id, "CardsDealt")

        for c in sig_cards_in_hand:
            # nature_1 = self.nature_hands[1]
            # nature_2 = self.nature_hands[2]
            # sum1 = sum(nature_1.values())
            # sum2 = sum(nature_2.values())
            self.has_card(c, self.player_id, "CardsDealt")

        # What to do with the remaining cards that we know are present/absent??
        # They need to be used at some point! TODO : Atleast update the nature_cards and later update nature_hands.

    #  Observation - 'posseser' has 'card'.
    def has_card(self, card_eng, posseser_id, situation=None):
        # Remove the has_card from _all_cards_still_out.
        # TODO : This is okay because has_card is called whenever any card is played out.
        #  but, is this one place sufficient? should I trim the _all_cards_still_out anywhere else?
        self._all_cards_still_out = [x for x in self._all_cards_still_out if x.eng != card_eng]

        if is_sig_card_eng(card_eng):
            self.has_sig_card(card_eng, posseser_id, situation)
        else:
            self.has_non_sig_card(card_eng, posseser_id, situation)

    # UPDATE NATURE_CARDS, BUT NOT NATURE_HANDS
    def has_non_sig_card(self, card_eng, posseser_id, situation):

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
            else:
                original_prob = self.nature_cards[card_eng][i]
                if rp_current == 0:
                    raise Exception('Bad change div by zero', card_eng + " " + i)
                new_prob = original_prob * (rp_new/rp_current)
                self.nature_cards[card_eng][i] = new_prob

    # UPDATE NATURE_CARDS AND NATURE_HANDS
    def has_sig_card(self, card_eng, posseser_id, situation=None):

        p_current = self.nature_cards[card_eng][posseser_id]
        rp_current = 1 - p_current

        p_new = 1   # surely 'posseser' has 'card'
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
                if p_current != p_new:      # posseser ideally knows he has the card, so it's of no use in card play phase, only useful in cards dealt phase.
                    self.card_prob_change(card_eng, i, p_current, p_new)
            else:
                original_prob = self.nature_cards[card_eng][i]
                if rp_current == 0:
                    raise Exception('Bad change div by zero', card_eng + " " + i)
                new_prob = original_prob * (rp_new/rp_current)
                self.nature_cards[card_eng][i] = new_prob
                # Alter nature_hand[i]
                if original_prob != new_prob:      # posseser ideally knows this i doesn't have the card , so it's of no use in card play phase, only useful in cards dealt phase.
                    self.card_prob_change(card_eng, i, original_prob, new_prob)
        # end for
    # end function

    # Observation - 'posseser' does not have 'card'
    def not_has_card(self, card_eng, posseser_id, situation=None):
        if is_sig_card_eng(card_eng):
            self.not_has_sig_card(card_eng, posseser_id, situation)
        else:
            self.not_has_non_sig_card(card_eng, posseser_id, situation)

    # UPDATE NATURE_CARDS AND NATURE_HANDS
    def not_has_sig_card(self, card_eng, posseser_id, situation=None):

        p_current = self.nature_cards[card_eng][posseser_id]
        rp_current = 1 - p_current

        p_new = 0  # surely 'posseser' has 'card'
        rp_new = 1 - p_new

        for i in range(4):
            if self.player_id == posseser_id and situation != "CardsDealt":
                # If this is not the cards dealing phase, then nothing is to be changed in belief
                # about his own card absence.
                continue
            if i == self.player_id and situation != "CardsDealt":
                # If this is not the cards dealing phase, then nothing is to be done about belief of oneself's cards.
                continue

            if i == posseser_id:
                self.nature_cards[card_eng][i] = p_new
                # Alter nature_hand[i]
                if p_current != p_new:
                    self.card_prob_change(card_eng, i, p_current, p_new)
            else:
                original_prob = self.nature_cards[card_eng][i]
                if rp_current == 0:
                    raise Exception('Bad change div by zero', card_eng + " " + i)
                new_prob = original_prob * (rp_new / rp_current)
                self.nature_cards[card_eng][i] = new_prob
                # Alter nature_hand[i]
                if original_prob != new_prob:
                    self.card_prob_change(card_eng, i, original_prob, new_prob)
        # end for
        return
    # end function

    # UPDATE NATURE_CARDS, BUT NOT NATURE_HANDS
    def not_has_non_sig_card(self, card_eng, posseser_id, situation=None):

        p_current = self.nature_cards[card_eng][posseser_id]
        rp_current = 1 - p_current

        p_new = 0  # surely 'posseser' has 'card'
        rp_new = 1 - p_new

        for i in range(4):
            if self.player_id == posseser_id and situation != "CardsDealt":
                # If this is not the cards dealing phase, then nothing is to be changed in belief
                # about his own card absence.
                continue
            if i == self.player_id and situation != "CardsDealt":
                # If this is not the cards dealing phase, then nothing is to be done about belief of oneself's cards.
                continue

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
    # end function

    # Observation - 'posseser' does not have 'card'
    def not_has_suite(self, player, suite):
        suite_cards_out_eng = [x.eng for x in self._all_cards_still_out if x.suite == suite]

        for card_eng in suite_cards_out_eng:
            self.not_has_card(card_eng, player)

        return
    # end function

    # Knowledge is gained that (Event X = player_i's having card_eng)'s probability has changed from
    # p_old to p_new.
    def card_prob_change(self, card_eng, player_i, p_old, p_new):
        # If p_old is 0 or 1 and if there's a consideration of it being moved to p_new,
        # somethings wrong.
        if p_old == 0 or p_old == 1:
            raise Exception('Bad prob change', card_eng + " " + str(self.player_id) + " " + str(player_i) +
                            " " + str(p_old) + " " + str(p_new))

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
            # else:
            #     self.impossible[card_set] = 0

        # I observe that the prob values don't sum up to 1. They begin at 0.999999 for a card_set,
        # but, slowly get lower and lower even upto 0.6 and then again shoot up to 1.3 for 50% has cards,
        # and 50% 'not has cards'. Hence, I'm going to do the sin of normalization.
        total = sum(temp.values())

        temp2 = {k: v/total for k, v in temp.items()}
        self.nature_hands[player_i] = temp2


