from mpmath import mp
import math


mp.dps = 20


def choose(n, k):
    return math.factorial(n) / (math.factorial(n-k) * math.factorial(k))


def choose_prob(n, k):
    ways_to_choose = choose(n, k)
    return 1 / ways_to_choose


def probability_prior(card_count):
    # ALl these shall be parameterized later if required.
    # c_total_cards = 16
    # c_hand_cards = 4
    # c_sig_card_count = 8  # Significant cards count - 16 | Having cards = 32
    # c_present_known = card_count
    # c_absent_known = c_sig_card_count - c_present_known

    c_total_cards = 32
    c_hand_cards = 8
    c_sig_card_count = 16    # Significant cards count - 16 | Having cards = 32
    c_present_known = card_count
    c_absent_known = c_sig_card_count - c_present_known
    player_count = 4    # Buckets

    # #All combinations - of a hand card set = 32 C 8, c_total_cards C c_hand_cards
    # for #Positive combinations - of a hand card set,
    # c_present_known of c_hand_cards are fixed. For the remaining (c_hand_cards - c_present_known) positions/vacancies,
    # (c_total_cards - c_absent_known - c_present_known) shall be used.
    # Thus, = (c_total_cards - c_absent_known - c_present_known) C ((c_hand_cards - c_present_known))
    # Prob() = #Pos / #All
    # Doing the math, it boils down to = 8 x 7 x .. (c_present_known elements) / 32 x 31 x ... 25

    deno = choose(c_total_cards, c_hand_cards)
    nume = choose(c_total_cards - c_sig_card_count, c_hand_cards - c_present_known)

    return nume/deno


# What an idiot I am !
def probability_prior_blasphemous(card_count):
    total_cards = 8      # Significant cards count - 16 | Having cards = 32
    player_count = 4    # Buckets

    out_count = total_cards - card_count

    prob_in = 1/player_count
    prob_out = 1 - prob_in

    # What an idiot I am !
    return (prob_in ** card_count) * (prob_out ** out_count)


# Bayes Theorem :
# Theta is the belief distribution. (of a parameter)
# X is the event observed (evidence), doesn't mean X happened. Just that we know for sure now if X happened or not.
# Posterior P(Theta | X) = Likelihood (X | Theta) *  Prior P(Theta) / Evidence's earlier probability P(X).

def calc_posterior(p_likelihood, p_evidence, p_prior):
    # TODO : Check p_evidence for 0
    return (p_likelihood * p_prior) / p_evidence


def get_mask(_card_ids_in_hand):
    mask = 0
    for i in _card_ids_in_hand:
        mask = mask + 2 ** i

    return mask