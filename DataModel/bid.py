

class Bid:
    def __init__(self):
        self.bidHistory = []
        self.recentBidValue = -1
        self.minimumNextBid = 500
        self.maximumBid = 904

    def add_bid(self, move, current_player):
        self.bidHistory.append((move, current_player))

        self.minimumNextBid = move + 1

        if len(self.bidHistory) >= 4:
            self.minimumNextBid = max(700, self.minimumNextBid)
        elif len(self.bidHistory) >= 8:
            self.minimumNextBid = 904

    def get_trump_setter_and_target(self):

        # No one bids anything, by default, the starter sets trump for 500 points.
        if len(self.bidHistory) == 4 and [bid[0] for bid in self.bidHistory] == [-1, -1, -1, -1]:
            return 500, self.bidHistory[0][1]

        # Bidding closes if someone bids 'full' 904.
        last_bidder = self.bidHistory[-1]
        if last_bidder[0] == 904:
            return last_bidder

        # Bidding closes if all three other players don't raise.
        if [bid[0] for bid in self.bidHistory[-3:]] == [-1, -1, -1]:
            return self.bidHistory[-4]

        # If the bidding is still in progress, return -1, -1.
        return -1, -1


