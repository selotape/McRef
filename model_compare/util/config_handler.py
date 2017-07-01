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

    def get_gphocs_data(self):
        simulation_path = self.get_simulation_path()

        burn_in = self.get_burn_in()

        comb_stats_name = self.config.get('Input', 'comb_stats_file_name', fallback='comb-trace.tsv')
        comb_stats_path = simulation_path + '/' + comb_stats_name  # TODO - use system fs separator
        comb_stats = pd.read_csv(comb_stats_path, sep='\t', skiprows=range(1, burn_in), header=0, index_col='iteration')
        logger.info("Loaded comb_stats data")

        trace_file_name = self.config.get('Input', 'trace_file_name', fallback='trace.tsv')
        trace_path = simulation_path + '/' + trace_file_name  # TODO - use system fs separator
        trace = pd.read_csv(trace_path, sep='\t', skiprows=range(1, burn_in), header=0, index_col='Sample')
        logger.info("Loaded trace data")

        return comb_stats, trace

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

    def get_debug_pops(self):
        debug_pops = self.config.get('ReferenceModel', 'debug_pops').split(',')

        debug_pops = list(filter(None, debug_pops))

        return debug_pops

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

    def get_log_conf(self):
        return (self.config.get('Logging', 'level', fallback='INFO'),
                self.config.get('Logging', 'file_name', fallback='model_compare.log'))

    def get_num_coals_template(self):
        comb_leaf_num_coals_template = self.config.get('Templates', 'comb_leaf_num_coals', fallback='C_{comb}_{leaf} nc')
        comb_num_coals_template = self.config.get('Templates', 'comb_num_coals', fallback='C_{comb} nc')
        pop_num_coals_template = self.config.get('Templates', 'pop_num_coals', fallback='P_{pop} nc')
        return comb_leaf_num_coals_template, comb_num_coals_template, pop_num_coals_template

    def get_theta_setup(self):
        theta_print_factor = self.config.getfloat('Input', 'theta_print_factor', fallback=10000.0)
        theta_template = self.config.get('Templates', 'theta', fallback='theta_{pop}')
        return theta_print_factor, theta_template

    def get_coal_stats_templates(self):
        pop_coal_stats_template = self.config.get('Templates', 'pop_coal_stats', fallback='P_{pop} cs')
        comb_coal_stats_template = self.config.get('Templates', 'comb_coal_stats', fallback='C_{comb} cs')
        comb_leaf_coal_stats_template = self.config.get('Templates', 'comb_leaf_coal_stats', fallback='C_{comb}_{leaf} cs')
        return comb_coal_stats_template, comb_leaf_coal_stats_template, pop_coal_stats_template

    def get_mig_stats_template(self):
        comb_migband_mig_stats_template = self.config.get('Templates', 'comb_migband_mig_stats', fallback='C_{comb}_{migband} ms')
        return comb_migband_mig_stats_template

    def get_num_migs_template(self):
        comb_migband_num_migs_template = self.config.get('Templates', 'comb_migband_num_migs', fallback='C_{comb}_{migband} nm')
        return comb_migband_num_migs_template


    def get_migrate_template(self):
        mig_rate = self.config.get('Templates', 'mig_rate', fallback='m_{migband}')
        return mig_rate


def remove_empty_strings(comb_leaves, mig_bands, pops):  # TODO - accept any number of args
    comb_leaves = list(filter(None, comb_leaves))
    pops = list(filter(None, pops))
    mig_bands = list(filter(None, mig_bands))
    return comb_leaves, mig_bands, pops
