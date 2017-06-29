from pandas import DataFrame

from model_compare.util.log import module_logger

log = module_logger(__name__)


def align_by_index(df1: DataFrame, df2: DataFrame):
    joined = df1.join(df2, how='inner')
    log.info("Aligned data frames")
    return joined[list(df1.columns)], joined[list(df2.columns)]
