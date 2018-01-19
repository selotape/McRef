import operator
from unittest import TestCase, skip

import matplotlib as plt
import numpy as np
import pandas as pd
from matplotlib import pyplot

from model_compare.probability_functions import PDF, bootstrap, ln_mean, kingman_coalescent, kingman_migration
from model_compare.util.general_purpose import frange


class ProbabilityFunctionsTest(TestCase):
    precision = 0.00000000000001

    def test_ln_mean(self):  # Test ln_mean by using a different but equal calculation
        pass

    def test_bootstrapping(self, iterations=50000):
        bootstrap_input = pd.Series(np.arange(100))
        expected = 0.0
        actual = bootstrap(np.mean, bootstrap_input, iterations, operator.sub, np.mean)
        self.assertAlmostEqual(expected, actual, delta=0.1)

    def test_log_expectation(self):

        data = [1, 2, 3, 4]
        ln_data = pd.Series([np.log(x) for x in data])
        expected = np.log(pd.Series(data).mean())
        actual = ln_mean(ln_data)

        self.assertAlmostEqual(expected, actual, delta=self.precision)

        data = [112312367666666, 2234987654723423234, 3345345345999888777, 43453453333345, 12345678912345678,
                2234987654723423234, 3345345345999888777, 43453453333345, 12345678912345678]
        ln_data = pd.Series([np.log(x) for x in data])
        expected = np.log(pd.Series(data).mean())
        actual = ln_mean(ln_data)

        self.assertAlmostEqual(expected, actual, delta=self.precision)

    def test_kingman_coalescent(self):
        theta = 0.1
        num_coal = pd.Series([0, 1, 2])
        coal_stats = pd.Series([0.2, 0.3, 0.4])

        expected = pd.Series(
            [-2.0, -0.0042677264460087016573197615798562765121, 1.9914645471079817085069407767150551080704])
        actual = kingman_coalescent(theta, num_coal, coal_stats)

        for i in range(len(expected)):
            self.assertAlmostEqual(expected[i], actual[i], delta=self.precision)

    def test_kingman_migration(self):
        mig_rate = 0.1

        num_migs = pd.Series([0, 1, 2])
        mig_stats = pd.Series([0.2, 0.3, 0.4])
        expected = pd.Series([-0.0200000000000000038857805861880478914827, -2.3325850929940452616051516088191419839859,
                              -4.6451701859880909495359446736983954906464])
        actual = kingman_migration(mig_rate, num_migs, mig_stats)

        for i in range(len(expected)):
            self.assertAlmostEqual(expected[i], actual[i], delta=self.precision)

    @skip("Plz run manually and assert plot matches https://en.wikipedia.org/wiki/Gamma_distribution#/media/File:Gamma_distribution_pdf.svg")
    def test_gamma_pdf(self):
        k_theta_params = [(1.0, 2.0), (2.0, 2.0), (3.0, 2.0), (5.0, 1.0), (9.0, 0.5), (7.5, 1.0), (0.5, 1.0)]

        fmt = 'k = %.1f, θ = %.1f'

        data = {fmt % (k, th): list(PDF.gamma(x, k, 1.0 / th) for x in frange(0, 20, 0.1)) for k, th in k_theta_params}

        df = pd.DataFrame(data)

        df.plot()
        plt.pyplot.show()
