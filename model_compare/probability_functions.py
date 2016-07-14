import numpy as np
from numpy import exp
from numpy import log


def kingman_coalescent(theta, num_coal, coal_stats):
    result = num_coal*np.log(2.0/theta) - (coal_stats / theta)
    return result

def kingman_migration(mig_rate, num_migs, mig_stats):
    result = num_migs*np.log(mig_rate) - mig_stats*mig_rate;
    return result

def statistify(log_likelihoods): #TODO - rename
    log_mean = log_expectation(log_likelihoods)
    log_var = log_variance(log_likelihoods)
    weighted_log_var = log_var - log_mean
    return log_mean, log_var, weighted_log_var


def log_expectation(ln_samples):
    """
    :param ln_samples: a series of tiny probabilities, with ln applied to them
    :return: ln of mean of probabilities
    """
    ln_C = max(ln_samples)
    n = len(ln_samples)

    log_mean = ln_C + log(sum(exp(ln_samples - ln_C))) - log(n)

    return log_mean

def log_variance(ln_samples):
    ln_C = max(ln_samples)

    log_var = log(exp(ln_samples - ln_C).var()) + 2*ln_C

    return log_var