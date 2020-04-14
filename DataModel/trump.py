from DataModel import card


class Trump(card.Card):

    def __init__(self):
        self.number = None
        self.suite = None
        self.id = None
        self.closed = True

        self.is_trump_set = False
        self.is_trump_revealed = False
        self.trump_setter = -1

    @classmethod
    def trump_from_card(cls, card, setter):
        trump = cls()

        trump.number = card.number
        trump.suite = card.suite
        trump.id = card.id

        trump.is_trump_set = True
        trump.trump_setter = setter

        return trump
