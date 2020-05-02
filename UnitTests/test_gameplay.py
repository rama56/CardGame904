from unittest import TestCase

# Internal dependencies
from DataModel import game_state
from Intelligence import belief
from DataModel.card import *


# SAMPLE CARD SETS

#  0 strong. Others even.
#  [2S, 3S, AS, 10S  |  KH | 2D | 3C, JC] - 0
#  [KS | 3H, 9H, 10H | 10D, KD | 2C, 10C] - 1
#  [9S | JH, AH, QH | JD, 9D | KC, QC] - 2
#  [JS, QS | 2H | 3D, AD, QD | 9C, AC] - 3

card_set_1 = [[8, 7, 4, 3, 10, 24, 31, 30],
              [2, 15, 13, 11, 19, 18, 32, 27],
              [5, 14, 12, 9, 22, 21, 26, 25],
              [6, 1, 16, 23, 20, 17, 29, 28]]


class Test(TestCase):

    # NO AI AGENT CALLED.

    def test_bidding_phase(self):

        # CREATE INSTANCE OF GAME.

        game = game_state.GameState(card_set_1)     # AVOID RANDOMNESS, HAVE DETERMINISTIC HANDS.

        # Player 0 to bid. Let him bid 550 and others pass.
        game.move = 550
        game.alter_state()

        for i in range(1, 4):
            game.move = -1
            game.alter_state()

        # Player 0 to set Trump. (Sets Ace Spade)
        game.move = 4
        game.alter_state()

        # Round 1 : 3- 2H, 0- KH, 1- 3H, 2-QH
        game.move = 16
        game.alter_state()
        game.move = 10
        game.alter_state()
        game.move = 15
        game.alter_state()
        game.move = 9
        game.alter_state()

        # Round 2 : 3- QS, 0- 2S, 1- KS, 2-9S
        game.move = 1
        game.alter_state()
        game.move = 8
        game.alter_state()
        game.move = 2
        game.alter_state()
        game.move = 5
        game.alter_state()

        # Player 0 is going to get all the trumps.
        # Round 3 : 0 - 3S, 1 - Ask Trump - 10H, 2-JH , 3- JS
        game.move = 7
        game.alter_state()
        game.move = "askForTrump"
        game.alter_state()
        game.move = 11
        game.alter_state()
        game.move = 14
        game.alter_state()
        game.move = 6
        game.alter_state()

        # Player 0 knows trumps are exhausted
        # Round 4 : 0 - 2D, 1 - KD, 2-JD , 3- QD
        game.move = 24
        game.alter_state()
        game.move = 18
        game.alter_state()
        game.move = 22
        game.alter_state()
        game.move = 17
        game.alter_state()

        # Player 0 knows trumps are exhausted
        # Round 5 : 0 - JC, 1 - 2C, 2-QC , 3- 9C
        game.move = 30
        game.alter_state()
        game.move = 32
        game.alter_state()
        game.move = 25
        game.alter_state()
        game.move = 29
        game.alter_state()

        # Player 1 starts
        # Round 6 : 1- 9H, 2 - AH, 3-3D , 0- 10S
        game.move = 13
        game.alter_state()
        game.move = 12
        game.alter_state()
        game.move = 23
        game.alter_state()
        game.move = 3
        game.alter_state()

        # Player 0 starts
        # Round 7 : 0 - AS, 1 - 10D, 2-KC , 3- AC
        game.move = 4
        game.alter_state()
        game.move = 19
        game.alter_state()
        game.move = 26
        game.alter_state()
        game.move = 28
        game.alter_state()

        # Player 0 starts
        # Round 8 : 0 - 3C, 1 - 10C, 2-9D , 3- AD
        game.move = 31
        game.alter_state()
        game.move = 27
        game.alter_state()
        game.move = 21
        game.alter_state()
        game.move = 20
        game.alter_state()

        b = 5
