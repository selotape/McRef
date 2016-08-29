import numpy as np
from numpy import exp
from numpy import log as ln


def kingman_coalescent(theta, num_coal, coal_stats):
    result = num_coal*ln(2.0/theta) - (coal_stats / theta)
    return result

def kingman_migration(mig_rate, num_migs, mig_stats):
    result = num_migs*ln(mig_rate) - mig_stats*mig_rate;
    return result

def statistify(log_likelihoods): #TODO - rename
    ln_meany = ln_mean(log_likelihoods)
    ln_var = ln_variance(log_likelihoods)
    return ln_meany, ln_var

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