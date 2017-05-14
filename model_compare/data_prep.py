import logging

from pandas import DataFrame


def equate_lengths(df1: DataFrame, df2: DataFrame):
    length = min((len(df1), len(df2)))
    df1 = df1[:length]
    df2 = df2[:length]
    return df1, df2


def preprocess_data(results: DataFrame, conf):
    trim_percentile, dilute_factor, burn_in = conf.get_data_prep_attributes()

    results = _trim_head(results, burn_in)
    results = _remove_percentiles(results, trim_percentile, 'rbf_ratio')
    results = _dilute_data(results, dilute_factor)
    logging.info("Preprocessed results data")

    return results


def _trim_head(df: DataFrame, head_length):
    df = df[head_length:]
    return df


def _dilute_data(df: DataFrame, dilute_factor: int):
    df = df[::dilute_factor]
    return df


def _remove_percentiles(df: DataFrame, percentile, column):
    bottom = df.quantile(percentile / 100)[column]
    top = df.quantile(1 - percentile / 100)[column]

    df = df[(df[column] < top) & (df[column] > bottom)]

    return df
