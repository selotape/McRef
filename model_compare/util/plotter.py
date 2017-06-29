import matplotlib

matplotlib.use('agg')
import pandas as pd


def save_plot(data_frame: pd.DataFrame, save_path: str, title: str):
    plot = data_frame.plot(title=title)
    plot_figure = plot.get_figure()
    plot_figure.savefig(save_path + ".line.png", bbox_inches='tight')
