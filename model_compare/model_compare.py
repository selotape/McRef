import os
import pandas as pd

import logging
from model_compare.config_handler import ConfigHandler
from model_compare.data_prep import *
from model_compare.probability_functions import *


def model_compare(simulation='sample'):


    conf = ConfigHandler(simulation)

    setup_logging(conf)

    comb_stats, trace = conf.get_gphocs_data()
    comb_stats, trace = equate_lengths(comb_stats, trace)

    results_data = pd.DataFrame()
    results_data['ref_gene_likelihood'] = _calc_ref_gene_likelihood(comb_stats, trace, conf)
    results_data['hyp_gene_likelihood'] = trace['Gene-ld-ln']
    results_data['rbf_ratio'] = results_data['ref_gene_likelihood'] - results_data['hyp_gene_likelihood']
    results_data['harmonic_mean'] = -trace['Data-ld-ln']

    results_data = preprocess_data(results_data, conf)

    results_stats = {}
    for column in ['rbf_ratio', 'harmonic_mean']:
        logging.info("Starting analysis of column \'{}\'".format(column))
        analysis = analyze(results_data[column])
        results_stats[column] = analysis
        logging.info("Finished analysis of column \'{}\'".format(column))

    _save_results(results_data, results_stats, conf)
    logging.info("Done!")


def _calc_ref_gene_likelihood(comb_stats: pd.DataFrame, trace: pd.DataFrame, conf: ConfigHandler):
    theta_template, mig_rate_template, comb_num_coals_template, comb_leaf_num_coals_template, pop_num_coals_template, \
        comb_coal_stats_template, comb_leaf_coal_stats_template, pop_coal_stats_template, \
        comb_migband_mig_stats_template, comb_migband_num_migs_template = conf.get_column_name_templates()

    comb, comb_leaves, populations, migration_bands = conf.get_comb_pops_and_migs()
    theta_print_factor, mig_rate_print_factor = conf.get_data_config()

    thetas = trace[[theta_template.format(pop=p) for p in populations + [comb] + comb_leaves]].divide(
        theta_print_factor)

    comb_num_coals_column = [comb_num_coals_template.format(comb=comb)]
    comb_leaves_num_coals_columns = [comb_leaf_num_coals_template.format(comb=comb, leaf=l) for l in comb_leaves]
    pops_num_coals_columns = [pop_num_coals_template.format(pop=p) for p in populations]
    num_coal = comb_stats[comb_num_coals_column + comb_leaves_num_coals_columns + pops_num_coals_columns]

    comb_coal_stats_column = [comb_coal_stats_template.format(comb=comb)]
    comb_leaves_coal_stats_columns = [comb_leaf_coal_stats_template.format(comb=comb, leaf=l) for l in comb_leaves]
    pop_coal_stats_columns = [pop_coal_stats_template.format(pop=p) for p in populations]
    coal_stats = comb_stats[comb_coal_stats_column + comb_leaves_coal_stats_columns + pop_coal_stats_columns]
    mig_rate_columns = [mig_rate_template.format(migband=mb) for mb in migration_bands]
    num_migs_columns = [comb_migband_mig_stats_template.format(comb=comb, migband=mb) for mb in migration_bands]
    mig_stats_columns = [comb_migband_num_migs_template.format(comb=comb, migband=mb) for mb in migration_bands]
    mig_rates = trace[mig_rate_columns] / mig_rate_print_factor
    num_migs = comb_stats[num_migs_columns]
    mig_stats = comb_stats[mig_stats_columns]

    for df in (mig_rates, num_migs, mig_stats):
        df.columns = migration_bands

    objects_to_sum = pd.DataFrame()

    for pop in populations:
        pop_theta = thetas[theta_template.format(pop=pop)]
        pop_num_coal = num_coal[pop_num_coals_template.format(pop=pop)]
        pop_coal_stats = coal_stats[pop_coal_stats_template.format(pop=pop)]
        objects_to_sum[pop] = kingman_coalescent(pop_theta, pop_num_coal, pop_coal_stats)

    comb_theta = thetas[theta_template.format(pop=comb)]
    comb_num_coal = num_coal[comb_num_coals_template.format(comb=comb)]
    comb_coal_stats = coal_stats[comb_coal_stats_template.format(comb=comb)]
    objects_to_sum[comb] = kingman_coalescent(comb_theta, comb_num_coal, comb_coal_stats)

    for mig in migration_bands:
        objects_to_sum[mig] = kingman_migration(mig_rates[mig], num_migs[mig], mig_stats[mig])

    columns_to_sum = [comb] + populations + migration_bands
    ref_gene_likelihood = objects_to_sum[columns_to_sum].sum(axis=1)
    logging.info("Calculated reference genealogy likelihood")

    return ref_gene_likelihood


def _save_results(results_data: pd.DataFrame, results_stats: dict, conf: ConfigHandler):
    results_directory, results_path, likelihoods_plot_path, expectation_plot_path, harmonic_mean_plot_path, \
        summary_path = conf.get_results_paths()

    if not os.path.exists(results_directory):
        os.makedirs(results_directory)

    _save_plot(results_data[['ref_gene_likelihood', 'hyp_gene_likelihood']], likelihoods_plot_path,
               conf.simulation.split("/")[-1])
    _save_plot(results_data[['harmonic_mean']], harmonic_mean_plot_path, conf.simulation.split("/")[-1])
    _save_plot(results_data[['rbf_ratio']], expectation_plot_path, conf.simulation.split("/")[-1])

    with open(summary_path, 'w') as f:
        experiment_summary = _summarize(results_stats, conf)
        print(experiment_summary)
        f.write(experiment_summary)

    if conf.should_save_results():
        results_data.to_csv(results_path)


def _summarize(results_stats: dict, conf: ConfigHandler):
    comb, comb_leaves, populations, migration_bands = conf.get_comb_pops_and_migs()
    simulation_name = conf.simulation.split('/')[-1]
    formatted_leaves = ','.join(comb_leaves)
    formatted_pops = ','.join(populations)
    formatted_migbands = ','.join(migration_bands)
    intro_template = "Summary:\n" + \
                     "Simulation: %s\n" % simulation_name + \
                     "Comb: {0} | Comb Leaves: {1} | Populations: {2} | Migration Bands: {3}\n"
    intro = intro_template.format(comb, formatted_leaves, formatted_pops, formatted_migbands)

    results_string = []
    for column in sorted(list(results_stats.keys())):
        results_string.extend([column, ': ', str(results_stats[column]), '\n'])
    results_string = ''.join(results_string)

    return intro + results_string


def _save_plot(data_frame: pd.DataFrame, plot_save_path: str, plot_name: str):
    plot = data_frame.plot(title=plot_name)
    plot_figure = plot.get_figure()
    plot_figure.savefig(plot_save_path + ".line.png")

    hist = data_frame.plot.hist(alpha=0.5, bins=160, normed=True,
                                title=plot_name + ' histogram')
    hist_figure = hist.get_figure()
    hist_figure.savefig(plot_save_path + ".hist.png")


def setup_logging(conf):
    results_directory = conf.get_results_paths()[0]
    os.makedirs(results_directory, exist_ok=True)
    log_file = results_directory + '/model_compare.log'
    logging.basicConfig(level=logging.DEBUG,
                        format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
                        filename=log_file,
                        filemode='w')
