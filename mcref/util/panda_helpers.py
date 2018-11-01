import matplotlib
import pandas as pd
from mcref.util.log import module_logger

log = module_logger(__name__)

EPSILON = 3.14e-10


def copy_then_rename_columns(df, columns_map) -> pd.DataFrame:
    result = df[list(columns_map.keys())].copy()
    result.rename(columns=columns_map, inplace=True)
    return result


def save_plot(data_frame: pd.DataFrame, save_path: str, title: str):
    matplotlib.use('agg')

    plot = data_frame.plot(title=title)
    plot_figure = plot.get_figure()
    plot_figure.savefig(save_path + ".line.png", bbox_inches='tight')


def align_by_index(df1: pd.DataFrame, df2: pd.DataFrame):
    joined = df1.join(df2, how='inner')
    log.info("Aligned data frames")
    return joined[list(df1.columns)], joined[list(df2.columns)]


def replace_zeroes_with_epsilon(df: pd.DataFrame):
    df.replace(to_replace=0.0, value=EPSILON, inplace=True)
