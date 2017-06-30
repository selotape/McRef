import matplotlib

matplotlib.use('agg')  # Order is important for plot platform-independence
import pandas as pd


def _copy_rename_columns(columns_map, df):
    result = df[list(columns_map.keys())].copy()
    result.rename(columns=columns_map, inplace=True)
    return result


def save_plot(data_frame: pd.DataFrame, save_path: str, title: str):
    plot = data_frame.plot(title=title)
    plot_figure = plot.get_figure()
    plot_figure.savefig(save_path + ".line.png", bbox_inches='tight')
