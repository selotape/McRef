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
    ln_var_normy = ln_var_norm(log_likelihoods)
    return ln_meany, ln_var, ln_var_normy

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
    ln_var = ln(exp(ln_samples - ln_C).var()) + 2*ln_C      # ln(var(X))
    return ln_var

def ln_var_norm(ln_samples):
    ln_meany = ln_mean(ln_samples)
    ln_var_normy = ln(exp(ln_samples - ln_meany).var())  # ln(var(X/mean(X)))
    return ln_var_normy