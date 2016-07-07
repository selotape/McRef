from model_compare.config_handler import ConfigHandler
import os
import pandas as pd
from model_compare.probability_functions import kingman_coalescent, E_P_G, kingman_migration


def model_compare(simulation='sample'):

    conf = ConfigHandler(simulation)

    clade_stats, trace = conf.get_data_frames()
    pop_infix, theta_prefix, num_coals_suffix, coal_stats_suffix, mig_rate_prefix, num_migs_suffix, mig_stats_suffix =\
        conf.get_prefixes()
    clades, populations, migration_bands = conf.get_clades_pops_and_migs()
    theta_print_factor, mig_rate_print_factor, tail_length = conf.get_data_config()

    thetas = trace[[theta_prefix + p for p in populations] + [theta_prefix + c for c in clades]].divide(theta_print_factor)
    num_coal = clade_stats[[c + num_coals_suffix for c in clades] + [p + pop_infix + num_coals_suffix for p in populations]]
    coal_stats = clade_stats[[c + coal_stats_suffix for c in clades] + [p + pop_infix + coal_stats_suffix for p in populations]]

    mig_rates = trace[[mig_rate_prefix + mig_band for mig_band in migration_bands]].divide(mig_rate_print_factor)
    num_migs = clade_stats[[mig_band + num_migs_suffix for mig_band in migration_bands]]
    mig_stats = clade_stats[[mig_band + mig_stats_suffix for mig_band in migration_bands]]

    rename_df_columns(data_frames=(mig_rates, num_migs, mig_stats), column_names=migration_bands)

    results = pd.DataFrame()

    results['hypothesis'] = trace['Gene-ld-ln']

    for pop in populations:
        results[pop + pop_infix] = kingman_coalescent(thetas[theta_prefix + pop], num_coal[pop + pop_infix + num_coals_suffix], coal_stats[pop + pop_infix + coal_stats_suffix])
    for clade in clades:
        results[clade] = kingman_coalescent(thetas[theta_prefix + clade], num_coal[clade + num_coals_suffix], coal_stats[clade + coal_stats_suffix])
    for mig in migration_bands:
        results[mig] = kingman_migration(mig_rates[mig], num_migs[mig], mig_stats[mig])

    columns_to_sum = clades + [pop + pop_infix for pop in populations] + migration_bands

    results['reference'] = results[columns_to_sum].sum(axis=1)
    results['E_ratio'] = results['reference'] - results['hypothesis']
    results.rbf = E_P_G(results['E_ratio'][-tail_length:])

    save_results(conf, results)


def rename_df_columns(data_frames, column_names):
    for df in data_frames:
        df.columns = column_names

def save_results(conf, results):

    tail_length = conf.get_data_config()[2]

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