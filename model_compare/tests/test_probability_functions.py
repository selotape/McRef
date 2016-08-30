import unittest
from pandas.util.testing import assert_frame_equal
import pandas as pd
import numpy as np
from model_compare.probability_functions import *

class test_probability_functions(unittest.TestCase):

    percision = 0.00000000000001

    def test_ln_mean(self): #Test ln_mean by using a different but equal calculation
        pass

    def test_bootstrapping(self):

        input = pd.Series(i for i in range(100))
        expected = 0.0
        actual = bootstrap(np.mean, input, 100000, operator.sub, np.mean)
        self.assertAlmostEqual(expected, actual, delta=0.01)

    def test_log_expectation(self):

        data = [1, 2, 3, 4]
        ln_data = pd.Series([np.log(x) for x in data])
        expected = np.log(pd.Series(data).mean())
        actual = ln_mean(ln_data)

        self.assertAlmostEqual(expected, actual, delta=self.percision)

        data = [112312367666666, 2234987654723423234, 3345345345999888777, 43453453333345, 12345678912345678, 2234987654723423234, 3345345345999888777, 43453453333345, 12345678912345678]
        ln_data = pd.Series([np.log(x) for x in data])
        expected = np.log(pd.Series(data).mean())
        actual = ln_mean(ln_data)

        self.assertAlmostEqual(expected, actual, delta=self.percision)

    def test_log_variance(self):

        data = [1, 2, 3, 4]
        ln_data = pd.Series([np.log(x) for x in data])
        expected = np.log(pd.Series(data).var())
        actual = ln_variance(ln_data)

        self.assertAlmostEqual(expected, actual, delta=self.percision)

        data = [112312367666666, 2234987654723423234, 3345345345999888777, 43453453333345, 12345678912345678, 2234987654723423234, 3345345345999888777, 43453453333345, 12345678912345678]
        ln_data = pd.Series([np.log(x) for x in data])
        expected = np.log(pd.Series(data).var())
        actual = ln_variance(ln_data)

        self.assertAlmostEqual(expected, actual, delta=self.percision)

    def test_kingman_coalescent(self):
        theta = 0.1
        num_coal = pd.Series([0, 1, 2])
        coal_stats = pd.Series([0.2, 0.3, 0.4])

        expected = pd.Series([-2.0, -0.0042677264460087016573197615798562765121, 1.9914645471079817085069407767150551080704])
        actual = kingman_coalescent(theta, num_coal, coal_stats)

        for i in range(len(expected)):
            self.assertAlmostEqual(expected[i], actual[i], delta=self.percision)

    def test_kingman_migration(self):
        mig_rate = 0.1

        num_migs = pd.Series([0, 1, 2])
        mig_stats = pd.Series([0.2, 0.3, 0.4])
        expected = pd.Series([-0.0200000000000000038857805861880478914827, -2.3325850929940452616051516088191419839859, -4.6451701859880909495359446736983954906464])
        actual = kingman_migration(mig_rate, num_migs, mig_stats)

        for i in range(len(expected)):
            self.assertAlmostEqual(expected[i], actual[i], delta=self.percision)


if __name__ == '__main__':
    unittest.main()