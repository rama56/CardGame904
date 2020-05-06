from operator import itemgetter
import math
import ast
from DataModel import card

class UxBelief:
    def __init__(self):
        self.surely_has = [[], [], [], []]
        self.nature_hands = []
        self.nature_cards = []
        # Do nothing

    def set_printable_hands_belief(self, nature_hands):
        # Fill belief about every hand.

        self.nature_hands = []
        for i in range(4):
            b = nature_hands[i]
            # Get top 20 card_sets
            n = 20
            n = min(n, b.shape[0])                                  # n = min(n, len(b))
                                                                    # n largest values in dictionary
            top20 = b.nlargest(n, 'Probability')                                                        # Using sorted() + itemgetter() + items()
            top20_list = top20.values.tolist()                                                    # top20 = dict(sorted(b.items(), key=itemgetter(1), reverse=True)[:n])

            for i in range(len(top20_list)):
                list_id_str = top20_list[i][0]
                list_id = ast.literal_eval(list_id_str)
                list_eng = [card.id_eng_mapping[x] for x in list_id]
                list_eng_str = str(list_eng)
                top20_list[i][0] = list_eng_str

            self.nature_hands.append(top20_list)

        # Fill belief about every card.

    def set_printable_cards_belief(self, nature_cards):
        self.nature_cards = []
        self.surely_has = [[], [], [], []]

        nature_cards_list = [[k, v[0], v[1], v[2], v[3]] for k, v in nature_cards.items()]
        self.nature_cards = nature_cards_list

        for k, v in nature_cards.items():
            for i in range(4):
                if v[i] == 1:
                    self.surely_has[i].append(k)

        x = 5



