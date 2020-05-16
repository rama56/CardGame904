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
            n = min(n, b.shape[0])

            top20 = b.nlargest(n, 'Probability').copy(deep=True)
            top20_reset = top20.reset_index()
            col_order = ['CardSet', 'Probability', 'Strength', 'TrumpCandidate']
            top20_reset_reordered = top20_reset[col_order]

            top20_list = top20_reset_reordered.values.tolist()

            for j in range(len(top20_list)):
                list_id_str = top20_list[j][0]
                list_id = ast.literal_eval(list_id_str)
                list_eng = [card.id_eng_mapping[x] for x in list_id]
                trimmed_list_eng = [x for x in list_eng if x not in self.surely_has[i]]
                list_eng_str = str(trimmed_list_eng)
                top20_list[j][0] = list_eng_str

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



