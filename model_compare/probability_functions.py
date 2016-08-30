import numpy as np
import pandas as pd
from numpy import exp
from numpy import log as ln



def statistify(log_likelihoods): #TODO - rename
    ln_meany = ln_mean(log_likelihoods)
    ln_var = ln_variance(log_likelihoods)
    # bootstrap_var = bootstrap_variance(ln_mean, log_likelihoods, 100)
    # print(bootstrap_var)
    # exit()
    return ln_meany, ln_var


def kingman_coalescent(theta, num_coal, coal_stats):
    result = num_coal*ln(2.0/theta) - (coal_stats / theta)
    return result

def kingman_migration(mig_rate, num_migs, mig_stats):
    result = num_migs*ln(mig_rate) - mig_stats*mig_rate;
    return result



def ln_mean(ln_samples):
    """
    :param ln_samples: a series of tiny probabilities, with ln applied to them
    :return: ln of mean of probabilities
    """
    ln_C = max(ln_samples)
    n = len(ln_samples)
    ln_meany = ln_C + ln(sum(exp(ln_samples - ln_C))) - ln(n)
    return ln_meany

def ln_variance(ln_samples):
    ln_C = max(ln_samples)
    ln_var = ln(exp(ln_samples - ln_C).var()) + 2*ln_C
    return ln_var

def ln_var_norm(ln_samples):
    ln_var_normy = ln(exp(ln_normalize(ln_samples)).var())
    return ln_var_normy

def ln_normalize(ln_samples):
    ln_meany = ln_mean(ln_samples)
    result = ln_samples - ln_meany
    return result

def ln_normalize2(ln_samples):
#
# an overly complex way of calculating-
#     X - min(X)
#    ----------
#  max(X) - min(X)
# when X is given in log-scale and is humongous

    ln_min = min(ln_samples)
    ln_max = max(ln_samples)

    a = ln_min

    b1 = ln_samples - ln_min
    b2 = exp(b1)-1
    b = ln(b2)


    c = ln_min

    d1 = ln_max-ln_min
    d2 = exp(d1)-1
    d = ln(d2)

    result = a + b - c - d

    return result

def bootstrap_variance(statistic, samples, num_iterations):
    bootstrap_truth = statistic(samples)

    bootstrap_estimates = []
    for i in range(num_iterations):
        bootstrap_estimates.append(__single_bootstrap_estimate(samples, bootstrap_truth, statistic, ratio_metric))

    result = np.var(bootstrap_estimates)
    return result

def __single_bootstrap_estimate(samples, boost_truth, statistic, metric):
    n = len(samples)
    rand_samples = np.random.choice(samples, n, replace=True)
    boost_estimate = statistic(rand_samples)
    result = metric(boost_estimate, boost_truth)
    return result

def distance_metric(x, y):
    return abs(x - y)
def ratio_metric(x, y):
    return max(x, y) / min(x, y)