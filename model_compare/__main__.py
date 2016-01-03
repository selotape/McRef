from math import log

import numpy as np
import pandas as pd
import configparser
from functools import reduce
from operator import mul

### SETUP ###

def main():
    set_pandas()

    config = configparser.ConfigParser()
    config.read('config.ini')
    simulation_name = config.get('Simulation', 'name')
    theta_column_name = config.get('Simulation','theta_column')
    print_factor = config.getfloat('Simulation','print_factor')

    simulations_path = config.get('Simulation','simulations_path')
    trace_file_name = config.get('Simulation','trace_file_name')
    flat_stats_file_name = config.get('Simulation','flat_stats_file_name')


    flat_stats_path = simulations_path + '\\' + simulation_name + '\\' + flat_stats_file_name
    flat_stats = pd.read_csv(flat_stats_path, sep='\t')

    trace_path = simulations_path + '\\' + simulation_name + '\\' + trace_file_name
    trace = pd.read_csv(trace_path, sep='\t')

    flat_stats[theta_column_name] = trace[theta_column_name]


    flat_stats = flat_stats[['logPrior', 'coalStatFlat', 'numCoalFlat', theta_column_name, 'genealogyLogLikelihood']]
    flat_stats.columns = ['logPrior', 'time_stats', 'num_coal', theta_column_name, 'P_Z_M']


    flat_stats[theta_column_name] /= print_factor

    thetas = flat_stats[theta_column_name]
    num_coal = flat_stats['num_coal']
    time_stats = flat_stats['time_stats']

    flat_stats['P_Z_M0'] = P_Z_M0(thetas, num_coal, time_stats)

    flat_stats[['P_Z_M0', 'P_Z_M']].plot(title=simulation_name)

    E_P_Z_M = E_P_Z(flat_stats['P_Z_M'][-100:])
    E_P_Z_M0 = E_P_Z(flat_stats['P_Z_M0'][-100:])

    print("E_P_Z_M={0},E_P_Z_M0={1}, E/E={2}".format(E_P_Z_M, E_P_Z_M0, E_P_Z_M/E_P_Z_M0))

def set_pandas():
    pd.set_option('display.mpl_style', 'default')
    pd.set_option('display.width', 5000)
    pd.set_option('display.max_columns', 60)

def P_Z_M0(theta, num_coal, time_stats):
    result = num_coal*np.log(2.0/theta) - (time_stats/theta)
    return result

def E_P_Z(likelihoods):

    a_max = max(likelihoods)
    b = likelihoods - a_max
    n = len(likelihoods)

    result = a_max + log(sum(np.exp(b))) - log(n)

    return result



if __name__ == "__main__":
    main()