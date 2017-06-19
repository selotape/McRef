from pandas import DataFrame

from model_compare.util.log import module_logger

logger = module_logger(__name__)


def align_input_data(comb_trace: DataFrame, trace: DataFrame):
    joined = comb_trace.join(trace)
    logger.info("Aligned input data")
    return joined[list(comb_trace.columns)], joined[list(trace.columns)]
