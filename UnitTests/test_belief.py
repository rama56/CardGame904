from unittest import TestCase

# Internal dependencies
from Intelligence import belief
from DataModel.card import *
from Intelligence import common_knowledge


class Test(TestCase):

    def test_initial_belief(self):
        initial_belief = belief.Belief(2)

        common_prior = initial_belief.common_prior
        # assert len(common_prior) == 39203

        vals = common_prior.values()
        total = sum(vals)

        assert 0.99 < total < 1.01

    def test_my_cards_2(self):
        # initial_belief = belief.Belief(2)

        cards = [Card(Number.Jack, Suite.Spade), Card(Number.Two, Suite.Hearts),
                 Card(Number.Three, Suite.Hearts), Card(Number.Ace, Suite.Hearts),
                 Card(Number.Jack, Suite.Hearts),
                 Card(Number.Queen, Suite.Dice), Card(Number.Nine, Suite.Clover)]

        initial_belief_2 = belief.Belief(2)
        initial_belief_2.my_hand_cards(cards)

        nature_1 = initial_belief_2.nature_hands[1]
        nature_2 = initial_belief_2.nature_hands[2]

        sum1 = sum(nature_1.values())
        sum2 = sum(nature_2.values())

        assert 0.99 < sum1 < 1.01
        assert 0.99 < sum2 < 1.01

    # CARD STRENGTHS

    def test_cardset_strengths(self):
        # [2S, 3S, AS, 10S  |  KH | 2D | 3C, JC]

        f2 = [-1, 3, 2.5, 2, 1.5, 1.5, 1.5, 1.2]        # [-1, 2, 2, 2, 2, 2, 2, 2]
        cards_engs = ['TwoSpade', 'ThreeSpade', 'AceSpade', 'TenSpade',
                 'KingHearts',
                 'TwoDice',
                 'ThreeClover', 'JackClover']

        cards = [get_card_from_eng(x) for x in cards_engs]
        value1, bucket_strengths1 = belief.get_strength(cards)
        value1a, bucket_strengths1a = belief.get_strength(cards, f2)

        # Replace KingHearts with KingSpade (same value, but an extra trump)
        cards_engs = ['TwoSpade', 'ThreeSpade', 'AceSpade', 'TenSpade', 'KingSpade',
                      'TwoDice',
                      'ThreeClover', 'JackClover']

        cards = [get_card_from_eng(x) for x in cards_engs]
        value2, bucket_strengths2 = belief.get_strength(cards)
        value1ab, bucket_strengths1ab = belief.get_strength(cards, f2)

        # 904 capable
        cards_engs = ['TwoSpade', 'ThreeSpade', 'NineSpade', 'AceSpade', 'TenSpade', 'KingSpade', 'QueenSpade',
                      'TwoDice']

        cards = [get_card_from_eng(x) for x in cards_engs]
        value3, bucket_strengths3 = belief.get_strength(cards)
        value1c, bucket_strengths1c = belief.get_strength(cards, f2)

        # 700 capable
        cards_engs = ['TwoSpade', 'ThreeSpade', 'NineSpade', 'KingSpade', 'QueenSpade',
                      'TwoDice',
                      'ThreeClover', 'JackClover']

        cards = [get_card_from_eng(x) for x in cards_engs]
        value4, bucket_strengths4 = belief.get_strength(cards)
        value1d, bucket_strengths1d = belief.get_strength(cards, f2)

        # from a random example
        cards_engs = ['TwoSpade', 'JackSpade', 'TenSpade',
                      'TwoHearts', 'NineHearts', 'TwoDice',
                      'ThreeClover', 'AceClover']
        cards = [get_card_from_eng(x) for x in cards_engs]
        value6, bucket_strengths6 = belief.get_strength(cards)
        value1f, bucket_strengths1f = belief.get_strength(cards, f2)

        # strong without Two
        cards_engs = ['TwoSpade',
                      'ThreeHearts', 'JackHearts', 'NineHearts', 'AceHearts', 'KingHearts',
                      'TwoDice',
                      'ThreeClover']
        cards = [get_card_from_eng(x) for x in cards_engs]
        value7, bucket_strengths7 = belief.get_strength(cards)
        value1g, bucket_strengths1g = belief.get_strength(cards, f2)

        # strong with no support
        cards_engs = ['KingSpade',
                      'TwoHearts', 'JackHearts', 'NineHearts', 'AceHearts', 'KingHearts',
                      'JackDice',
                      'JackClover']
        cards = [get_card_from_eng(x) for x in cards_engs]
        value8, bucket_strengths8 = belief.get_strength(cards)
        value1h, bucket_strengths1h = belief.get_strength(cards, f2)

        # shuffle
        cards = get_shuffled_deck()[0:8]
        cards_engs2 = [x.eng for x in cards]
        cards = [get_card_from_eng(x) for x in cards_engs2]
        value5, bucket_strengths5 = belief.get_strength(cards)
        value1e, bucket_strengths1e = belief.get_strength(cards, f2)

        a = 2

    def test_bid_belief_change(self):
        cards_engs = ['TwoSpade', 'ThreeSpade', 'AceSpade', 'TenSpade',
                      'KingHearts',
                      'TwoDice',
                      'ThreeClover', 'JackClover']

        cards = [get_card_from_eng(x) for x in cards_engs]

        _belief = belief.Belief(0)
        ck = common_knowledge.CommonKnowledge()
        ck.set_common_prior()

        _belief.my_hand_cards(cards, ck)

        _belief.bid_strength = [None, (520, 560), (0, 520), (700, 740)]

        _belief.bidding_over()

        top_about_1 = _belief.nature_hands[1].nlargest(30, 'Probability', keep='first')
        top_about_2 = _belief.nature_hands[2].nlargest(30, 'Probability', keep='first')
        top_about_3 = _belief.nature_hands[3].nlargest(30, 'Probability', keep='first')

    def test_bid_belief_change_hands_and_cards(self):
        cards_engs = ['TwoSpade', 'ThreeSpade', 'AceSpade', 'TenSpade',
                      'KingHearts',
                      'TwoDice',
                      'ThreeClover', 'JackClover']

        cards = [get_card_from_eng(x) for x in cards_engs]

        # bid_val = belief.get_strength_from_cardset(car)

        _belief = belief.Belief(0)
        ck = common_knowledge.CommonKnowledge()
        ck.set_common_prior()

        _belief.my_hand_cards(cards, ck)

        _belief.bid_strength = [None, (0, 500), (0, 500), (700, 740)]

        _belief.bidding_over()

        top_about_1 = _belief.nature_hands[1].nlargest(30, 'Probability', keep='first')
        top_about_2 = _belief.nature_hands[2].nlargest(30, 'Probability', keep='first')
        top_about_3 = _belief.nature_hands[3].nlargest(30, 'Probability', keep='first')

        x = 5

