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
    ln_meany = ln_mean(log_likelihoods)
    ln_var = ln_variance(log_likelihoods)
    return ln_meany, ln_var, ln_var - ln_meany


def ln_mean(ln_samples):
    """
    :param ln_samples: a series of tiny probabilities, with ln applied to them
    :return: ln of mean of probabilities
    """
    ln_C = max(ln_samples)
    n = len(ln_samples)

    ln_meany = ln_C + log(sum(exp(ln_samples - ln_C))) - log(n)

    return ln_meany


def ln_variance(ln_samples):
    ln_C = max(ln_samples)

    ln_var = log(exp(ln_samples - ln_C).var()) + 2*ln_C # ln(var(X))
    var_ln =  ln_samples.var()                          # var(ln(X))
    ln_var_norm = log(exp(ln_samples - ln_C).var())     # ln(var(X/C)) ; C:=max(X)
    var_ln_norm = (ln_samples/ln_C).var()               # var(ln(X)/ln(C)) ; C:=max(X)
    #todotodotodo                                       # var(logistic/softmax/sigmoid(X))
    ln_var_over_mean = ln_var - ln_mean(ln_samples)

    print("ln_var={0}, var_ln={1}, ln_var_norm={2}, var_ln_norm={3}, ln_var_over_mean={4}".format(ln_var, var_ln, ln_var_norm, var_ln_norm, ln_var_over_mean))

    return ln_var