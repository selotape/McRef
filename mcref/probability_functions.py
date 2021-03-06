import numpy as np
import pandas as pd
from scipy.stats import gamma

from mcref.util.log import module_logger

log = module_logger(__name__)

BOOTSTRAP_ITERATIONS = 1000


def analyze_columns(results_data, columns):
    log.info("Starting analysis of columns %r" % columns)

    results_analysis = {}

    for col in columns:
        data = results_data[col]
        result = analyze(data)
        results_analysis[col] = result

    log.info("Finished analysis of columns %r" % columns)
    return results_analysis


def analyze(ln_likelihoods):
    """Performs a set of statistical analyses on a series of ln-likelihoods"""

    def norm(x):
        return np.sqrt(np.mean(x))

    def metric(x, y):
        return (x - y) ** 2

    return {
        'ln_mean': ln_mean(ln_likelihoods),
        'bootstrap': bootstrap(ln_mean, ln_likelihoods, BOOTSTRAP_ITERATIONS, metric, norm)
    }


def kingman_coalescent(theta, num_coal, coal_stats):
    return num_coal * np.log(2.0 / theta) - (coal_stats / theta)


def kingman_migration(mig_rate, num_migs, mig_stats):
    return num_migs * np.log(mig_rate) - mig_stats * mig_rate


def ln_mean(ln_samples):
    """
    :param ln_samples: a series of tiny probabilities, with ln applied to them
    :return: ln of mean of probabilities
    """
    ln_c = ln_samples.max()
    n = len(ln_samples)
    ln_meany = (ln_c + np.log(np.exp(ln_samples - ln_c).sum())) - np.log(n)
    return ln_meany


def bootstrap(statistic, samples, num_iterations, metric, norm):
    truth = statistic(samples)

    estimates = (_single_bootstrap(statistic, samples) for _ in range(num_iterations))
    distance_vector = pd.Series(metric(estimate, truth) for estimate in estimates)
    result = norm(distance_vector)

    return result


def _single_bootstrap(statistic, samples):
    rand_samples = samples.sample(len(samples), replace=True)
    estimate = statistic(rand_samples)
    return estimate


class PDF:

    @staticmethod
    def uniform(length):
        return 1.0 / length

    @staticmethod
    def gamma(sample, alpha, beta):
        """
        https://en.wikipedia.org/wiki/Gamma_distribution#Parameterizations
        https://stackoverflow.com/a/16964743/3052112
        """
        x = sample
        k = alpha
        theta = 1.0 / beta
        return gamma.pdf(x, a=k, scale=theta)
