import time
import configparser
import pandas as pd

class ConfigHandler:
    def __init__(self, simulation):
        self.simulation = simulation
        self.config = configparser.ConfigParser()
        self.config.read(['config.ini', '%s/config.ini' % simulation]) # look for configuration in cwd and in simulation dir. simulation-specific config overrides the one in cwd!

    def get_simulation_path(self):
        return self.simulation


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
        clade_stats_path = simulation_path + '/' + clade_stats_name
        clade_stats = pd.read_csv(clade_stats_path, sep='\t')

        trace_file_name = self.config.get('Input','trace_file_name')
        trace_path = simulation_path + '/' + trace_file_name
        trace = pd.read_csv(trace_path, sep='\t')

        return clade_stats, trace


    def get_results_paths(self):
        simulation_path = self.get_simulation_path()
        # timestamp = datetime.now().strftime("%H.%M_%d.%m.%Y")
        timestamp = str(time.time())

        results_directory = simulation_path + '/' + self.config.get('Output','results_directory') + '/' + timestamp
        results_path =          results_directory + '/' + self.config.get('Output','results_name')
        summary_path =          results_directory + '/' + self.config.get('Output','summary_name')
        likelihoods_plot_path = results_directory + '/' + self.config.get('Output','likelihoods_plot_name')
        expectation_plot_path = results_directory + '/' + self.config.get('Output','expectation_plot_name')
        harmonic_mean_plot_path= results_directory + '/' + self.config.get('Output','harmonic_mean_plot_name')

        return results_directory, results_path, likelihoods_plot_path, expectation_plot_path, harmonic_mean_plot_path, summary_path


    def get_prefixes(self):
        pop_infix =         self.config.get('Clade','pop_inffix')
        theta_prefix =      self.config.get('Clade','theta_prefix')
        num_coals_suffix =  self.config.get('Clade','num_coals_suffix')
        coal_stats_suffix = self.config.get('Clade','coal_stats_suffix')
        mig_rate_prefix =   self.config.get('Clade','mig_rate_prefix')
        num_migs_suffix =   self.config.get('Clade','num_migs_suffix')
        mig_stats_suffix =  self.config.get('Clade','mig_stats_suffix')

        return pop_infix, theta_prefix, num_coals_suffix, coal_stats_suffix, mig_rate_prefix, num_migs_suffix, mig_stats_suffix


    def get_data_config(self):
        theta_print_factor = self.config.getfloat('Data','theta_print_factor')
        mig_rate_print_factor = self.config.getfloat('Data', 'mig_rate_print_factor')
        tail_length = self.config.getint('Data','expectation_tail_length')

        return theta_print_factor, mig_rate_print_factor, tail_length
