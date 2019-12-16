from random import normalvariate, uniform, seed

from py_bucket_match.util.stat import get_variance


def simulate_preferences(teachers, buckets, alpha, n_pref_probabilities, buckets_factors=None):
    gen_utilities = {}
    for index, bucket in enumerate(buckets):
        gen_utilities[bucket] = normalvariate(0, 1) if not buckets_factors else buckets_factors[index]

    for teacher in teachers:
        std_utilities = {}
        variance = 1 if not buckets_factors else get_variance(buckets_factors)
        for bucket in buckets:
            std_utilities[bucket] = normalvariate(0, variance**0.5) * (1 - alpha) + gen_utilities[bucket] * alpha

        pref = sorted(std_utilities.keys(), key=lambda s: std_utilities[s], reverse=True)

        n_pref = weighted_choice([(v+1, p) for v, p in enumerate(n_pref_probabilities)])
        teacher.preferences = pref[:n_pref]


def weighted_choice(choices):
    total = sum(w for c, w in choices)
    r = uniform(0, total)
    upto = 0
    for c, w in choices:
        if upto + w >= r:
            return c
        upto += w
    assert False, "Should not get here"
