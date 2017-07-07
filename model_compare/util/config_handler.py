import configparser
import os
import time

import pandas as pd

from model_compare.util.log import module_logger

logger = module_logger(__name__)


class ConfigHandler:
    def __init__(self, simulation):
        self.simulation = simulation
        self.config = configparser.ConfigParser()
        # look for configuration in cwd and in simulation dir. simulation-specific config overrides the one in cwd!
        self.config.read(['config.ini', 'model_compare/config.ini', '%s/config.ini' % simulation])

    def load_comb_data(self):
        simulation_path = self.get_simulation_path()
        burn_in = self.get_burn_in()
        comb_stats_name = self.config.get('Input', 'comb_stats_file_name')
        comb_stats_path = simulation_path + '/' + comb_stats_name  # TODO - use system fs separator
        comb_stats = pd.read_csv(comb_stats_path, sep='\t', skiprows=range(1, burn_in), header=0, index_col='iteration')
        logger.info("Loaded comb_stats data")

        return comb_stats

    def load_clade_data(self):
        simulation_path = self.get_simulation_path()
        burn_in = self.get_burn_in()
        clade_stats_name = self.config.get('Input', 'clade_stats_file_name')
        clade_stats_path = simulation_path + '/' + clade_stats_name
        clade_stats = pd.read_csv(clade_stats_path, sep='\t', skiprows=range(1, burn_in), header=0, index_col='iteration')
        logger.info("Loaded clade_stats data")

        return clade_stats

    def load_trace_data(self):
        simulation_path = self.get_simulation_path()
        burn_in = self.get_burn_in()
        trace_file_name = self.config.get('Input', 'trace_file_name')
        trace_path = simulation_path + '/' + trace_file_name
        trace = pd.read_csv(trace_path, sep='\t', skiprows=range(1, burn_in), header=0, index_col='Sample')
        logger.info("Loaded trace data")
        return trace

    def load_hyp_data(self):
        simulation_path = self.get_simulation_path()
        burn_in = self.get_burn_in()
        hyp_file_name = self.config.get('Debug', 'hyp_stats_file_name')
        hyp_path = simulation_path + '/' + hyp_file_name
        hyp_stats = pd.read_csv(hyp_path, sep='\t', skiprows=range(1, burn_in), header=0, index_col='iteration')
        logger.info("Loaded trace data")
        return hyp_stats

    def get_burn_in(self):
        return self.config.getint('Data', 'skip_rows', fallback=0)

    def get_simulation_path(self):
        return self.simulation

    def get_reference_tree(self):
        comb = self.config.get('ReferenceModel', 'comb')
        comb_leaves = self.config.get('ReferenceModel', 'comb_leaves').split(',')
        pops = self.config.get('ReferenceModel', 'pops').split(',')
        mig_bands = self.config.get('ReferenceModel', 'mig_bands').split(',')

        comb_leaves, mig_bands, pops = remove_empty_strings(comb_leaves, mig_bands, pops)

        return comb, comb_leaves, pops, mig_bands

    def get_clade_reference_tree(self):
        clade = self.config.get('ReferenceModel', 'clade')
        pops = self.config.get('ReferenceModel', 'pops').split(',')
        mig_bands = self.config.get('ReferenceModel', 'mig_bands').split(',')
        _, mig_bands, pops = remove_empty_strings([], mig_bands, pops)

        return clade, pops, mig_bands

    def get_hypothesis_tree(self):
        pops = self.config.get('Debug', 'hypothesis_pops').split(',')
        migs = self.config.get('Debug', 'hypothesis_migbands').split(',')

        pops = list(filter(None, pops))
        migs = list(filter(None, migs))

        return pops, migs

    def get_results_paths(self):
        simulation_path = self.get_simulation_path()
        timestamp = time.strftime('%Y%m%d_%H%M')

        results_directory = simulation_path + '/' + self.config.get('Output', 'results_directory', fallback='results') + '/' + timestamp
        debug_directory = results_directory + '/' + self.config.get('Output', 'debug_directory', fallback='debug')
        for directory in results_directory, debug_directory:
            if not os.path.exists(directory):
                os.makedirs(directory)
        results_path = results_directory + '/' + self.config.get('Output', 'results_name', fallback='results.csv')
        summary_path = results_directory + '/' + self.config.get('Output', 'summary_name', fallback='summary.txt')
        likelihoods_plot_path = results_directory + '/' + self.config.get('Output', 'likelihoods_plot_name', fallback='hyp_and_ref_plot')
        expectation_plot_path = results_directory + '/' + self.config.get('Output', 'expectation_plot_name', fallback='rbf_plot')
        harmonic_mean_plot_path = results_directory + '/' + self.config.get('Output', 'harmonic_mean_plot_name', fallback='harmonic_mean_plot')

        return (results_directory, debug_directory, results_path, likelihoods_plot_path, expectation_plot_path,
                harmonic_mean_plot_path, summary_path)

    def get_column_name_templates(self):

        theta = self.config.get('Templates', 'theta', fallback='theta_{pop}')
        mig_rate = self.config.get('Templates', 'mig_rate', fallback='m_{migband}')
        pop_num_coals_template = self.config.get('Templates', 'pop_num_coals', fallback='P_{pop} nc')
        pop_coal_stats_template = self.config.get('Templates', 'pop_coal_stats', fallback='P_{pop} cs')
        comb_coal_stats_template = self.config.get('Templates', 'comb_coal_stats', fallback='C_{comb} cs')
        comb_num_coals_template = self.config.get('Templates', 'comb_num_coals', fallback='C_{comb} nc')
        comb_leaf_num_coals_template = self.config.get('Templates', 'comb_leaf_num_coals', fallback='C_{comb}_{leaf} nc')
        comb_leaf_coal_stats_template = self.config.get('Templates', 'comb_leaf_coal_stats', fallback='C_{comb}_{leaf} cs')
        comb_migband_mig_stats_template = self.config.get('Templates', 'comb_migband_mig_stats', fallback='C_{comb}_{migband} ms')
        comb_migband_num_migs_template = self.config.get('Templates', 'comb_migband_num_migs', fallback='C_{comb}_{migband} nm')

        return (theta, mig_rate, comb_num_coals_template, comb_leaf_num_coals_template, pop_num_coals_template,
                comb_coal_stats_template, comb_leaf_coal_stats_template, pop_coal_stats_template,
                comb_migband_mig_stats_template, comb_migband_num_migs_template)

    def get_print_factors(self):
        theta_print_factor = self.config.getfloat('Input', 'theta_print_factor', fallback=10000.0)
        mig_rate_print_factor = self.config.getfloat('Input', 'mig_rate_print_factor', fallback=0.1)

        return theta_print_factor, mig_rate_print_factor

    def should_save_results(self):
        result = self.config.getboolean("Output", "save_data", fallback=False)
        return result

    def get_comb_num_coals_template(self):
        comb_leaf_num_coals_template = self.config.get('Templates', 'comb_leaf_num_coals', fallback='C_{comb}_{leaf} nc')
        comb_num_coals_template = self.config.get('Templates', 'comb_num_coals', fallback='C_{comb} nc')
        pop_num_coals_template = self.config.get('Templates', 'pop_num_coals', fallback='P_{pop} nc')
        return comb_leaf_num_coals_template, comb_num_coals_template, pop_num_coals_template

    def get_clade_num_coals_template(self):
        clade_num_coals_template = self.config.get('Templates', 'clade_num_coals', fallback='{clade}_num_coals_total')
        pop_num_coals_template = self.config.get('Templates', 'clade_pop_num_coals', fallback='{pop}__pop_num_coals_total')
        return clade_num_coals_template, pop_num_coals_template

    def get_theta_setup(self):
        theta_print_factor = self.config.getfloat('Input', 'theta_print_factor', fallback=10000.0)
        theta_template = self.config.get('Templates', 'theta', fallback='theta_{pop}')
        return theta_print_factor, theta_template

    def get_comb_coal_stats_templates(self):
        comb_coal_stats_template = self.config.get('Templates', 'comb_coal_stats', fallback='C_{comb} cs')
        comb_leaf_coal_stats_template = self.config.get('Templates', 'comb_leaf_coal_stats', fallback='C_{comb}_{leaf} cs')
        return comb_coal_stats_template, comb_leaf_coal_stats_template

    def get_clade_coal_stats_templates(self):
        pop_coal_stats_template = self.config.get('Templates', 'clade_pop_coal_stats', fallback='{pop}__pop_coal_stats_total')
        clade_coal_stats_template = self.config.get('Templates', 'clade_coal_stats', fallback='{clade}_coal_stats_total')
        return clade_coal_stats_template, pop_coal_stats_template

    def get_hyp_coal_templates(self):
        pop_coal_stats_template = self.config.get('Templates', 'pop_coal_stats', fallback='P_{pop} cs')
        pop_num_coals_template = self.config.get('Templates', 'pop_coal_stats', fallback='P_{pop} nc')
        return pop_coal_stats_template, pop_num_coals_template

    def get_hyp_mig_templates(self):
        hyp_mig_stats_template = self.config.get('Templates', 'hyp_migband_mig_stats', fallback='MB_{migband} ms')
        hyp_num_migs_template = self.config.get('Templates', 'hyp_migband_num_migs', fallback='MB_{migband} nm')
        return hyp_mig_stats_template, hyp_num_migs_template

    def get_clade_mig_stats_template(self):
        clade_migband_mig_stats_template = self.config.get('Templates', 'clade_migband_mig_stats', fallback='{migband}_mig_stats')
        return clade_migband_mig_stats_template

    def get_comb_migs_templates(self):
        comb_num_migs_template = self.config.get('Templates', 'comb_migband_num_migs', fallback='C_{comb}_{migband} nm')
        comb_mig_stats_template = self.config.get('Templates', 'comb_migband_mig_stats', fallback='C_{comb}_{migband} ms')
        return comb_num_migs_template, comb_mig_stats_template

    def get_clade_num_migs_template(self):
        clade_migband_num_migs_template = self.config.get('Templates', 'clade_migband_num_migs', fallback='{migband}_num_migs')
        return clade_migband_num_migs_template

    def get_migrate_template(self):
        mig_rate = self.config.get('Templates', 'mig_rate', fallback='m_{migband}')
        return mig_rate

    def is_debug_enabled(self):
        return self.config.getboolean('Debug', 'enabled', fallback=False)

    def get_log_conf(self):
        return (self.config.get('Logging', 'level', fallback='INFO'),
                self.config.get('Logging', 'file_name', fallback='model_compare.log'))


def remove_empty_strings(comb_leaves, mig_bands, pops):  # TODO - accept any number of args
    comb_leaves = list(filter(None, comb_leaves))
    pops = list(filter(None, pops))
    mig_bands = list(filter(None, mig_bands))
    return comb_leaves, mig_bands, pops
