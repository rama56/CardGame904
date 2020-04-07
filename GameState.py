import Card
import Player

class GameState:

  def __init__(self):
    # CREATE A NEW GAME STATE.

    # META DATA
    isGameRunning = True
    playerCount = 4
    players = []
    winner = Player(None,None,None)

    # BID DATA
    bidProgression = []
    bidStarter = Player
    maxBid = -1
    minimumNextBid = -1
    TrumpCard = Card(None, None)

    # Add other variables for cards dealt, points earned etc.
