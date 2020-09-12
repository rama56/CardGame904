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


########## SHAPING NATURE HANDS ###############

def shape_9_1(dist_heavy, dist_light, make_99_01_flag):
    heavy_sum = dist_heavy['Probability'].sum()
    light_sum = dist_light['Probability'].sum()
    heavy_mass = 0.9
    light_mass = 0.1

    if make_99_01_flag:
        heavy_mass = 0.999
        light_mass = 0.001

    heavy_factor = heavy_mass / heavy_sum
    light_factor = light_mass / light_sum
    dist_heavy['Probability'] = dist_heavy['Probability'] * heavy_factor
    dist_light['Probability'] = dist_light['Probability'] * light_factor

def shape_shrink_heavy_gap(dist_heavy, dist_light, constant_factor):
    # Add to heavy, a fraction (1/c_f) of heavy's gap.
    # Ex: H -> 0.8, L -> 0.2, const_factor = 5
    # => H -> 0.84, L - 0.16
    _gap = 1 - dist_heavy['Probability'].sum()
    _heavy_sum = dist_heavy['Probability'].sum()

    _factor = (_heavy_sum + _gap / constant_factor) / _heavy_sum
    dist_heavy['Probability'] = dist_heavy['Probability'] * _factor

    return dist_heavy, dist_light


def shape_shrink_light(dist_heavy, dist_light, constant_factor):
    # Reduce light's weight by dividing by a constant_factor

    dist_light['Probability'] = dist_light['Probability'] / constant_factor

    return dist_heavy, dist_light


# Multiply heavy set by constant_factor
def shape_boost_heavy(dist_heavy, dist_light, constant_factor):
    dist_heavy['Probability'] = dist_heavy['Probability'] * constant_factor


# Scale it up/down to sum up to 1
def normalize_distribution(dist):
    _new_sum = dist['Probability'].sum()
    dist['Probability'] = dist['Probability'] / _new_sum
    return dist
