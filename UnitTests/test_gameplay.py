from unittest import TestCase
import timeit
from timeit import default_timer as timer

# Internal dependencies
from DataModel import game_state
from GameHost import session_helper
from Intelligence import belief
from DataModel.card import *
import logging

# logging.debug('This is a debug message')
# logging.info('This is an info message')
# logging.warning('This is a warning message')
# logging.error('This is an error message')
# logging.critical('This is a critical message')

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
        logging.getLogger().setLevel(logging.DEBUG)
        # CREATE INSTANCE OF GAME.

        start = timer()
        session_helper.precompute_beliefs()
        end = timer()
        elapsed = end - start   # 448 seconds

        logging.debug('Precomputation of beliefs completed. Time elapsed = ' + str(elapsed))

        start = timer()
        game = game_state.GameState(card_set_1)     # AVOID RANDOMNESS, HAVE DETERMINISTIC HANDS.
        end = timer()
        elapsed = end - start   # 32 seconds    8 seconds
        logging.debug('New game. Time elapsed = ' + str(elapsed))

        # Player 0 to bid. Let him bid 550 and others pass.
        start = timer()
        game.move = 550
        game.alter_state()

        for i in range(1, 4):
            game.move = -1
            game.alter_state()

        end = timer()
        elapsed = end - start   # 2.3 seconds
        logging.debug('Bidding phase. Time elapsed = ' + str(elapsed))

        # Player 0 to set Trump. (Sets Ace Spade)
        game.move = 4
        game.alter_state()

        # Round 1 : 3- 2H, 0- KH, 1- 3H, 2-QH
        logging.debug('Move 1 starts')
        start = timer()
        game.move = 16
        game.alter_state()
        end = timer()
        elapsed = end - start   # 75 seconds    17 seconds
        logging.debug('Move 1. Time elapsed = ' + str(elapsed))

        logging.debug('Move 2 starts')
        start = timer()
        game.move = 10
        game.alter_state()
        end = timer()
        elapsed = end - start   # 54 seconds    15 seconds
        logging.debug('Move 2. Time elapsed = ' + str(elapsed))

        logging.debug('Move 3 starts')
        start = timer()
        game.move = 15
        game.alter_state()
        end = timer()
        elapsed = end - start   # 41 seconds    13 seconds
        logging.debug('Move 3. Time elapsed = ' + str(elapsed))

        logging.debug('Move 4 starts')
        start = timer()
        game.move = 9
        game.alter_state()
        end = timer()
        elapsed = end - start   # 29 seconds    12 seconds
        logging.debug('Move 4. Time elapsed = ' + str(elapsed))

        # Round 2 : 3- QS, 0- 2S, 1- KS, 2-9S
        logging.debug('Move 5 starts')
        start = timer()
        game.move = 1
        game.alter_state()
        end = timer()
        elapsed = end - start   # 18 seconds
        logging.debug('Move 5. Time elapsed = ' + str(elapsed))

        start = timer()
        game.move = 8
        game.alter_state()
        end = timer()
        elapsed = end - start   # 15 seconds

        start = timer()
        game.move = 2
        game.alter_state()
        end = timer()
        elapsed = end - start   # 12 seconds

        start = timer()
        game.move = 5
        game.alter_state()
        end = timer()
        elapsed = end - start   # 12 seconds

        # Player 0 is going to get all the trumps.
        # Round 3 : 0 - 3S, 1 - Ask Trump - 10H, 2-JH , 3- JS
        start = timer()
        game.move = 7
        game.alter_state()
        end = timer()
        elapsed = end - start

        start = timer()
        game.move = "askForTrump"
        game.alter_state()
        end = timer()
        elapsed = end - start

        start = timer()
        game.move = 11
        game.alter_state()
        end = timer()
        elapsed = end - start

        start = timer()
        game.move = 14
        game.alter_state()
        end = timer()
        elapsed = end - start

        start = timer()
        game.move = 6
        game.alter_state()
        end = timer()
        elapsed = end - start

        # Player 0 knows trumps are exhausted
        # Round 4 : 0 - 2D, 1 - KD, 2-JD , 3- QD
        start = timer()
        game.move = 24
        game.alter_state()
        end = timer()
        elapsed = end - start

        start = timer()
        game.move = 18
        game.alter_state()
        end = timer()
        elapsed = end - start

        start = timer()
        game.move = 22
        game.alter_state()
        end = timer()
        elapsed = end - start

        start = timer()
        game.move = 17
        game.alter_state()
        end = timer()
        elapsed = end - start

        # Player 0 knows trumps are exhausted
        # Round 5 : 0 - JC, 1 - 2C, 2-QC , 3- 9C
        start = timer()
        game.move = 30
        game.alter_state()
        end = timer()
        elapsed = end - start

        start = timer()
        game.move = 32
        game.alter_state()
        end = timer()
        elapsed = end - start

        start = timer()
        game.move = 25
        game.alter_state()
        end = timer()
        elapsed = end - start

        start = timer()
        game.move = 29
        game.alter_state()
        end = timer()
        elapsed = end - start

        # Player 1 starts
        # Round 6 : 1- 9H, 2 - AH, 3-3D , 0- 10S
        start = timer()
        game.move = 13
        game.alter_state()
        end = timer()
        elapsed = end - start

        start = timer()
        game.move = 12
        game.alter_state()
        end = timer()
        elapsed = end - start

        start = timer()
        game.move = 23
        game.alter_state()
        end = timer()
        elapsed = end - start

        start = timer()
        game.move = 3
        game.alter_state()
        end = timer()
        elapsed = end - start

        # Player 0 starts
        # Round 7 : 0 - AS, 1 - 10D, 2-KC , 3- AC
        start = timer()
        game.move = 4
        game.alter_state()
        end = timer()
        elapsed = end - start

        start = timer()
        game.move = 19
        game.alter_state()
        end = timer()
        elapsed = end - start

        start = timer()
        game.move = 26
        game.alter_state()
        end = timer()
        elapsed = end - start

        start = timer()
        game.move = 28
        game.alter_state()
        end = timer()
        elapsed = end - start

        # Player 0 starts
        # Round 8 : 0 - 3C, 1 - 10C, 2-9D , 3- AD
        start = timer()
        game.move = 31
        game.alter_state()
        end = timer()
        elapsed = end - start

        start = timer()
        game.move = 27
        game.alter_state()
        end = timer()
        elapsed = end - start

        start = timer()
        game.move = 21
        game.alter_state()
        end = timer()
        elapsed = end - start

        start = timer()
        game.move = 20
        game.alter_state()
        end = timer()
        elapsed = end - start

        b = 5
