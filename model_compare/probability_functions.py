import numpy as np
import pandas as pd
import operator
from numpy import exp
from numpy import linalg
from numpy import log as ln




def statistify(log_likelihoods):

    statistification = {
        'ln_mean': ln_mean(log_likelihoods),
        'ln_variance': ln_variance(log_likelihoods),
        'bootstrap': bootstrap(ln_mean, log_likelihoods, 10, operator.sub, linalg.norm)
    }
    return statistification


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
    ln_var = ln((exp(ln_samples - ln_C)).var()) + 2*ln_C
    return ln_var

def ln_normalize(ln_samples):
    ln_meany = ln_mean(ln_samples)
    result = ln_samples - ln_meany
    return result



def bootstrap(statistic, samples, num_iterations, metric, norm):
    truth = statistic(samples)

    estimates = (single_bootstrap(statistic, samples) for i in range(num_iterations))
    distance_vector = pd.Series((metric(estimate, truth) for estimate in estimates))
    result = norm(distance_vector)

    return result

def single_bootstrap(statistic, samples):
    n = len(samples)
    rand_samples = np.random.choice(samples, n, replace=True)
    estimate = statistic(rand_samples)
    return estimate