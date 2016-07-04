import configparser
import os
import pandas as pd
from model_compare.probability_functions import P_G_Mroot, E_P_G

config = configparser.ConfigParser()
config.read(os.path.dirname(os.path.realpath(__file__)) + '\\' + 'config.ini')

def model_compare(simulation='sample'):

    clade_stats, trace = get_data_frames(config, simulation)
    pop_infix, theta_prefix, num_coals_suffix, coal_stats_suffix = get_prefixes(config)
    clades, pops = get_clades_and_pops(config)


    print_factor = config.getfloat('Data','print_factor')
    expectation_tail_length = config.getint('Data','expectation_tail_length')

    thetas = trace[[theta_prefix + p for p in pops] + [theta_prefix + c for c in clades]].divide(print_factor)
    num_coal = clade_stats[[c + num_coals_suffix for c in clades] + [p + pop_infix + num_coals_suffix for p in pops]]
    coal_stats = clade_stats[[c + coal_stats_suffix for c in clades] + [p + pop_infix + coal_stats_suffix for p in pops]]

    results = pd.DataFrame()

    results['hypothesis'] = trace['Gene-ld-ln']

    for pop in pops:
        results[pop + pop_infix] = P_G_Mroot(thetas[theta_prefix + pop], num_coal[ pop + pop_infix + num_coals_suffix ], coal_stats[pop + pop_infix + coal_stats_suffix ])
    for clade in clades:
        results[clade] = P_G_Mroot(thetas[theta_prefix + clade], num_coal[clade + num_coals_suffix], coal_stats[clade + coal_stats_suffix])

    columns_to_sum = [clade for clade in clades] + [pop + pop_infix for pop in pops]

    results['reference'] = results[columns_to_sum].sum(axis=1)
    results['E_ratio'] = results['reference'] - results['hypothesis']
    results.rbf = E_P_G(results['E_ratio'][-expectation_tail_length:])

    save_results(simulation, results)

def get_simulation_path(config, simulation):
    simulations_path = config.get('Input', 'simulations_path')
    return simulations_path + '\\' + simulation


def get_clades_and_pops(config):
    clades = config.get('Clade','clades').split(',')
    pops = config.get('Clade', 'pops').split(',')

    #remove empty strings
    clades = list(filter(None, clades))
    pops = list(filter(None, pops))

    return clades, pops

def get_data_frames(config, simulation):
    simulation_path = get_simulation_path(config, simulation)

    clade_stats_name = config.get('Input','clade_stats_file_name')
    clade_stats_path = simulation_path + '\\' + clade_stats_name
    clade_stats = pd.read_csv(clade_stats_path, sep='\t')

    trace_file_name = config.get('Input','trace_file_name')
    trace_path = simulation_path + '\\' + trace_file_name
    trace = pd.read_csv(trace_path, sep='\t')

    return clade_stats, trace

def get_results_paths(config, simulation):
    simulation_path = get_simulation_path(config, simulation)

    results_directory_path = simulation_path + '\\' + config.get('Output','results_directory')
    results_path = results_directory_path + '\\' + config.get('Output','results_name')
    summary_path = results_directory_path + '\\' + config.get('Output','summary_name')
    likelihoods_plot_path = results_directory_path + '\\' + config.get('Output','likelihoods_plot_name')
    expectation_plot_path = results_directory_path + '\\' + config.get('Output','expectation_plot_name')

    return results_path, likelihoods_plot_path, expectation_plot_path, summary_path

def get_prefixes(config):
    pop_infix = config.get('Clade','pop_inffix')
    theta_prefix = config.get('Clade','theta_prefix')
    num_coals_suffix = config.get('Clade','num_coals_suffix')
    coal_stats_suffix = config.get('Clade','coal_stats_suffix')
    return pop_infix, theta_prefix, num_coals_suffix, coal_stats_suffix

def save_results(simulation, results):

    results_path, likelihoods_plot_path, expectation_plot_path, summary_path = get_results_paths(config, simulation)
    tail_length = config.getint('Data','expectation_tail_length')


    save_plot(results[-tail_length:][['reference', 'hypothesis']], likelihoods_plot_path, simulation)
    save_plot(results[-tail_length:][['E_ratio']], expectation_plot_path, simulation)

    results.to_csv(results_path)

    with open(summary_path, 'w') as f:
        f.write("RBF={0}\n".format(results.rbf))


def save_plot(data_frame, plot_save_path, plot_name=''):
    plot = data_frame.plot(title=plot_name)
    figure = plot.get_figure()
    figure.savefig(plot_save_path)