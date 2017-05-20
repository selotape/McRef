import configparser
import logging
import time

import pandas as pd


class ConfigHandler:
    def __init__(self, simulation):
        self.simulation = simulation
        self.config = configparser.ConfigParser()
        # look for configuration in cwd and in simulation dir. simulation-specific config overrides the one in cwd!
        self.config.read(['config.ini', 'model_compare/config.ini', '%s/config.ini' % simulation])

    def get_gphocs_data(self):
        simulation_path = self.get_simulation_path()

        trim_percentile, dilute_factor, burn_in, num_rows = self.get_data_prep_attributes()


        comb_stats_name = self.config.get('Input', 'comb_stats_file_name')
        comb_stats_path = simulation_path + '/' + comb_stats_name  # TODO - use system fs separator
        comb_stats = pd.read_csv(comb_stats_path, sep='\t', skiprows=range(1, burn_in), nrows=num_rows, header=0)
        logging.info("Loaded comb_stats simdata")

        trace_file_name = self.config.get('Input', 'trace_file_name')
        trace_path = simulation_path + '/' + trace_file_name  # TODO - use system fs separator
        trace = pd.read_csv(trace_path, sep='\t', skiprows=range(1, burn_in), nrows=num_rows, header=0)
        logging.info("Loaded trace simdata")

        return comb_stats, trace

    def get_data_prep_attributes(self):
        trim_percentile = self.config.getint('Data', 'trim_percentile')
        dilute_factor = self.config.getint('Data', 'dilute_factor')
        burn_in = self.config.getint('Data', 'skip_rows')
        num_rows = self.config.getint('Data', 'number_of_rows')
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

    def get_results_paths(self):
        simulation_path = self.get_simulation_path()
        timestamp = time.strftime('%Y%m%d_%H%M')


        results_directory = simulation_path + '/' + self.config.get('Output', 'results_directory') + '/' + timestamp
        results_path = results_directory + '/' + self.config.get('Output', 'results_name')
        summary_path = results_directory + '/' + self.config.get('Output', 'summary_name')
        likelihoods_plot_path = results_directory + '/' + self.config.get('Output', 'likelihoods_plot_name')
        expectation_plot_path = results_directory + '/' + self.config.get('Output', 'expectation_plot_name')
        harmonic_mean_plot_path = results_directory + '/' + self.config.get('Output', 'harmonic_mean_plot_name')

        return results_directory, results_path, likelihoods_plot_path, expectation_plot_path, harmonic_mean_plot_path, \
            summary_path

    def get_column_name_templates(self):  # TODO - add annotations

        theta = self.config.get('Templates', 'theta')
        mig_rate = self.config.get('Templates', 'mig_rate')
        comb_num_coals_template = self.config.get('Templates', 'comb_num_coals')
        comb_leaf_num_coals_template = self.config.get('Templates', 'comb_leaf_num_coals')
        pop_num_coals_template = self.config.get('Templates', 'pop_num_coals')
        comb_coal_stats_template = self.config.get('Templates', 'comb_coal_stats')
        comb_leaf_coal_stats_template = self.config.get('Templates', 'comb_leaf_coal_stats')
        pop_coal_stats_template = self.config.get('Templates', 'pop_coal_stats')
        comb_migband_mig_stats_template = self.config.get('Templates', 'comb_migband_mig_stats')
        comb_migband_num_migs_template = self.config.get('Templates', 'comb_migband_num_migs')

        return theta, mig_rate, comb_num_coals_template, comb_leaf_num_coals_template, pop_num_coals_template, \
            comb_coal_stats_template, comb_leaf_coal_stats_template, pop_coal_stats_template, \
            comb_migband_mig_stats_template, comb_migband_num_migs_template

    def get_data_config(self):
        theta_print_factor = self.config.getfloat('Input', 'theta_print_factor')
        mig_rate_print_factor = self.config.getfloat('Input', 'mig_rate_print_factor')

        return theta_print_factor, mig_rate_print_factor

    def should_save_results(self):
        result = self.config.getboolean("Output", "save_data")
        return result


def remove_empty_strings(comb_leaves, mig_bands, pops):  # TODO - accept any number of args
    comb_leaves = list(filter(None, comb_leaves))
    pops = list(filter(None, pops))
    mig_bands = list(filter(None, mig_bands))
    return comb_leaves, mig_bands, pops
