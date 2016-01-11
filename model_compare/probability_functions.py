import numpy as np


def P_Z_M0(theta, num_coal, time_stats):
    result = num_coal*np.log(2.0/theta) - (time_stats/theta)
    return result


def E_P_Z(likelihoods):

    """
    :param likelihoods: a series of tiny probabilities, with ln applied to them
    :return: mean of probabilities, with ln applied
    """

    a_max = max(likelihoods)
    b = likelihoods - a_max
    n = len(likelihoods)

    result = a_max + np.log(sum(np.exp(b))) - np.log(n)

    return result