from DataModel.card import get_significant_cards, get_deck
from Intelligence import arithmetic


class CommonKnowledge:

    # (EVERYONE KNOWS THAT)^inf EVERYONE KNOWS THE INFORMATION OF THIS CLASS OBJECT.

    def __init__(self):
        # Distribution of the hand's card set.
        self.nature_hands = {}  # TODO: [{}, {}, {}, {}] will still be required when learning from bids happen.

        # For each card, chance of it being in different hands.
        self.nature_cards = {}
        self.cards_per_hand = 8

        self.all_cards_still_out = []

    def set_common_prior(self):
        # At the beginning, the common prior is the uniform belief about the nature for any player,

        # Computing common prior of nature_hands
        _significant_cards = get_significant_cards()  # card.get_significant_cards() get_deck()
        self.fill_prior_hands([], _significant_cards, 0)

        # Common prior of cards still out there in the hands
        self.all_cards_still_out = get_deck()

        # Computing common prior of nature_cards
        for card in self.all_cards_still_out:
            eng = card.eng
            self.nature_cards[eng] = [0.25, 0.25, 0.25, 0.25]

    def fill_prior_hands(self, taken_cards, cards, index):

        prob = arithmetic.probability_prior(len(taken_cards))
        # self.common_prior[tuple(taken_cards)] = prob
        engs = [x.eng for x in taken_cards]
        self.nature_hands[tuple(engs)] = prob

        # Stop recursing if 8 cards are already taken.
        if len(taken_cards) == self.cards_per_hand:
            return

        # Take the next card from one of the positions from index
        # (which is the position of last taken card)
        for i in range(index, len(cards)):
            taken_cards.append(cards[i])
            self.fill_prior_hands(taken_cards, cards, i+1)
            taken_cards.pop()

        return  # Necessary?
