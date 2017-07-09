import pandas as pd

from model_compare.probability_functions import *
from model_compare.util.config_handler import ConfigHandler
from model_compare.util.log import configure_logging, module_logger
from model_compare.util.panda_helpers import copy_then_rename_columns, save_plot

log = module_logger(__name__)


def model_compare(simulation, is_clade):
    conf = ConfigHandler(simulation, is_clade)

    configure_logging(*conf.get_log_conf())
    try:
        if is_clade:
            _clade_model_compare(conf)
        else:
            _comb_model_compare(conf)
    except:
        log.exception("Failure during model_compare")
    log.info("===== Done! =====")


def _comb_model_compare(conf: ConfigHandler):
    comb_stats = conf.load_comb_data()
    trace = conf.load_trace_data()
    hyp_stats = conf.load_hyp_data()

    results_data = _calculate_comb_likelihoods(comb_stats, hyp_stats, trace, conf)

    if conf.is_debug_enabled():
        _calc_hyp_gene_likelihood(results_data, hyp_stats, trace, conf)
        _debug_coal_stats(results_data, comb_stats, hyp_stats, conf)

    results_analysis = analyze_columns(results_data, ['rbf_ratio', 'harmonic_mean'])
    experiment_summary = _comb_summarize(results_analysis, conf)
    _save_results(results_data, experiment_summary, conf)


def _clade_model_compare(conf: ConfigHandler):
    clade_stats = conf.load_clade_data()
    trace = conf.load_trace_data()
    hyp_stats = conf.load_hyp_data()

    results_data = _calculate_clade_likelihoods(clade_stats, hyp_stats, trace, conf)

    if conf.is_debug_enabled():
        _calc_hyp_gene_likelihood(results_data, hyp_stats, trace, conf)
        _debug_coal_stats(results_data, clade_stats, hyp_stats, conf)

    results_analysis = analyze_columns(results_data, ['rbf_ratio', 'harmonic_mean'])
    experiment_summary = _clade_summarize(results_analysis, conf)
    _save_results(results_data, experiment_summary, conf)


def _calculate_comb_likelihoods(comb_stats, hyp_stats, trace, conf: ConfigHandler):
    results_data = pd.DataFrame()
    results_data['ref_gene_likelihood'] = _calc_comb_ref_gene_likelihood(comb_stats, hyp_stats, trace, conf)
    results_data['hyp_gene_likelihood'] = trace['Gene-ld-ln']
    results_data['rbf_ratio'] = results_data['ref_gene_likelihood'] - results_data['hyp_gene_likelihood']
    results_data['harmonic_mean'] = -trace['Data-ld-ln']

    return results_data


def _calculate_clade_likelihoods(clade_stats, hyp_stats, trace, conf):
    results_data = pd.DataFrame()
    results_data['ref_gene_likelihood'] = _calc_clade_ref_gene_likelihood(clade_stats, hyp_stats, trace, conf)
    results_data['hyp_gene_likelihood'] = trace['Gene-ld-ln']
    results_data['rbf_ratio'] = results_data['ref_gene_likelihood'] - results_data['hyp_gene_likelihood']
    results_data['harmonic_mean'] = -trace['Data-ld-ln']
    return results_data


def _calc_comb_ref_gene_likelihood(comb_stats: pd.DataFrame, hyp_stats: pd.DataFrame, trace: pd.DataFrame, conf: ConfigHandler):
    comb, comb_leaves, hyp_pops, comb_mig_bands, hyp_mig_bands = conf.get_comb_reference_tree()

    all_pops = [comb] + comb_leaves + hyp_pops
    all_mig_bands = comb_mig_bands + hyp_mig_bands

    thetas = _get_thetas(all_pops, trace, conf)
    mig_rates = _get_migrates(all_mig_bands, trace, conf)

    num_migs, mig_stats = _get_comb_mig_stats(comb_stats, hyp_stats, conf)
    num_coal, coal_stats = _get_comb_coal_stats(comb_stats, hyp_stats, conf)

    objects_to_sum = pd.DataFrame()
    for pop in all_pops:
        objects_to_sum[pop] = kingman_coalescent(thetas[pop], num_coal[pop], coal_stats[pop])
    for mig in all_mig_bands:
        objects_to_sum[mig] = kingman_migration(mig_rates[mig], num_migs[mig], mig_stats[mig])

    if conf.is_debug_enabled():
        debug_dir = conf.get_results_paths()[1]
        save_plot(objects_to_sum, debug_dir + '/pop_ln_ld', 'Kingman coal & mig of Reference Model')

    ref_gene_likelihood = objects_to_sum.sum(axis=1)
    log.info("Calculated reference genealogy likelihood")

    return ref_gene_likelihood


def _calc_clade_ref_gene_likelihood(clade_stats: pd.DataFrame, hyp_stats, trace: pd.DataFrame, conf: ConfigHandler):
    clade, hyp_pops, hyp_mig_bands = conf.get_clade_reference_tree()

    thetas = _get_thetas(hyp_pops + [clade], trace, conf)
    mig_rates = _get_migrates(hyp_mig_bands, trace, conf)
    mig_stats, num_migs = _get_hyp_mig_stats(hyp_mig_bands, hyp_stats, conf)
    coal_stats, num_coal = _get_clade_coal_stats(clade_stats, hyp_stats, conf)

    objects_to_sum = pd.DataFrame()
    for pop in hyp_pops + [clade]:
        objects_to_sum[pop] = kingman_coalescent(thetas[pop], num_coal[pop], coal_stats[pop])
    for mig in hyp_mig_bands:
        objects_to_sum[mig] = kingman_migration(mig_rates[mig], num_migs[mig], mig_stats[mig])

    ref_gene_likelihood = objects_to_sum.sum(axis=1)
    log.info("Calculated reference genealogy likelihood")

    return ref_gene_likelihood


def _get_migrates(mig_bands, trace, conf: ConfigHandler):
    _, mig_rate_print_factor = conf.get_print_factors()
    mig_rate_template = conf.get_migrate_template()
    mig_rate_columns = [mig_rate_template.format(migband=mb) for mb in mig_bands]
    mig_rates = trace[mig_rate_columns].divide(mig_rate_print_factor).copy()
    mig_rates.columns = mig_bands
    return mig_rates


def _get_thetas(pops, trace, conf):
    theta_print_factor, theta_template = conf.get_theta_setup()

    theta_columns = [theta_template.format(pop=p) for p in pops]
    thetas = trace[theta_columns].divide(theta_print_factor).copy()  # type: pd.DataFrame
    columns_map = {theta_template.format(pop=p): p for p in pops}
    thetas.rename(columns=columns_map, inplace=True)
    return thetas


def _get_comb_mig_stats(comb_stats: pd.DataFrame, hyp_stats: pd.DataFrame, conf: ConfigHandler):
    comb, _, _, comb_mig_bands, hyp_mig_bands = conf.get_comb_reference_tree()
    comb_num_migs_template, comb_mig_stats_template = conf.get_comb_migs_templates()

    hyp_mig_stats, hyp_num_migs = _get_hyp_mig_stats(hyp_mig_bands, hyp_stats, conf)

    comb_mig_stats_columns = [comb_mig_stats_template.format(comb=comb, migband=mb) for mb in comb_mig_bands]
    comb_mig_stats = comb_stats[comb_mig_stats_columns]
    comb_mig_stats.columns = comb_mig_bands
    mig_stats = pd.concat([hyp_mig_stats, comb_mig_stats], join='inner', axis=1)

    comb_num_migs_columns = [comb_num_migs_template.format(comb=comb, migband=mb) for mb in comb_mig_bands]
    comb_num_migs = comb_stats[comb_num_migs_columns]
    comb_num_migs.columns = comb_mig_bands
    num_migs = pd.concat([comb_num_migs, hyp_num_migs], join='inner', axis=1)

    return num_migs, mig_stats


def _get_hyp_mig_stats(hyp_mig_bands, hyp_stats, conf: ConfigHandler) -> (pd.DataFrame, pd.DataFrame):
    hyp_mig_stats_template, hyp_num_migs_template = conf.get_hyp_mig_templates()

    mig_stats_columns = [hyp_mig_stats_template.format(migband=mb) for mb in hyp_mig_bands]
    mig_stats = hyp_stats[mig_stats_columns]
    mig_stats.columns = hyp_mig_bands

    num_migs_columns = [hyp_num_migs_template.format(migband=mb) for mb in hyp_mig_bands]
    num_migs = hyp_stats[num_migs_columns]
    num_migs.columns = hyp_mig_bands

    return mig_stats, num_migs


def _get_comb_coal_stats(comb_stats, hyp_stats, conf: ConfigHandler):
    comb, comb_leaves, hyp_pops, _, _ = conf.get_comb_reference_tree()
    comb_coal_stats_template, comb_leaf_coal_stats_template = conf.get_comb_coal_stats_templates()
    comb_leaf_num_coals_template, comb_num_coals_template = conf.get_comb_num_coals_templates()
    hyp_coal_stats, hyp_num_coal = _get_hyp_coal_stats(hyp_stats, hyp_pops, conf)

    cs_columns_map = {comb_coal_stats_template.format(comb=comb): comb}
    cs_columns_map.update({comb_leaf_coal_stats_template.format(comb=comb, leaf=l): l for l in comb_leaves})
    comb_coal_stats = copy_then_rename_columns(comb_stats, cs_columns_map)
    coal_stats = pd.concat([hyp_coal_stats, comb_coal_stats], join='inner', axis=1)

    nc_columns_map = {comb_num_coals_template.format(comb=comb): comb}
    nc_columns_map.update({comb_leaf_num_coals_template.format(comb=comb, leaf=l): l for l in comb_leaves})
    comb_num_coals = copy_then_rename_columns(comb_stats, nc_columns_map)
    num_coal = pd.concat([hyp_num_coal, comb_num_coals], join='inner', axis=1)

    return num_coal, coal_stats


def _get_clade_coal_stats(clade_stats: pd.DataFrame, hyp_stats, conf: ConfigHandler):
    clade, hyp_pops, _ = conf.get_clade_reference_tree()
    clade_num_coals_template, clade_coal_stats_template = conf.get_clade_coal_templates()

    hyp_coal_stats, hyp_num_coal = _get_hyp_coal_stats(hyp_stats, hyp_pops, conf)

    clade_num_coals = clade_stats[[clade_num_coals_template.format(clade=clade)]]
    clade_num_coals.columns = [clade]
    num_coals = pd.concat([hyp_num_coal, clade_num_coals], join='inner', axis=1)

    clade_coal_stats = clade_stats[[clade_coal_stats_template.format(clade=clade)]]
    clade_coal_stats.columns = [clade]
    coal_stats = pd.concat([hyp_coal_stats, clade_coal_stats], join='inner', axis=1)

    return coal_stats, num_coals


def _get_hyp_coal_stats(hyp_stats, hyp_pops, conf):
    pop_coal_stats_template, pop_num_coals_template = conf.get_hyp_coal_templates()
    hyp_nc_columns_map = {pop_num_coals_template.format(pop=p): p for p in hyp_pops}
    hyp_num_coals = copy_then_rename_columns(hyp_stats, hyp_nc_columns_map)
    hyp_cs_columns_map = {pop_coal_stats_template.format(pop=p): p for p in hyp_pops}
    hyp_coal_stats = copy_then_rename_columns(hyp_stats, hyp_cs_columns_map)
    return hyp_coal_stats, hyp_num_coals


def _calc_hyp_gene_likelihood(results_data: pd.DataFrame, hyp_stats: pd.DataFrame, trace: pd.DataFrame, conf: ConfigHandler):
    hyp_pops, hyp_mig_bands = conf.get_hypothesis_tree()

    thetas = _get_thetas(hyp_pops, trace, conf)
    mig_rates = _get_migrates(hyp_mig_bands, trace, conf)
    mig_stats, num_migs = _get_hyp_mig_stats(hyp_mig_bands, hyp_stats, conf)
    coal_stats, num_coals = _get_hyp_coal_stats(hyp_stats, hyp_pops, conf)

    objects_to_sum = pd.DataFrame()
    for pop in hyp_pops:
        objects_to_sum[pop] = kingman_coalescent(thetas[pop], num_coals[pop], coal_stats[pop])
    for mig in hyp_mig_bands:
        objects_to_sum[mig] = kingman_migration(mig_rates[mig], num_migs[mig], mig_stats[mig])

    debug_dir = conf.get_results_paths()[1]
    save_plot(objects_to_sum, debug_dir + '/hyp_ln_ld', 'Kingman coal & mig of Hypothesis Model')

    hyp_gene_likelihood = objects_to_sum.sum(axis=1)
    log.info("Calculated hypothesis genealogy likelihood")

    results_data['debug_hyp_gene_likelihood'] = hyp_gene_likelihood


def _debug_coal_stats(results_data: pd.DataFrame, ref_stats: pd.DataFrame, hyp_stats: pd.DataFrame, conf: ConfigHandler):
    if conf.is_clade_enabled():
        _, ref_coal_stats = _get_clade_coal_stats(ref_stats, hyp_stats, conf)
    else:
        _, ref_coal_stats = _get_comb_coal_stats(ref_stats, hyp_stats, conf)

    hyp_pops, _ = conf.get_hypothesis_tree()
    hyp_coal_stats, _ = _get_hyp_coal_stats(hyp_stats, hyp_pops, conf)

    results_data['hyp_coal_stats'] = hyp_coal_stats.sum(axis=1)
    results_data['ref_coal_stats'] = ref_coal_stats.sum(axis=1)
    log.info("Calculated DEBUG coal stats")


def _save_results(results_data: pd.DataFrame, experiment_summary: str, conf: ConfigHandler):
    (results_directory, debug_directory, results_path, likelihoods_plot_path,
     expectation_plot_path, harmonic_mean_plot_path, summary_path) = conf.get_results_paths()

    sim_name = conf.simulation.split("/")[-1]
    save_plot(results_data[['ref_gene_likelihood', 'hyp_gene_likelihood']], likelihoods_plot_path, sim_name)
    save_plot(results_data[['harmonic_mean']], harmonic_mean_plot_path, sim_name)
    save_plot(results_data[['rbf_ratio']], expectation_plot_path, sim_name)

    if conf.is_debug_enabled():
        save_plot(results_data[['ref_gene_likelihood', 'debug_hyp_gene_likelihood', 'hyp_gene_likelihood']], debug_directory + '/gene_likelihoods',
                  sim_name)
        save_plot(results_data[['ref_coal_stats', 'hyp_coal_stats']], debug_directory + '/coal_stats', sim_name)

    with open(summary_path, 'w') as f:
        log.info(experiment_summary)
        f.write(experiment_summary)

    if conf.should_save_results():
        results_data.to_csv(results_path)


def _comb_summarize(results_analysis: dict, conf: ConfigHandler):
    comb, comb_leaves, populations, leaf_mig_bands, _ = conf.get_comb_reference_tree()
    simulation_name = conf.simulation.split('/')[-1]
    formatted_leaves = ','.join(comb_leaves)
    formatted_pops = ','.join(populations)
    formatted_migbands = ','.join(leaf_mig_bands)
    intro_template = "Summary:\n" + \
                     "Simulation: %s\n" % simulation_name + \
                     "Comb: {0} | Comb Leaves: {1} | Populations: {2} | Migration Bands: {3}\n"
    intro = intro_template.format(comb, formatted_leaves, formatted_pops, formatted_migbands)

    results_string = []
    for column in sorted(list(results_analysis.keys())):
        results_string.extend([column, ': ', str(results_analysis[column]), '\n'])
    results_string = ''.join(results_string)

    return intro + results_string


def _clade_summarize(results_analysis: dict, conf: ConfigHandler):
    clade, populations, migration_bands = conf.get_clade_reference_tree()
    simulation_name = conf.simulation.split('/')[-1]
    formatted_pops = ','.join(populations)
    formatted_migbands = ','.join(migration_bands)
    intro_template = "Summary:\n" + \
                     "Simulation: %s\n" % simulation_name + \
                     "Comb: {0} | Populations: {1} | Migration Bands: {2}\n"
    intro = intro_template.format(clade, formatted_pops, formatted_migbands)

    results_string = []
    for column in sorted(list(results_analysis.keys())):
        results_string.extend([column, ': ', str(results_analysis[column]), '\n'])
    results_string = ''.join(results_string)

    return intro + results_string
