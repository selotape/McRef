import configparser
import os
import time

import pandas as pd

from model_compare.util.log import module_logger

logger = module_logger(__name__)


class ConfigHandler:
    def __init__(self, simulation, is_clade):
        self.simulation = simulation
        self.config = configparser.ConfigParser()
        # look for configuration in cwd and in simulation dir. simulation-specific config overrides the one in cwd!
        self.config.read(['config.ini', 'model_compare/config.ini', '%s/config.ini' % simulation])
        self.clade_enabled = is_clade

    def load_ref_data(self):
        if self.is_clade_enabled():
            ref_stats = self._load_input_file('clade_stats_file')
        else:
            ref_stats = self._load_input_file('comb_stats_file')
        return ref_stats

    def load_trace_data(self):
        trace = self._load_input_file('trace_file', index_col='Sample')
        return trace

    def load_hyp_data(self):
        hyp_stats = self._load_input_file('hyp_stats_file')
        return hyp_stats

    def _load_input_file(self, config_key, index_col='iteration'):
        simulation_path = self.get_simulation_path()
        burn_in = self.get_burn_in()
        trace_file_name = self.config.get('Input', config_key)
        trace_path = simulation_path + '/' + trace_file_name
        trace = pd.read_csv(trace_path, sep='\t', skiprows=range(1, burn_in), header=0, index_col=index_col)
        logger.info("Loaded " + config_key)
        return trace

    def get_simulation_path(self):
        return self.simulation

    def get_comb_reference_tree(self):
        comb = self.config.get('ReferenceModel', 'comb')
        comb_leaves = self.config.get('ReferenceModel', 'comb_leaves').split(',')
        hyp_pops = self.config.get('ReferenceModel', 'hyp_pops').split(',')
        comb_mig_bands = self.config.get('ReferenceModel', 'comb_mig_bands').split(',')
        hyp_mig_bands = self.config.get('ReferenceModel', 'hyp_mig_bands').split(',')

        for l in comb_leaves, comb_mig_bands, hyp_pops, hyp_mig_bands:
            l[:] = [i.strip() for i in l if i]

        return comb, comb_leaves, hyp_pops, comb_mig_bands, hyp_mig_bands

    def get_clade_reference_tree(self):
        clade = self.config.get('ReferenceModel', 'clade')
        hyp_pops = self.config.get('ReferenceModel', 'hyp_pops').split(',')
        hyp_mig_bands = self.config.get('ReferenceModel', 'hyp_mig_bands').split(',')

        for l in hyp_pops, hyp_mig_bands:
            l[:] = [i.strip() for i in l if i]

        return clade, hyp_pops, hyp_mig_bands

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

        return (debug_directory, results_path, likelihoods_plot_path, expectation_plot_path,
                harmonic_mean_plot_path, summary_path)

    def get_comb_num_coals_templates(self):
        comb_leaf_num_coals_template = self.config.get('Templates', 'comb_leaf_num_coals', fallback='C_{comb}_{leaf} nc')
        comb_num_coals_template = self.config.get('Templates', 'comb_num_coals', fallback='C_{comb} nc')
        return comb_leaf_num_coals_template, comb_num_coals_template

    def get_comb_coal_stats_templates(self):
        comb_coal_stats_template = self.config.get('Templates', 'comb_coal_stats', fallback='C_{comb} cs')
        comb_leaf_coal_stats_template = self.config.get('Templates', 'comb_leaf_coal_stats', fallback='C_{comb}_{leaf} cs')
        return comb_coal_stats_template, comb_leaf_coal_stats_template

    def get_comb_migs_templates(self):
        comb_num_migs_template = self.config.get('Templates', 'comb_migband_num_migs', fallback='C_{comb}_{migband} nm')
        comb_mig_stats_template = self.config.get('Templates', 'comb_migband_mig_stats', fallback='C_{comb}_{migband} ms')
        return comb_num_migs_template, comb_mig_stats_template

    def get_hyp_coal_templates(self):
        pop_coal_stats_template = self.config.get('Templates', 'hyp_pop_coal_stats', fallback='P_{pop} cs')
        pop_num_coals_template = self.config.get('Templates', 'hyp_pop_num_coals', fallback='P_{pop} nc')
        return pop_coal_stats_template, pop_num_coals_template

    def get_hyp_mig_templates(self):
        hyp_mig_stats_template = self.config.get('Templates', 'hyp_migband_mig_stats', fallback='MB_{migband} ms')
        hyp_num_migs_template = self.config.get('Templates', 'hyp_migband_num_migs', fallback='MB_{migband} nm')
        return hyp_mig_stats_template, hyp_num_migs_template

    def get_clade_coal_templates(self):
        clade_num_coals_template = self.config.get('Templates', 'clade_num_coals', fallback='{clade}_num_coals_total')
        clade_coal_stats_template = self.config.get('Templates', 'clade_coal_stats', fallback='{clade}_coal_stats_total')
        return clade_num_coals_template, clade_coal_stats_template

    def get_theta_setup(self):
        theta_print_factor = self.config.getfloat('Input', 'theta_print_factor', fallback=10000.0)
        theta_template = self.config.get('Templates', 'theta', fallback='theta_{pop}')
        return theta_print_factor, theta_template

    def get_migrate_setup(self):
        mig_rate_print_factor = self.config.getfloat('Input', 'mig_rate_print_factor', fallback=0.1)
        mig_rate_template = self.config.get('Templates', 'mig_rate', fallback='m_{migband}')
        return mig_rate_print_factor, mig_rate_template

    def get_burn_in(self):
        return self.config.getint('Data', 'skip_rows', fallback=0)

    def get_log_conf(self):
        return (self.config.get('Logging', 'level', fallback='INFO'),
                self.config.get('Logging', 'file_name', fallback='model_compare.log'))

    def is_debug_enabled(self):
        return self.config.getboolean('Debug', 'enabled', fallback=False)

    def is_clade_enabled(self):
        return self.clade_enabled

    def should_save_results(self):
        result = self.config.getboolean("Output", "save_data", fallback=False)
        return result
