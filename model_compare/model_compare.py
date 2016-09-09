import pandas as pd
import os
from model_compare.config_handler import ConfigHandler
from model_compare.data_prep import *
from model_compare.probability_functions import *


def model_compare(simulation='sample'):

    conf = ConfigHandler(simulation)
    clade_stats, trace = conf.get_gphocs_data()
    clade_stats, trace = equate_lengths(clade_stats, trace)

    results_data = pd.DataFrame()

    results_data['ref_gene_likelihood'] = calc_ref_gene_likelihood(clade_stats, trace, conf)
    results_data['hyp_gene_likelihood'] = trace['Gene-ld-ln']
    results_data['hm_data_likelihood'] = -trace['Full-ld-ln']
    results_data['rbf_ratio'] = results_data['ref_gene_likelihood'] - results_data['hyp_gene_likelihood']

    results_data = preprocess_data(results_data, conf)

    results_stats = {column: statistify(results_data[column]) for column in ['rbf_ratio', 'hm_data_likelihood']}

    save_results(results_data, results_stats, conf)


def calc_ref_gene_likelihood(clade_stats, trace, conf):

    pop_infix, theta_prefix, num_coals_suffix, coal_stats_suffix,\
    mig_rate_prefix, num_migs_suffix, mig_stats_suffix = conf.get_prefixes()

    clades, populations, migration_bands = conf.get_clades_pops_and_migs()
    theta_print_factor, mig_rate_print_factor = conf.get_data_config()

    thetas = trace[[theta_prefix + p for p in populations] + [theta_prefix + c for c in clades]].divide(
        theta_print_factor)
    num_coal = clade_stats[
        [c + num_coals_suffix for c in clades] + [p + pop_infix + num_coals_suffix for p in populations]]
    coal_stats = clade_stats[
        [c + coal_stats_suffix for c in clades] + [p + pop_infix + coal_stats_suffix for p in populations]]

    mig_rates = trace[[mig_rate_prefix + mig_band for mig_band in migration_bands]] / mig_rate_print_factor
    num_migs = clade_stats[[mig_band + num_migs_suffix for mig_band in migration_bands]]
    mig_stats = clade_stats[[mig_band + mig_stats_suffix for mig_band in migration_bands]]
    for df in (mig_rates, num_migs, mig_stats):
        df.columns = migration_bands

    objects_to_sum = pd.DataFrame()
    for pop in populations:
        objects_to_sum[pop + pop_infix] = kingman_coalescent(thetas[theta_prefix + pop],
                                                            num_coal[pop + pop_infix + num_coals_suffix],
                                                            coal_stats[pop + pop_infix + coal_stats_suffix])
    for clade in clades:
        objects_to_sum[clade] = kingman_coalescent(thetas[theta_prefix + clade], num_coal[clade + num_coals_suffix],
                                                  coal_stats[clade + coal_stats_suffix])
    for mig in migration_bands:
        objects_to_sum[mig] = kingman_migration(mig_rates[mig], num_migs[mig], mig_stats[mig])

    results = pd.DataFrame()

    columns_to_sum = clades + [pop + pop_infix for pop in populations] + migration_bands
    ref_gene_likelihood = objects_to_sum[columns_to_sum].sum(axis=1)

    return ref_gene_likelihood


def save_results(results_data, results_stats, conf):

    results_directory, results_path, likelihoods_plot_path, expectation_plot_path, harmonic_mean_plot_path, summary_path = conf.get_results_paths()

    if not os.path.exists(results_directory):
        os.makedirs(results_directory)

    save_plot(results_data[['ref_gene_likelihood', 'hyp_gene_likelihood']], likelihoods_plot_path, conf.simulation.split("/")[-1])
    save_plot(results_data[['hm_data_likelihood']], harmonic_mean_plot_path, conf.simulation.split("/")[-1])
    save_plot(results_data[['rbf_ratio']], expectation_plot_path, conf.simulation.split("/")[-1])


    with open(summary_path, 'w') as f:
        experiment_summary = summarize(results_stats, conf)
        super_summary = super_summarize(results_stats, conf)
        print(super_summary)
        f.write(experiment_summary)

    if conf.should_save_results():
        results_data.to_csv(results_path)


def summarize(results_stats, conf):
    clades, populations, migration_bands = conf.get_clades_pops_and_migs()
    simulation_name = conf.simulation.split('/')[-1]

    intro = "Summary:\n" + \
            "Simulation: %s\n" % simulation_name + \
            "|Clades: {0} | Populations: {1} | Migration Bands: {2}|\n".format(','.join(clades), ','.join(populations), ','.join(migration_bands))

    results_string = []
    for column in sorted(list(results_stats.keys())):
        results_string.extend([column, ': ', str(results_stats[column]), '\n'])
    results_string = ''.join(results_string)

    return intro + results_string

def super_summarize(results_stats, conf):
    clades, pops, mig_bands = conf.get_clades_pops_and_migs()
    simulation_name = conf.simulation.split('/')[-1]
    hm_mean = results_stats['hm_data_likelihood']['ln_mean']
    hm_boot = results_stats['hm_data_likelihood']['bootstrap']
    rbf_mean = results_stats['rbf_ratio']['ln_mean']
    rbf_boot = results_stats['rbf_ratio']['bootstrap']
    result=','.join((simulation_name, '&'.join(clades), '&'.join(pops), '&'.join(mig_bands), \
                      str(rbf_boot), str(rbf_mean), str(hm_boot), str(hm_mean)))
    return result


def save_plot(data_frame, plot_save_path, plot_name):
    plot = data_frame.plot(title=plot_name)
    plot_figure = plot.get_figure()
    plot_figure.savefig(plot_save_path + ".line.png")

    hist = data_frame.plot.hist(alpha=0.5, bins=160, normed=True, \
		title=plot_name+' histogram')
    hist_figure = hist.get_figure()
    hist_figure.savefig(plot_save_path + ".hist.png")
