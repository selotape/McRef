from math import log
import sys
import numpy as np
import pandas as pd
import configparser
import os



def model_compare(simulation='sample'):

    set_pandas()

    config = configparser.ConfigParser()
    config.read('config.ini')

    simulations_path = config.get('Input','simulations_path')
    simulation_path = simulations_path + '\\' + simulation

    validate_simulation(simulation_path)

    flat_stats_name = config.get('Input','flat_stats_file_name')
    flat_stats_path = simulation_path + '\\' + flat_stats_name
    flat_stats = pd.read_csv(flat_stats_path, sep='\t')

    trace_file_name = config.get('Input','trace_file_name')
    trace_path = simulation_path + '\\' + trace_file_name
    trace = pd.read_csv(trace_path, sep='\t')

    theta_column_name = config.get('Data','theta_column')
    print_factor = config.getfloat('Data','print_factor')
    expectation_tail_length = config.getint('Data','expectation_tail_length')

    results_directory_path = simulation_path + '\\' + config.get('Output','results_directory')

    trace_results_name = config.get('Output','trace_results_name')
    trace_results_path = results_directory_path + '\\' + trace_results_name

    summary_name = config.get('Output','summary_name')
    summary_path = results_directory_path + '\\' + summary_name

    likelihoods_plot_name = config.get('Output','likelihoods_plot_name')
    likelihoods_plot_path = results_directory_path + '\\' + likelihoods_plot_name

    expectation_plot_name = config.get('Output','expectation_plot_name')
    expectation_plot_path = results_directory_path + '\\' + expectation_plot_name




    flat_stats[theta_column_name] = trace[theta_column_name]
    flat_stats = flat_stats[['logPrior', 'coalStatFlat', 'numCoalFlat', theta_column_name, 'genealogyLogLikelihood']]
    flat_stats.columns = ['logPrior', 'time_stats', 'num_coal', theta_column_name, 'P_Z_M']

    flat_stats[theta_column_name] /= print_factor

    thetas = flat_stats[theta_column_name]
    num_coal = flat_stats['num_coal']
    time_stats = flat_stats['time_stats']

    flat_stats['P_Z_M0'] = P_Z_M0(thetas, num_coal, time_stats)

    flat_stats['E_ratio'] = flat_stats['P_Z_M'] - flat_stats['P_Z_M0'] # since likelihoods are stored in log-space, ratio is calculated using subtraction

    save_results(expectation_tail_length, likelihoods_plot_path, expectation_plot_path, flat_stats, trace_results_path, simulation, summary_path)


def save_results(expectation_tail_length, likelihoods_plot_path, expectation_plot_path, flat_stats, results_path, simulation_name, summary_path):

    flat_stats_tail = flat_stats[-expectation_tail_length:]
    save_plot(flat_stats_tail[['P_Z_M0', 'P_Z_M']], likelihoods_plot_path, simulation_name)
    save_plot(flat_stats_tail[['E_ratio']], expectation_plot_path, simulation_name)
    flat_stats.to_csv(results_path)
    E = E_P_Z(flat_stats_tail['E_ratio'])

    f = open(summary_path, 'w')
    f.write("E={0}\n".format(E))


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

def save_plot(data_frame, plot_save_path, plot_name=''):
    plot = data_frame.plot(title=plot_name)
    figure = plot.get_figure()
    figure.savefig(plot_save_path)


def validate_simulation(simulation_path):
    pass

if __name__ == "__main__":
    simulation_names = sys.argv[1:]
    for simulation in simulation_names:
        model_compare(simulation)