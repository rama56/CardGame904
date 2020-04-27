from unittest import TestCase

# Internal dependencies
from Intelligence import belief
from DataModel.card import *


class Test(TestCase):

    def test_initial_belief(self):
        initial_belief = belief.Belief(2)

        common_prior = initial_belief.common_prior
        # assert len(common_prior) == 39203

        vals = common_prior.values()
        total = sum(vals)

        assert 0.99 < total < 1.01

    def test_interim_prob(self):
        initial_belief = belief.Belief(2)

        cards = [Card(Number.Jack, Suite.Spade), Card(Number.Two, Suite.Hearts),
                 Card(Number.Three, Suite.Hearts), Card(Number.Ace, Suite.Hearts),
                 Card(Number.Jack, Suite.Hearts),
                 Card(Number.Queen, Suite.Dice), Card(Number.Nine, Suite.Clover)]

        # cards = [x.eng for x in cards]
        initial_belief.my_cards(cards)

        interim_prob = initial_belief.private_interim
        vals = interim_prob.values()
        total = sum(vals)
        assert 0.99 < total < 1.01

    def test_my_cards_2(self):
        # initial_belief = belief.Belief(2)

        cards = [Card(Number.Jack, Suite.Spade), Card(Number.Two, Suite.Hearts),
                 Card(Number.Three, Suite.Hearts), Card(Number.Ace, Suite.Hearts),
                 Card(Number.Jack, Suite.Hearts),
                 Card(Number.Queen, Suite.Dice), Card(Number.Nine, Suite.Clover)]

        # cards = [x.eng for x in cards]
        # initial_belief.my_cards(cards)

        # interim_prob = initial_belief.private_interim
        # vals = interim_prob.values()
        # total = sum(vals)
        # assert 0.99 < total < 1.01

        initial_belief_2 = belief.Belief(2)
        initial_belief_2.my_cards_2(cards)

        nature_1 = initial_belief_2.nature_hands[1]
        nature_2 = initial_belief_2.nature_hands[2]

        sum1 = sum(nature_1.values())
        sum2 = sum(nature_2.values())

        assert 0.99 < sum1 < 1.01
        assert 0.99 < sum2 < 1.01
