from operator import itemgetter
import math


class UxBelief:
    def __init__(self):
        self.nature_hands = []
        self.nature_cards = []
        # Do nothing

    def set_printable_hands_belief(self, nature_hands):
        # Fill belief about every hand.
        for i in range(4):
            b = nature_hands[i]
            # Get top 20 card_sets
            n = 20
            n = min(n, len(b))
            # n largest values in dictionary
            # Using sorted() + itemgetter() + items()
            top20 = dict(sorted(b.items(), key=itemgetter(1), reverse=True)[:n])
            top20_list = [[str(k), v] for k, v in top20.items()]
            self.nature_hands.append(top20_list)

        # Fill belief about every card.

    def set_printable_cards_belief(self, nature_cards):
        nature_cards_list = [[k, v[0], v[1], v[2], v[3]] for k, v in nature_cards.items()]
        self.nature_cards = nature_cards_list



