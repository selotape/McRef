import numpy as np


def kingman_coalescent(theta, num_coal, time_stats):
    result = num_coal*np.log(2.0/theta) - (time_stats/theta)
    return result

def kingman_migration(mig_rate, num_migs, mig_stats):
    result = num_migs*np.log(mig_rate) - mig_stats*mig_rate;
    return result

def statistify(log_likelihoods): #TODO - rename
    log_mean = log_expectation(log_likelihoods)
    variance = log_variance(log_likelihoods)
    return log_mean, variance



def log_expectation(log_likelihoods):
    """
    :param log_likelihoods: a series of tiny probabilities, with ln applied to them
    :return: ln of mean of probabilities
    """

    a_max = max(log_likelihoods)
    b = log_likelihoods - a_max
    n = len(log_likelihoods)

    log_mean = a_max + np.log(sum(np.exp(b))) - np.log(n)

    return log_mean

def log_variance(log_likelihoods):
    mean = np.exp(log_expectation(log_likelihoods))
    mean_sqrd = np.exp(log_expectation(2*log_likelihoods))
    variance = mean_sqrd - mean**2
    return variance

def log_variance2(log_likelihoods):
    return 0

def log_variance3(log_likelihoods):
    likelihoods = np.exp(log_likelihoods)
    return likelihoods.var()