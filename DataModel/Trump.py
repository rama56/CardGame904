from DataModel import Card


class Trump(Card.Card):
    def __init__(self, card):
        self.number = card.number
        self.suite = card.suite
        self.id = card.id

        self.is_trump_set = True
        self.is_trump_revealed = False

    def __init__(self):
        self.number = None
        self.suite = None
        self.id = None

        self.is_trump_set = False
        self.is_trump_revealed = False
        self.trump_setter = -1
    # Try to internally call constructors.
