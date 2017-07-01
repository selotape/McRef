from numpy import exp, sqrt, mean, random, log as ln
from pandas import Series

from util.log import module_logger

log = module_logger(__name__)


def kingman_coalescent(theta, num_coal, coal_stats) -> Series:
    result = num_coal * ln(2.0 / theta) - (coal_stats / theta)
    return result


def kingman_migration(mig_rate, num_migs, mig_stats) -> Series:
    result = num_migs * ln(mig_rate) - mig_stats * mig_rate
    return result


def analyze_columns(results_data, columns):
    log.info("Starting analysis of columns {}".format(columns))
    results_analysis = {
        column: analyze(results_data[column])
        for column in columns
    }
    log.info("Finished analysis of columns \'{}\'".format(columns))
    return results_analysis


def analyze(log_likelihoods) -> dict:
    """Performs a set of statistical analyses on a series of ln-likelihoods"""

    def norm(x):
        return sqrt(mean(x))

    def metric(x, y):
        return (x - y) ** 2

    bootstrap_iterations = 1000

    analysis = {
        'ln_mean': ln_mean(log_likelihoods),
        'bootstrap': bootstrap(ln_mean, log_likelihoods, bootstrap_iterations, metric, norm)
    }

    return analysis


def ln_mean(ln_samples) -> Series:
    """
    :param ln_samples: a series of tiny probabilities, with ln applied to them
    :return: ln of mean of probabilities
    """
    ln_c = max(ln_samples)
    n = len(ln_samples)
    ln_meany = ln_c + ln(sum(exp(ln_samples - ln_c))) - ln(n)
    return ln_meany


def bootstrap(statistic, samples, num_iterations, metric, norm):
    truth = statistic(samples)

    estimates = [_single_bootstrap(statistic, samples) for _ in range(num_iterations)]
    distance_vector = Series(metric(estimate, truth) for estimate in estimates)
    result = norm(distance_vector)

    return result


def _single_bootstrap(statistic, samples):
    rand_samples = random.choice(samples, len(samples), replace=True)
    estimate = statistic(rand_samples)
    return estimate
