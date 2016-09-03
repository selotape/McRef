import pandas as pd
import matplotlib.pyplot as plt
import re



experiment_dir = "G:\\Users\\ronvis\\Dropbox\\Thesis\\ModelCompare\\experiments\\oxford\\simM2.05\\mig2a"
trace_file_name = "data.trace.mig2a.05.tsv"
data_plots_dir = 'data_plots'

burn_in = 50000
skip = 4

print('reading data...')
trace = pd.read_csv(experiment_dir + '\\' + trace_file_name, delimiter='\t')
print('preprocessing data...')
trace.drop('Sample', axis=1, inplace=True)
trace = trace[burn_in:]
trace = trace[skip::]

for column in trace.columns:
    print('plotting column ' + column + '...')
    plot = trace[[column,]].plot(title=column)
    plot_figure = plot.get_figure()

    plot_save_name = experiment_dir + '\\' + data_plots_dir + '\\' + ('trace_' + column + ".png")
    plot_save_name = re.sub('[>]', '', plot_save_name )

    plot_figure.savefig(plot_save_name)
