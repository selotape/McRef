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

        trim_percentile, dilute_factor, burn_in, num_rows = self.get_data_prep_attributes()

        comb_stats_name = self.config.get('Input', 'comb_stats_file_name', fallback='comb-trace.tsv')
        comb_stats_path = simulation_path + '/' + comb_stats_name  # TODO - use system fs separator
        comb_stats = pd.read_csv(comb_stats_path, sep='\t', skiprows=range(1, burn_in), nrows=num_rows, header=0)
        logger.info("Loaded comb_stats simdata")

        trace_file_name = self.config.get('Input', 'trace_file_name', fallback='trace.tsv')
        trace_path = simulation_path + '/' + trace_file_name  # TODO - use system fs separator
        trace = pd.read_csv(trace_path, sep='\t', skiprows=range(1, burn_in), nrows=num_rows, header=0)
        logger.info("Loaded trace simdata")

        if num_rows:
            assert len(comb_stats) == num_rows, "expected {} rows but found {}".format(num_rows, len(comb_stats))
            assert len(trace) == num_rows, "expected {} rows but got found".format(num_rows, len(trace))

        return comb_stats, trace

    def get_data_prep_attributes(self):
        trim_percentile = self.config.getint('Data', 'trim_percentile', fallback=0)
        dilute_factor = self.config.getint('Data', 'dilute_factor', fallback=0)
        burn_in = self.config.getint('Data', 'skip_rows', fallback=0)
        num_rows = self.config.getint('Data', 'number_of_rows', fallback=None)
        return trim_percentile, dilute_factor, burn_in, num_rows

    def get_simulation_path(self):
        return self.simulation

    def get_comb_pops_and_migs(self):
        comb = self.config.get('ReferenceModel', 'comb')
        comb_leaves = self.config.get('ReferenceModel', 'comb_leaves').split(',')
        pops = self.config.get('ReferenceModel', 'pops').split(',')
        mig_bands = self.config.get('ReferenceModel', 'mig_bands').split(',')

        # remove empty strings
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

    def get_data_config(self):
        theta_print_factor = self.config.getfloat('Input', 'theta_print_factor', fallback=10000.0)
        mig_rate_print_factor = self.config.getfloat('Input', 'mig_rate_print_factor', fallback=0.1)

        return theta_print_factor, mig_rate_print_factor

    def should_save_results(self):
        result = self.config.getboolean("Output", "save_data", fallback=False)
        return result

    def get_log_conf(self):
        return (self.config.get('Logging', 'level', fallback='INFO'),
                self.config.get('Logging', 'file_name', fallback='model_compare.log'))


def remove_empty_strings(comb_leaves, mig_bands, pops):  # TODO - accept any number of args
    comb_leaves = list(filter(None, comb_leaves))
    pops = list(filter(None, pops))
    mig_bands = list(filter(None, mig_bands))
    return comb_leaves, mig_bands, pops
