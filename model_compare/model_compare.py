from model_compare.config_handler import ConfigHandler
import os
import pandas as pd
from model_compare.probability_functions import P_G_Mroot, E_P_G

def model_compare(simulation='sample'):

    conf = ConfigHandler(simulation)

    clade_stats, trace = conf.get_data_frames()
    pop_infix, theta_prefix, num_coals_suffix, coal_stats_suffix = conf.get_prefixes()
    clades, pops = conf.get_clades_and_pops()
    print_factor, tail_length = conf.get_data_config()

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
    results.rbf = E_P_G(results['E_ratio'][-tail_length:])

    save_results(conf, results)


def save_results(conf, results):

    print_factor, tail_length = conf.get_data_config()

    results_path, likelihoods_plot_path, expectation_plot_path, summary_path = conf.get_results_paths()

    save_plot(results[-tail_length:][['reference', 'hypothesis']], likelihoods_plot_path, conf.simulation)
    save_plot(results[-tail_length:][['E_ratio']], expectation_plot_path, conf.simulation)

    results.to_csv(results_path)

    with open(summary_path, 'w') as f:
        f.write("RBF={0}\n".format(results.rbf))


def save_plot(data_frame, plot_save_path, plot_name=''):
    plot = data_frame.plot(title=plot_name)
    figure = plot.get_figure()
    figure.savefig(plot_save_path)