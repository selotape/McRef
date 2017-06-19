from pandas import DataFrame

from model_compare.util.log import module_logger

logger = module_logger(__name__)


def align_input_data(comb_trace: DataFrame, trace: DataFrame):
    joined = comb_trace.join(trace)
    logger.info("Aligned input data")
    return joined[list(comb_trace.columns)], joined[list(trace.columns)]


def clean_results(results: DataFrame, trim_percentile):
    results = _remove_percentiles(results, trim_percentile, 'rbf_ratio')
    logger.info("Cleaned results data")

    return results


def _remove_percentiles(df: DataFrame, percentile, column):
    bottom = df.quantile(percentile / 100)[column]
    top = df.quantile(1 - percentile / 100)[column]

    df = df[(df[column] < top) & (df[column] > bottom)]

    return df
