from model_compare.config_handler import ConfigHandler
import os
import pandas as pd
from model_compare.probability_functions import kingman_coalescent, kingman_migration, statistify


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

    results['hm_data_likelihood'] = 1/trace['Data-ld-ln']
    results['hyp_gene_likelihood'] = trace['Gene-ld-ln']

    for pop in populations:
        results[pop + pop_infix] = kingman_coalescent(thetas[theta_prefix + pop], num_coal[pop + pop_infix + num_coals_suffix], coal_stats[pop + pop_infix + coal_stats_suffix])
    for clade in clades:
        results[clade] = kingman_coalescent(thetas[theta_prefix + clade], num_coal[clade + num_coals_suffix], coal_stats[clade + coal_stats_suffix])
    for mig in migration_bands:
        results[mig] = kingman_migration(mig_rates[mig], num_migs[mig], mig_stats[mig])

    columns_to_sum = clades + [pop + pop_infix for pop in populations] + migration_bands

    results['ref_gene_likelihood'] = results[columns_to_sum].sum(axis=1)
    results['rbf_ratio'] = results['ref_gene_likelihood'] - results['hyp_gene_likelihood']
    results.rbf = statistify(results['rbf_ratio'])
    results.hm = statistify(results['hm_data_likelihood'])
    save_results(conf, results)


def rename_df_columns(data_frames, column_names):
    for df in data_frames:
        df.columns = column_names

def save_results(conf, results):

    tail_length = conf.get_data_config()[2]

    results_path, likelihoods_plot_path, expectation_plot_path, harmonic_mean_plot_path, summary_path = conf.get_results_paths()

    save_plot(results[-tail_length:][['ref_gene_likelihood', 'hyp_gene_likelihood']], likelihoods_plot_path, conf.simulation)
    save_plot(results[-tail_length:][['hm_data_likelihood']], harmonic_mean_plot_path, conf.simulation)
    save_plot(results[-tail_length:][['rbf_ratio']], expectation_plot_path, conf.simulation)

    results.to_csv(results_path)

    with open(summary_path, 'w') as f:
        f.write("Relative Bayes Factor  : Mean={0}, Variance={1}, Standard Deviation={2}\n".format(results.rbf[0], results.rbf[1], results.rbf[2]))
        f.write("Harmonic Mean Estimator: Mean={0}, Variance={1}, Standard Deviation={2}\n".format(results.hm[0], results.hm[1], results.hm[2]))


def save_plot(data_frame, plot_save_path, plot_name=''):
    plot = data_frame.plot(title=plot_name)
    figure = plot.get_figure()
    figure.savefig(plot_save_path)