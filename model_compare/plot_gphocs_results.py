import os

import logging
import pandas as pd
import matplotlib.pyplot as plt
import re


BURN_IN = 50000
SKIP = 4
EXPERIMENT_DIR = "G:\\Users\\ronvis\\Dropbox\\Thesis\\ModelCompare\\experiments\\oxford"


def plotnic(experiment_dir, data_plots_dir, trace_file_name):
    logging.info('reading data...')
    trace = pd.read_csv(experiment_dir + '\\' + trace_file_name, delimiter='\t')
    logging.info('preprocessing data...')
    trace.drop('Sample', axis=1, inplace=True)
    trace = trace[BURN_IN:]
    trace = trace[SKIP::]
    for column in trace.columns:
        logging.info('plotting column ' + column + '...')
        plot = trace[[column, ]].plot(title=column)
        plot_figure = plot.get_figure()

        plot_save_path = data_plots_dir + '\\' + ('trace_' + column + ".png")
        plot_save_path = re.sub('[>]', '', plot_save_path)

        plot_figure.savefig(plot_save_path)
        plt.close(plot_figure)


def plot_trace_file(base_dir, tau, ac_mig, ca_mig):

    experiment = "M3." + tau + ".migAC_" + ac_mig + "_" + ca_mig
    logging.info('===plotting ' + experiment + ': ===')

    experiment_dir = base_dir + '\\' + experiment
    trace_file_name = "trace." + experiment + ".tsv"
    data_plots_dir = experiment_dir + '\\' + 'data_plots'

    try:
        if not os.path.exists(data_plots_dir):
            os.makedirs(data_plots_dir)
        plotnic(experiment_dir, data_plots_dir, trace_file_name)
    except OSError as err:
        logging.error('failed plotting ' + ' '.join((experiment_dir, data_plots_dir, trace_file_name)))
        logging.error(str(err))



plot_trace_file(EXPERIMENT_DIR, '00', '0', '0')
for tau in ('01', '05', '10', '15'):
    plot_trace_file(EXPERIMENT_DIR, tau, '0', '0')
    for mig in ('1', '2', '4'):
        plot_trace_file(EXPERIMENT_DIR, tau, mig, '0')
        plot_trace_file(EXPERIMENT_DIR, tau, '0', mig)

