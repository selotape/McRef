import os
import configparser
import pandas as pd

class ConfigHandler:
    def __init__(self, simulation):
        self.simulation = simulation
        self.config = configparser.ConfigParser()
        self.config.read(os.path.dirname(os.path.realpath(__file__)) + '\\' + 'config.ini')

    def get_simulation_path(self):
        simulations_path = self.config.get('Input', 'simulations_path')
        return simulations_path + '\\' + self.simulation

    def get_clades_pops_and_migs(self):
        clades = self.config.get('Clade','clades').split(',')
        pops = self.config.get('Clade', 'pops').split(',')
        mig_bands = self.config.get('Clade', 'mig_bands').split(',')

        #remove empty strings
        clades = list(filter(None, clades))
        pops = list(filter(None, pops))
        mig_bands = list(filter(None, mig_bands))

        return clades, pops, mig_bands

    def get_data_frames(self):
        simulation_path = self.get_simulation_path()

        clade_stats_name = self.config.get('Input','clade_stats_file_name')
        clade_stats_path = simulation_path + '\\' + clade_stats_name
        clade_stats = pd.read_csv(clade_stats_path, sep='\t')

        trace_file_name = self.config.get('Input','trace_file_name')
        trace_path = simulation_path + '\\' + trace_file_name
        trace = pd.read_csv(trace_path, sep='\t')

        return clade_stats, trace

    def get_results_paths(self):
        simulation_path = self.get_simulation_path()

        results_directory_path = simulation_path + '\\' + self.config.get('Output','results_directory')
        results_path = results_directory_path + '\\' + self.config.get('Output','results_name')
        summary_path = results_directory_path + '\\' + self.config.get('Output','summary_name')
        likelihoods_plot_path = results_directory_path + '\\' + self.config.get('Output','likelihoods_plot_name')
        expectation_plot_path = results_directory_path + '\\' + self.config.get('Output','expectation_plot_name')

        return results_path, likelihoods_plot_path, expectation_plot_path, summary_path

    def get_prefixes(self):
        pop_infix = self.config.get('Clade','pop_inffix')
        theta_prefix = self.config.get('Clade','theta_prefix')
        num_coals_suffix = self.config.get('Clade','num_coals_suffix')
        coal_stats_suffix = self.config.get('Clade','coal_stats_suffix')
        return pop_infix, theta_prefix, num_coals_suffix, coal_stats_suffix

    def get_data_config(self):
        print_factor = self.config.getfloat('Data','print_factor')
        tail_length = self.config.getint('Data','expectation_tail_length')
        return print_factor, tail_length
