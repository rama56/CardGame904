from DataModel.card import Card


class Carpet:
    def __init__(self):
        # self.North = None
        # self.East = None
        # self.South = None
        # self.West = None
        # TODO : Seriously consider making this an array instead of this North, South stuff.

        self.cards = [-1, -1, -1, -1]

        self.starter = None
        self.winner = None
        self.size = 0
        self.suite = None

    @classmethod
    def carpet_starter(cls, starter):
        carpet = cls()
        carpet.starter = starter
        return carpet

    def add_card(self, player, card):
        self.cards[player] = card
        self.size = self.size + 1
        if self.size == 1:
            self.suite = card.suite

    def is_round_over(self):
        return self.size == 4

    def compute_winner(self, is_trump_revealed, trump_suite):

        winner, win_value = (-1,-1)

        for i in range(4):
            if self.cards[i].suite == self.suite and self.cards[i].number > win_value:
                winner, win_value = i, self.cards[i].number

        if is_trump_revealed:
            win_value = -1
            for i in range(4):
                if self.cards[i].suite == trump_suite and self.cards[i].number > win_value:
                    winner, win_value = i, self.cards[i].number

        self.winner = winner

        return winner, win_value
