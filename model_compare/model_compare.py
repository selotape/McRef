import pandas as pd

from model_compare.probability_functions import *
from model_compare.util.config_handler import ConfigHandler
from model_compare.util.log import configure_logging, module_logger
from model_compare.util.panda_helpers import align_by_index
from model_compare.util.panda_helpers import copy_then_rename_columns, save_plot

log = module_logger(__name__)


def model_compare(simulation):
    conf = ConfigHandler(simulation)

    configure_logging(*conf.get_log_conf())
    try:
        _model_compare(conf)
    except:
        log.exception("Failure during _model_compare")
    log.info("===== Done! =====")


def clade_model_compare(simulation):
    conf = ConfigHandler(simulation)

    configure_logging(*conf.get_log_conf())
    try:
        _clade_model_compare(conf)
    except:
        log.exception("Failure during _clade_model_compare")
    log.info("===== Done! =====")


def _model_compare(conf: ConfigHandler):
    comb_stats, trace = conf.get_gphocs_data()
    comb_stats, trace = align_by_index(comb_stats, trace)
    results_data = _calculate_likelihoods(comb_stats, trace, conf)
    results_analysis = analyze_columns(results_data, ['rbf_ratio', 'harmonic_mean'])
    _save_results(results_data, results_analysis, conf)


def _clade_model_compare(conf: ConfigHandler):
    clade_stats, trace = conf.get_clade_gphocs_data()
    clade_stats, trace = align_by_index(clade_stats, trace)
    results_data = _clade_calculate_likelihoods(clade_stats, trace, conf)
    results_analysis = analyze_columns(results_data, ['rbf_ratio', 'harmonic_mean'])
    _clade_save_results(results_data, results_analysis, conf)


def _clade_calculate_likelihoods(comb_stats, trace, conf):
    results_data = pd.DataFrame()
    results_data['ref_gene_likelihood'] = _clade_calc_ref_gene_likelihood(comb_stats, trace, conf)
    results_data['hyp_gene_likelihood'] = trace['Gene-ld-ln']
    results_data['rbf_ratio'] = results_data['ref_gene_likelihood'] - results_data['hyp_gene_likelihood']
    results_data['harmonic_mean'] = -trace['Data-ld-ln']
    return results_data


def _calculate_likelihoods(comb_stats, trace, conf):
    results_data = pd.DataFrame()
    results_data['ref_gene_likelihood'] = _clade_calc_ref_gene_likelihood(comb_stats, trace, conf)
    results_data['hyp_gene_likelihood'] = trace['Gene-ld-ln']
    results_data['rbf_ratio'] = results_data['ref_gene_likelihood'] - results_data['hyp_gene_likelihood']
    results_data['harmonic_mean'] = -trace['Data-ld-ln']
    results_data['debug_ref_gene_likelihood'] = _debug_calc_ref_gene_likelihood(comb_stats, trace, conf)
    results_data['debug_coal_stats'], results_data['ref_coal_stats'] = _debug_calc_coal_stats(comb_stats, conf)
    return results_data


def _calc_ref_gene_likelihood(comb_stats: pd.DataFrame, trace: pd.DataFrame, conf: ConfigHandler):
    comb, comb_leaves, populations, migration_bands = conf.get_reference_tree()

    thetas = _get_clade_thetas(trace, conf)
    mig_rates = _get_clade_mig_rates(trace, conf)
    num_migs = _get_num_migs(comb_stats, conf)
    mig_stats = _get_mig_stats(comb_stats, conf)
    num_coal = _get_num_coals(comb_stats, conf)
    coal_stats = _get_coal_stats(comb_stats, conf)

    objects_to_sum = pd.DataFrame()
    for node in populations + [comb] + comb_leaves:
        objects_to_sum[node] = kingman_coalescent(thetas[node], num_coal[node], coal_stats[node])
    for mig in migration_bands:
        objects_to_sum[mig] = kingman_migration(mig_rates[mig], num_migs[mig], mig_stats[mig])

    debug_dir = conf.get_results_paths()[1]
    save_plot(objects_to_sum, debug_dir + '/pop_ln_ld', 'ronvis')

    ref_gene_likelihood = objects_to_sum.sum(axis=1)
    log.info("Calculated reference genealogy likelihood")

    return ref_gene_likelihood


def _clade_calc_ref_gene_likelihood(clade_stats: pd.DataFrame, trace: pd.DataFrame, conf: ConfigHandler):
    clade, populations, migration_bands = conf.get_clade_reference_tree()

    thetas = _get_clade_thetas(trace, conf)
    mig_rates = _get_clade_mig_rates(trace, conf)
    num_migs = _get_clade_num_migs(clade_stats, conf)
    mig_stats = _get_clade_mig_stats(clade_stats, conf)
    num_coal = _get_clade_num_coals(clade_stats, conf)
    coal_stats = _get_clade_coal_stats(clade_stats, conf)

    objects_to_sum = pd.DataFrame()
    for node in populations + [clade]:
        objects_to_sum[node] = kingman_coalescent(thetas[node], num_coal[node], coal_stats[node])
    for mig in migration_bands:
        objects_to_sum[mig] = kingman_migration(mig_rates[mig], num_migs[mig], mig_stats[mig])

    ref_gene_likelihood = objects_to_sum.sum(axis=1)
    log.info("Calculated reference genealogy likelihood")

    return ref_gene_likelihood


def _get_mig_rates(trace, conf: ConfigHandler):
    _, mig_rate_print_factor = conf.get_print_factors()
    _, _, migration_bands = conf.get_clade_reference_tree()
    mig_rate_template = conf.get_migrate_template()

    mig_rate_columns = [mig_rate_template.format(migband=mb) for mb in migration_bands]
    mig_rates = trace[mig_rate_columns] / mig_rate_print_factor
    mig_rates.columns = migration_bands
    return mig_rates


def _get_clade_mig_rates(trace, conf: ConfigHandler):
    return _get_mig_rates(trace, conf)


def _get_mig_stats(comb_stats, conf: ConfigHandler):
    comb, _, _, migration_bands = conf.get_reference_tree()
    comb_migband_num_migs_template = conf.get_num_migs_template()

    mig_stats_columns = [comb_migband_num_migs_template.format(comb=comb, migband=mb) for mb in migration_bands]
    mig_stats = comb_stats[mig_stats_columns]
    mig_stats.columns = migration_bands
    return mig_stats


def _get_clade_mig_stats(clade_stats, conf: ConfigHandler):
    _, _, migration_bands = conf.get_clade_reference_tree()
    clade_migband_num_migs_template = conf.get_clade_num_migs_template()

    mig_stats_columns = [clade_migband_num_migs_template.format(migband=mb) for mb in migration_bands]
    mig_stats = clade_stats[mig_stats_columns]
    mig_stats.columns = migration_bands
    return mig_stats


def _get_num_migs(comb_stats, conf: ConfigHandler):
    comb, _, _, migration_bands = conf.get_reference_tree()
    comb_migband_mig_stats_template = conf.get_mig_stats_template()

    num_migs_columns = [comb_migband_mig_stats_template.format(comb=comb, migband=mb) for mb in migration_bands]
    num_migs = comb_stats[num_migs_columns]
    num_migs.columns = migration_bands  # TODO unify column renaming methods
    return num_migs


def _get_clade_num_migs(clade_stats, conf: ConfigHandler):
    _, _, migration_bands = conf.get_clade_reference_tree()
    clade_migband_mig_stats_template = conf.get_clade_mig_stats_template()

    num_migs_columns = [clade_migband_mig_stats_template.format(migband=mb) for mb in migration_bands]
    num_migs = clade_stats[num_migs_columns]
    num_migs.columns = migration_bands  # TODO unify column renaming methods
    return num_migs


def _get_coal_stats(comb_stats, conf: ConfigHandler):
    comb, comb_leaves, populations, _ = conf.get_reference_tree()
    comb_coal_stats_template, comb_leaf_coal_stats_template, pop_coal_stats_template = conf.get_coal_stats_templates()

    columns_map = {comb_coal_stats_template.format(comb=comb): comb}
    columns_map.update({comb_leaf_coal_stats_template.format(comb=comb, leaf=l): l for l in comb_leaves})
    columns_map.update({pop_coal_stats_template.format(pop=p): p for p in populations})

    coal_stats = copy_then_rename_columns(comb_stats, columns_map)
    return coal_stats


def _get_clade_coal_stats(clade_stats, conf: ConfigHandler):
    clade, populations, _ = conf.get_clade_reference_tree()
    clade_coal_stats_template, pop_coal_stats_template = conf.get_clade_coal_stats_templates()

    columns_map = {clade_coal_stats_template.format(clade=clade): clade}
    columns_map.update({pop_coal_stats_template.format(pop=p): p for p in populations})

    coal_stats = copy_then_rename_columns(clade_stats, columns_map)
    return coal_stats


def _get_thetas(trace: pd.DataFrame, conf: ConfigHandler):
    comb, comb_leaves, populations, _ = conf.get_reference_tree()
    theta_print_factor, theta_template = conf.get_theta_setup()
    all_pops = populations + [comb] + comb_leaves
    theta_columns = [theta_template.format(pop=p) for p in all_pops]
    thetas = trace[theta_columns].divide(theta_print_factor).copy()  # type: pd.DataFrame
    columns_map = {theta_template.format(pop=p): p for p in all_pops}
    thetas.rename(columns=columns_map, inplace=True)
    return thetas


def _get_clade_thetas(trace: pd.DataFrame, conf: ConfigHandler):
    clade, populations, _ = conf.get_clade_reference_tree()
    theta_print_factor, theta_template = conf.get_theta_setup()
    all_pops = populations + [clade]
    theta_columns = [theta_template.format(pop=p) for p in all_pops]
    thetas = trace[theta_columns].divide(theta_print_factor).copy()  # type: pd.DataFrame
    columns_map = {theta_template.format(pop=p): p for p in all_pops}
    thetas.rename(columns=columns_map, inplace=True)
    return thetas


def _get_num_coals(comb_stats: pd.DataFrame, conf: ConfigHandler):
    comb, comb_leaves, populations, _ = conf.get_reference_tree()
    comb_leaf_num_coals_template, comb_num_coals_template, pop_num_coals_template = conf.get_num_coals_template()

    columns_map = {comb_num_coals_template.format(comb=comb): comb}
    columns_map.update({comb_leaf_num_coals_template.format(comb=comb, leaf=l): l for l in comb_leaves})
    columns_map.update({pop_num_coals_template.format(pop=p): p for p in populations})

    num_coal = copy_then_rename_columns(comb_stats, columns_map)
    return num_coal


def _get_clade_num_coals(clade_stats: pd.DataFrame, conf: ConfigHandler):
    clade, populations, _ = conf.get_clade_reference_tree()
    clade_num_coals_template, pop_num_coals_template = conf.get_clade_num_coals_template()

    columns_map = {clade_num_coals_template.format(clade=clade): clade}
    columns_map.update({pop_num_coals_template.format(pop=p): p for p in populations})

    num_coal = copy_then_rename_columns(clade_stats, columns_map)
    return num_coal


def _debug_calc_ref_gene_likelihood(comb_stats: pd.DataFrame, trace: pd.DataFrame, conf: ConfigHandler):
    (theta_template, mig_rate_template, comb_num_coals_template, comb_leaf_num_coals_template, pop_num_coals_template,
     comb_coal_stats_template, comb_leaf_coal_stats_template, pop_coal_stats_template,
     comb_migband_mig_stats_template, comb_migband_num_migs_template) = conf.get_column_name_templates()

    debug_pops = conf.get_debug_pops()
    theta_print_factor, mig_rate_print_factor = conf.get_print_factors()

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
    log.info("Calculated DEBUG reference genealogy likelihood")

    return debug_ref_gene_likelihood


def _debug_calc_coal_stats(comb_stats: pd.DataFrame, conf: ConfigHandler):
    (theta_template, mig_rate_template, comb_num_coals_template, comb_leaf_num_coals_template, pop_num_coals_template,
     comb_coal_stats_template, comb_leaf_coal_stats_template, pop_coal_stats_template,
     comb_migband_mig_stats_template, comb_migband_num_migs_template) = conf.get_column_name_templates()

    comb, comb_leaves, populations, migration_bands = conf.get_reference_tree()
    debug_pops = conf.get_debug_pops()

    debug_pop_coal_stats_columns = [pop_coal_stats_template.format(pop=p) for p in debug_pops]
    comb_coal_stats_column = [comb_coal_stats_template.format(comb=comb)]
    pop_coal_stats_columns = [pop_coal_stats_template.format(pop=p) for p in populations]
    comb_leaves_coal_stats_columns = [comb_leaf_coal_stats_template.format(comb=comb, leaf=l) for l in comb_leaves]

    debug_results_coal_stats = pd.DataFrame()
    debug_results_coal_stats['debug'] = comb_stats[debug_pop_coal_stats_columns].sum(axis=1)
    ref_coal_stats_columns = comb_coal_stats_column + pop_coal_stats_columns + comb_leaves_coal_stats_columns
    debug_results_coal_stats['ref'] = comb_stats[ref_coal_stats_columns].sum(axis=1)

    log.info("Calculated DEBUG coal stats")

    return debug_results_coal_stats['debug'], debug_results_coal_stats['ref']


def _save_results(results_data: pd.DataFrame, results_stats: dict, conf: ConfigHandler):
    (results_directory, debug_directory, results_path, likelihoods_plot_path,
     expectation_plot_path, harmonic_mean_plot_path, summary_path) = conf.get_results_paths()

    sim_name = conf.simulation.split("/")[-1]
    save_plot(results_data[['ref_gene_likelihood', 'hyp_gene_likelihood']], likelihoods_plot_path, sim_name)
    save_plot(results_data[['harmonic_mean']], harmonic_mean_plot_path, sim_name)
    save_plot(results_data[['rbf_ratio']], expectation_plot_path, sim_name)

    save_plot(results_data[['ref_gene_likelihood', 'debug_ref_gene_likelihood', 'hyp_gene_likelihood']], debug_directory + '/gene_likelihoods',
              sim_name)
    save_plot(results_data[['ref_coal_stats', 'debug_coal_stats']], debug_directory + '/coal_stats', sim_name)

    with open(summary_path, 'w') as f:
        experiment_summary = _summarize(results_stats, conf)
        log.info(experiment_summary)
        f.write(experiment_summary)

    if conf.should_save_results():
        results_data.to_csv(results_path)


def _clade_save_results(results_data: pd.DataFrame, results_stats: dict, conf: ConfigHandler):
    (results_directory, debug_directory, results_path, likelihoods_plot_path,
     expectation_plot_path, harmonic_mean_plot_path, summary_path) = conf.get_results_paths()

    sim_name = conf.simulation.split("/")[-1]
    save_plot(results_data[['ref_gene_likelihood', 'hyp_gene_likelihood']], likelihoods_plot_path, sim_name)
    save_plot(results_data[['harmonic_mean']], harmonic_mean_plot_path, sim_name)
    save_plot(results_data[['rbf_ratio']], expectation_plot_path, sim_name)

    with open(summary_path, 'w') as f:
        experiment_summary = _clade_summarize(results_stats, conf)
        log.info(experiment_summary)
        f.write(experiment_summary)

    if conf.should_save_results():
        results_data.to_csv(results_path)


def _summarize(results_stats: dict, conf: ConfigHandler):
    comb, comb_leaves, populations, migration_bands = conf.get_reference_tree()
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


def _clade_summarize(results_stats: dict, conf: ConfigHandler):
    clade, populations, migration_bands = conf.get_clade_reference_tree()
    simulation_name = conf.simulation.split('/')[-1]
    formatted_pops = ','.join(populations)
    formatted_migbands = ','.join(migration_bands)
    intro_template = "Summary:\n" + \
                     "Simulation: %s\n" % simulation_name + \
                     "Comb: {0} | Populations: {1} | Migration Bands: {2}\n"
    intro = intro_template.format(clade, formatted_pops, formatted_migbands)

    results_string = []
    for column in sorted(list(results_stats.keys())):
        results_string.extend([column, ': ', str(results_stats[column]), '\n'])
    results_string = ''.join(results_string)

    return intro + results_string
