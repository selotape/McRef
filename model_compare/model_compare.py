import os

import pandas as pd

from model_compare.data_prep import *
from model_compare.probability_functions import *
from model_compare.util.config_handler import ConfigHandler
from model_compare.util.log import configure_logging, module_logger
from model_compare.util.plotter import save_plot

logger = module_logger(__name__)


def model_compare(simulation='sample'):
    conf = ConfigHandler(simulation)

    configure_logging(conf)
    try:
        _model_compare(conf)
    except:
        logger.exception("Failure during _model_compare")
    logger.info("===== Done! =====")


def _model_compare(conf):
    comb_stats, trace = conf.get_gphocs_data()
    comb_stats, trace = equate_lengths(comb_stats, trace)
    results_data = pd.DataFrame()

    results_data['ref_gene_likelihood'] = _calc_ref_gene_likelihood(comb_stats, trace, conf)
    results_data['hyp_gene_likelihood'] = trace['Gene-ld-ln']
    results_data['rbf_ratio'] = results_data['ref_gene_likelihood'] - results_data['hyp_gene_likelihood']
    results_data['harmonic_mean'] = -trace['Data-ld-ln']

    results_data['debug_ref_gene_likelihood'] = _debug_calc_ref_gene_likelihood(comb_stats, trace, conf)
    results_data['debug_coal_stats'], results_data['ref_coal_stats'] = _debug_calc_coal_stats(comb_stats, trace, conf)
    results_data = clean_results(results_data, conf)
    results_stats = {}
    for column in ['rbf_ratio', 'harmonic_mean']:
        logger.info("Starting analysis of column \'{}\'".format(column))
        analysis = analyze(results_data[column])
        results_stats[column] = analysis
        logger.info("Finished analysis of column \'{}\'".format(column))
    _save_results(results_data, results_stats, conf)


def _calc_ref_gene_likelihood(comb_stats: pd.DataFrame, trace: pd.DataFrame, conf: ConfigHandler):
    (theta_template, mig_rate_template, comb_num_coals_template, comb_leaf_num_coals_template, pop_num_coals_template,
     comb_coal_stats_template, comb_leaf_coal_stats_template, pop_coal_stats_template,
     comb_migband_mig_stats_template, comb_migband_num_migs_template) = conf.get_column_name_templates()

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

    debug_dir = conf.get_results_paths()[1]
    save_plot(objects_to_sum[columns_to_sum], debug_dir+'/pop_ln_ld', 'ronvis')

    ref_gene_likelihood = objects_to_sum[columns_to_sum].sum(axis=1)
    logger.info("Calculated reference genealogy likelihood")

    return ref_gene_likelihood


def _debug_calc_ref_gene_likelihood(comb_stats: pd.DataFrame, trace: pd.DataFrame, conf: ConfigHandler):
    (theta_template, mig_rate_template, comb_num_coals_template, comb_leaf_num_coals_template, pop_num_coals_template,
     comb_coal_stats_template, comb_leaf_coal_stats_template, pop_coal_stats_template,
     comb_migband_mig_stats_template, comb_migband_num_migs_template) = conf.get_column_name_templates()

    debug_pops = conf.get_debug_pops()
    theta_print_factor, mig_rate_print_factor = conf.get_data_config()

    debug_thetas = trace[[theta_template.format(pop=p) for p in debug_pops]].divide(theta_print_factor)

    debug_pops_num_coals_columns = [pop_num_coals_template.format(pop=p) for p in debug_pops]
    debug_num_coal = comb_stats[debug_pops_num_coals_columns]

    debug_pop_coal_stats_columns = [pop_coal_stats_template.format(pop=p) for p in debug_pops]
    debug_coal_stats = comb_stats[debug_pop_coal_stats_columns]

    debug_objects_to_sum = pd.DataFrame()

    for debug_pop in debug_pops:
        debug_pop_theta = debug_thetas[theta_template.format(pop=debug_pop)]
        debug_pop_num_coal = debug_num_coal[pop_num_coals_template.format(pop=debug_pop)]
        debug_pop_coal_stats = debug_coal_stats[pop_coal_stats_template.format(pop=debug_pop)]
        debug_objects_to_sum[debug_pop] = kingman_coalescent(debug_pop_theta, debug_pop_num_coal, debug_pop_coal_stats)

    debug_columns_to_sum = debug_pops
    debug_ref_gene_likelihood = debug_objects_to_sum[debug_columns_to_sum].sum(axis=1)
    logger.info("Calculated DEBUG reference genealogy likelihood")

    return debug_ref_gene_likelihood


def _debug_calc_coal_stats(comb_stats: pd.DataFrame, trace: pd.DataFrame, conf: ConfigHandler):
    (theta_template, mig_rate_template, comb_num_coals_template, comb_leaf_num_coals_template, pop_num_coals_template,
     comb_coal_stats_template, comb_leaf_coal_stats_template, pop_coal_stats_template,
     comb_migband_mig_stats_template, comb_migband_num_migs_template) = conf.get_column_name_templates()

    comb, comb_leaves, populations, migration_bands = conf.get_comb_pops_and_migs()
    debug_pops = conf.get_debug_pops()

    debug_pop_coal_stats_columns = [pop_coal_stats_template.format(pop=p) for p in debug_pops]
    comb_coal_stats_column = [comb_coal_stats_template.format(comb=comb)]
    pop_coal_stats_columns = [pop_coal_stats_template.format(pop=p) for p in populations]
    comb_leaves_coal_stats_columns = [comb_leaf_coal_stats_template.format(comb=comb, leaf=l) for l in comb_leaves]

    debug_results_coal_stats = pd.DataFrame()
    debug_results_coal_stats['debug'] = comb_stats[debug_pop_coal_stats_columns].sum(axis=1)
    ref_coal_stats_columns = comb_coal_stats_column + pop_coal_stats_columns + comb_leaves_coal_stats_columns
    debug_results_coal_stats['ref'] = comb_stats[ref_coal_stats_columns].sum(axis=1)

    logger.info("Calculated DEBUG coal stats")

    return debug_results_coal_stats['debug'], debug_results_coal_stats['ref']


def _save_results(results_data: pd.DataFrame, results_stats: dict, conf: ConfigHandler):
    (results_directory, debug_directory, results_path, likelihoods_plot_path,
     expectation_plot_path, harmonic_mean_plot_path, summary_path) = conf.get_results_paths()


    sim_name = conf.simulation.split("/")[-1]
    save_plot(results_data[['ref_gene_likelihood', 'hyp_gene_likelihood']], likelihoods_plot_path, sim_name)
    save_plot(results_data[['harmonic_mean']], harmonic_mean_plot_path, sim_name)
    save_plot(results_data[['rbf_ratio']], expectation_plot_path, sim_name)

    save_plot(results_data[['ref_gene_likelihood', 'debug_ref_gene_likelihood', 'hyp_gene_likelihood']], debug_directory + '/gene_likelihoods', sim_name)
    save_plot(results_data[['ref_coal_stats', 'debug_coal_stats']], debug_directory + '/coal_stats', sim_name)

    with open(summary_path, 'w') as f:
        experiment_summary = _summarize(results_stats, conf)
        logger.info(experiment_summary)
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


