import os
from collections import namedtuple
from functools import partial

from mcref.probability_functions import *
from mcref.util.config_handler import ConfigHandler
from mcref.util.log import with_entry_log, module_logger
from mcref.util.panda_helpers import copy_then_rename_columns, save_plot, replace_zeroes_with_epsilon

_log = module_logger(__name__)

Result = namedtuple('Result', ('simulation', 'rbf_mean', 'rbf_bootstrap', 'hm_mean', 'hm_bootstrap'))


@with_entry_log(_log)
def run_simulation(simulation) -> Result:
    _validate_simulation(simulation)
    return _run_simulation(simulation)


def _validate_simulation(sim):
    try:
        sim = os.path.abspath(sim)
        configuration_path = os.path.join(sim, 'config.ini')
        assert os.path.isfile(configuration_path)
    except AssertionError as e:
        _log.error("simulation %s isn't valid directory" % sim)
        raise FileNotFoundError("Could not locate 'config.ini' in simulation dir '%s'" % sim) from e


def _run_simulation(simulation):
    conf = ConfigHandler(simulation)
    ref_stats = conf.load_ref_data()
    trace = conf.load_trace_data()
    hyp_stats = conf.load_hyp_data()
    results_data = _calculate_ref_likelihoods(ref_stats, hyp_stats, trace, conf)
    results_analysis = analyze_columns(results_data, ['rbf_ratio', 'harmonic_mean'])
    if conf.debug_enabled:
        try:
            _debug_calc_hyp_gene_likelihood(results_data, hyp_stats, trace, conf)
            _debug_calc_coal_stats(results_data, ref_stats, hyp_stats, conf)
        except:
            _log.error("Failed calculating debug stats")
    _save_results(results_data, conf)
    return _build_result(conf, results_analysis)


def _calculate_ref_likelihoods(ref_stats, hyp_stats, trace, conf: ConfigHandler):
    results_data = pd.DataFrame()
    ref_gene_likelihood = _clade_ref_gene_likelihood if conf.clade else _comb_ref_gene_likelihood
    results_data['ref_gene_likelihood'] = ref_gene_likelihood(ref_stats, hyp_stats, trace, conf)
    results_data['hyp_gene_likelihood'] = trace['Gene-ld-ln']
    results_data['rbf_ratio'] = results_data['ref_gene_likelihood'] - results_data['hyp_gene_likelihood']
    if conf.tau_bounds_enabled():
        _calculate_tau_priors(conf.tau_bounds, results_data, conf)
        results_data['rbf_ratio'] += results_data['ref_tau_prior'] - results_data['hyp_tau_prior']
    results_data['harmonic_mean'] = -trace['Data-ld-ln']

    return results_data


def _comb_ref_gene_likelihood(comb_stats: pd.DataFrame, hyp_stats: pd.DataFrame, trace: pd.DataFrame, conf: ConfigHandler):
    comb, comb_leaves, hyp_pops, hyp_mig_bands = conf.get_comb_reference_tree()

    all_pops = [comb] + comb_leaves + hyp_pops

    thetas = _get_thetas(all_pops, trace, conf)
    mig_rates = _get_migrates(hyp_mig_bands, trace, conf)

    mig_stats, num_migs = _get_hyp_mig_stats(hyp_mig_bands, hyp_stats, conf)
    coal_stats, num_coal = _get_comb_coal_stats(comb_stats, hyp_stats, conf)

    objects_to_sum = pd.DataFrame()
    for pop in all_pops:
        objects_to_sum[pop] = kingman_coalescent(thetas[pop], num_coal[pop], coal_stats[pop])
    for mig in hyp_mig_bands:
        objects_to_sum[mig] = kingman_migration(mig_rates[mig], num_migs[mig], mig_stats[mig])

    if conf.debug_enabled:
        debug_dir = conf.results_paths[0]
        save_plot(objects_to_sum, debug_dir + '/ref_ln_ld', 'Kingman coal & mig of Reference Model')

    ref_gene_likelihood = objects_to_sum.sum(axis=1)
    _log.info("Calculated reference genealogy likelihood")

    return ref_gene_likelihood


def _clade_ref_gene_likelihood(clade_stats: pd.DataFrame, hyp_stats, trace: pd.DataFrame, conf: ConfigHandler):
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
    _log.info("Calculated reference genealogy likelihood")

    return ref_gene_likelihood


def _calculate_tau_priors(tau_bounds_trace: pd.DataFrame, results_data: pd.DataFrame, conf: ConfigHandler):
    bound_columns = [col for col in tau_bounds_trace.columns if 'bound' in col]
    bounds = tau_bounds_trace[bound_columns].copy()
    non_zero_min = bounds[bounds > 0.0].min()
    bounds.replace(to_replace=0.0, value=non_zero_min, inplace=True)
    bound_intervals = calc_bound_intervals(bounds)
    ref_tau_priors = bound_intervals.applymap(PDF.uniform)
    log_ref_tau_priors = ref_tau_priors.applymap(np.log)
    results_data['ref_tau_prior'] = log_ref_tau_priors.sum(axis=1)

    tau_columns = [col for col in tau_bounds_trace.columns if 'tau' in col]
    taus = tau_bounds_trace[tau_columns]
    hyp_tau_priors = taus.applymap(partial(PDF.gamma, alpha=conf.gamma_alpha, beta=conf.gamma_beta))
    log_hyp_tau_priors = hyp_tau_priors.applymap(np.log)
    results_data['hyp_tau_prior'] = log_hyp_tau_priors.sum(axis=1)

    if conf.debug_enabled:
        debug_dir = conf.results_paths[0]
        tau_bounds_dir = debug_dir + '/tau_bounds'
        save_plot(log_hyp_tau_priors, tau_bounds_dir + '/log_hyp_tau_priors', 'Log Hypothesis Tau priors')
        save_plot(log_ref_tau_priors, tau_bounds_dir + '/log_ref_tau_priors', 'Log Reference Tau priors')
        save_plot(results_data[['ref_tau_prior', 'hyp_tau_prior']], tau_bounds_dir + '/log_hyp_n_ref_sum_tau_priors', 'Sum of Log of Tau priors')


def calc_bound_intervals(bounds: pd.DataFrame):
    tau_intervals = pd.DataFrame()
    ubound_columns = [col for col in bounds.columns.values if 'ubound' in col]
    for ubound_col in ubound_columns:
        pop = ubound_col.split('_')[0]
        lbound_col, interval_col = f'{pop}_lbound', f'{pop}_interval'
        tau_intervals[interval_col] = bounds[ubound_col] - bounds[lbound_col]
    return tau_intervals


def _get_migrates(mig_bands, trace, conf: ConfigHandler):
    mig_rate_print_factor, mig_rate_template = conf.migrate_setup
    mig_rate_columns = [mig_rate_template.format(migband=mb) for mb in mig_bands]
    mig_rates = trace[mig_rate_columns].divide(mig_rate_print_factor).copy()
    mig_rates.columns = mig_bands
    replace_zeroes_with_epsilon(mig_rates)
    return mig_rates


def _get_thetas(pops, trace, conf: ConfigHandler):
    theta_print_factor, theta_template = conf.theta_setup

    theta_columns = [theta_template.format(pop=p) for p in pops]
    thetas = trace[theta_columns].divide(theta_print_factor).copy()  # type: pd.DataFrame
    columns_map = {theta_template.format(pop=p): p for p in pops}
    thetas.rename(columns=columns_map, inplace=True)
    return thetas


def _get_comb_coal_stats(comb_stats, hyp_stats, conf: ConfigHandler) -> (pd.DataFrame, pd.DataFrame):
    comb, comb_leaves, hyp_pops, _ = conf.get_comb_reference_tree()
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
    num_coals = pd.concat([hyp_num_coal, comb_num_coals], join='inner', axis=1)

    return coal_stats, num_coals


def _get_clade_coal_stats(clade_stats: pd.DataFrame, hyp_stats, conf: ConfigHandler) -> (pd.DataFrame, pd.DataFrame):
    clade, hyp_pops, _ = conf.get_clade_reference_tree()
    clade_num_coals_template, clade_coal_stats_template = conf.clade_coal_templates

    hyp_coal_stats, hyp_num_coal = _get_hyp_coal_stats(hyp_stats, hyp_pops, conf)

    clade_num_coals = clade_stats[[clade_num_coals_template.format(clade=clade)]]
    clade_num_coals.columns = [clade]
    num_coals = pd.concat([hyp_num_coal, clade_num_coals], join='inner', axis=1)

    clade_coal_stats = clade_stats[[clade_coal_stats_template.format(clade=clade)]]
    clade_coal_stats.columns = [clade]
    coal_stats = pd.concat([hyp_coal_stats, clade_coal_stats], join='inner', axis=1)

    return coal_stats, num_coals


def _get_hyp_coal_stats(hyp_stats, hyp_pops, conf) -> (pd.DataFrame, pd.DataFrame):
    pop_coal_stats_template, pop_num_coals_template = conf.get_hyp_coal_templates()
    hyp_nc_columns_map = {pop_num_coals_template.format(pop=p): p for p in hyp_pops}
    num_coals = copy_then_rename_columns(hyp_stats, hyp_nc_columns_map)
    hyp_cs_columns_map = {pop_coal_stats_template.format(pop=p): p for p in hyp_pops}
    coal_stats = copy_then_rename_columns(hyp_stats, hyp_cs_columns_map)
    return coal_stats, num_coals


def _get_hyp_mig_stats(hyp_mig_bands, hyp_stats, conf: ConfigHandler) -> (pd.DataFrame, pd.DataFrame):
    hyp_mig_stats_template, hyp_num_migs_template = conf.get_hyp_mig_templates()

    mig_stats_columns = [hyp_mig_stats_template.format(migband=mb) for mb in hyp_mig_bands]
    mig_stats = hyp_stats[mig_stats_columns]
    mig_stats.columns = hyp_mig_bands

    num_migs_columns = [hyp_num_migs_template.format(migband=mb) for mb in hyp_mig_bands]
    num_migs = hyp_stats[num_migs_columns]
    num_migs.columns = hyp_mig_bands

    return mig_stats, num_migs


def _debug_calc_hyp_gene_likelihood(results_data: pd.DataFrame, hyp_stats: pd.DataFrame, trace: pd.DataFrame, conf: ConfigHandler):
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

    debug_dir = conf.results_paths[0]
    save_plot(objects_to_sum, debug_dir + '/hyp_ln_ld', 'Kingman coal & mig of Hypothesis Model')

    hyp_gene_likelihood = objects_to_sum.sum(axis=1)
    _log.info("Calculated hypothesis genealogy likelihood")

    results_data['debug_hyp_gene_likelihood'] = hyp_gene_likelihood


def _debug_calc_coal_stats(results_data: pd.DataFrame, ref_stats: pd.DataFrame, hyp_stats: pd.DataFrame, conf: ConfigHandler):
    get_ref_coal_stats = _get_clade_coal_stats if conf.clade else _get_comb_coal_stats
    ref_coal_stats, _ = get_ref_coal_stats(ref_stats, hyp_stats, conf)

    hyp_pops, _ = conf.get_hypothesis_tree()
    hyp_coal_stats, _ = _get_hyp_coal_stats(hyp_stats, hyp_pops, conf)

    results_data['hyp_coal_stats'] = hyp_coal_stats.sum(axis=1)
    results_data['ref_coal_stats'] = ref_coal_stats.sum(axis=1)
    _log.info("Calculated DEBUG coal stats")


def _save_results(results_data: pd.DataFrame, conf: ConfigHandler):
    (debug_directory, results_path, likelihoods_plot_path,
     expectation_plot_path, harmonic_mean_plot_path, summary_path) = conf.results_paths

    sim_name = conf.simulation_path.split("/")[-1]
    save_plot(results_data[['ref_gene_likelihood', 'hyp_gene_likelihood']], likelihoods_plot_path, sim_name)
    save_plot(results_data[['harmonic_mean']], harmonic_mean_plot_path, sim_name)
    save_plot(results_data[['rbf_ratio']], expectation_plot_path, sim_name)

    conf.store()

    try:
        if conf.debug_enabled:
            save_plot(results_data[['ref_gene_likelihood', 'debug_hyp_gene_likelihood', 'hyp_gene_likelihood']], debug_directory + '/gene_likelihoods',
                      sim_name)
            save_plot(results_data[['ref_coal_stats', 'hyp_coal_stats']], debug_directory + '/coal_stats', sim_name)
    except:
        pass

    if conf.should_save_raw_results:
        results_data.to_csv(results_path)


def _build_result(conf, results_analysis):
    return Result(conf.simulation_path,
                  results_analysis['rbf_ratio']['ln_mean'], results_analysis['rbf_ratio']['bootstrap'],
                  results_analysis['harmonic_mean']['ln_mean'], results_analysis['harmonic_mean']['bootstrap'])
