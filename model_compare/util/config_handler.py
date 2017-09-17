import configparser
import os
import time

import pandas as pd

from model_compare.util.log import module_logger

logger = module_logger(__name__)


class ConfigHandler:
    def __init__(self, simulation_path):

        self.config = configparser.ConfigParser()

        # look for configuration in cwd and in simulation dir. simulation-specific config overrides the one in cwd!
        self.config.read(['config.ini', 'model_compare/config.ini', '%s/config.ini' % simulation_path])

        self.simulation_path = simulation_path

        if (self.clade and self.comb) or (not self.clade and not self.comb):
            raise ConfigurationError("Exactly one of 'clade' and 'comb' must be configured")

        self.debug_enabled = self.config.getboolean('Debug', 'enabled', fallback=False)
        self.should_save_results = self.config.getboolean("Output", "save_data", fallback=False)
        self.skip_rows = self.config.getint('Data', 'skip_rows', fallback=0)
        self.log_conf = (self.config.get('Logging', 'level', fallback='INFO'), self.config.get('Logging', 'file_name', fallback=None))

        theta_print_factor = self.config.getfloat('Input', 'theta_print_factor')
        theta_template = self.config.get('Templates', 'theta', fallback='theta_{pop}')
        self.theta_setup = theta_print_factor, theta_template

        mig_rate_print_factor = self.config.getfloat('Input', 'mig_rate_print_factor')
        mig_rate_template = self.config.get('Templates', 'mig_rate', fallback='m_{migband}')
        self.migrate_setup = mig_rate_print_factor, mig_rate_template

        self.results_paths = self._get_results_paths()

        self.clade_coal_templates = self._get_clade_coal_templates()

    @property
    def clade(self):
        return self.config.get('ReferenceModel', 'clade', fallback=None)

    @property
    def comb(self):
        return self.config.get('ReferenceModel', 'comb', fallback=None)

    def load_ref_data(self):
        stats_file_config = 'clade_stats_file' if self.clade else 'comb_stats_file'
        ref_stats = self._load_input_file(stats_file_config)
        return ref_stats

    def load_trace_data(self):
        trace = self._load_input_file('trace_file', index_col='Sample')
        return trace

    def load_hyp_data(self):
        hyp_stats = self._load_input_file('hyp_stats_file')
        return hyp_stats

    def _load_input_file(self, config_key, index_col='iteration'):
        input_file_path = self.config.get('Input', config_key)
        trace = pd.read_csv(input_file_path, sep='\t', skiprows=range(1, self.skip_rows), header=0, index_col=index_col)
        logger.info("Loaded " + config_key)
        return trace

    def get_comb_reference_tree(self):
        comb_leaves = self._fetch_config_list('ReferenceModel', 'comb_leaves')
        hyp_pops = self._fetch_config_list('ReferenceModel', 'hyp_pops')
        hyp_mig_bands = self._fetch_config_list('ReferenceModel', 'hyp_mig_bands')

        return self.comb, comb_leaves, hyp_pops, hyp_mig_bands

    def get_clade_reference_tree(self):
        hyp_pops = self._fetch_config_list('ReferenceModel', 'hyp_pops')
        hyp_mig_bands = self._fetch_config_list('ReferenceModel', 'hyp_mig_bands')

        return self.clade, hyp_pops, hyp_mig_bands

    def get_hypothesis_tree(self):
        pops = self._fetch_config_list('Debug', 'hypothesis_pops')
        migs = self._fetch_config_list('Debug', 'hypothesis_migbands')

        return pops, migs

    def _fetch_config_list(self, section, key):
        return [v.strip() for v in self.config.get(section, key).split(',') if v]

    def _get_results_paths(self):
        simulation_path = self.simulation_path
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

    def _get_clade_coal_templates(self):
        clade_num_coals_template = self.config.get('Templates', 'clade_num_coals', fallback='{clade}_num_coals_total')
        clade_coal_stats_template = self.config.get('Templates', 'clade_coal_stats', fallback='{clade}_coal_stats_total')
        return clade_num_coals_template, clade_coal_stats_template


class ConfigurationError(Exception):
    pass
