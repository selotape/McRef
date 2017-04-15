from model_compare.probability_functions import ln_normalize
from numpy import exp, floor


def __trim_head(df, head_length):
    df = df[head_length:]
    return df


def __dilute_data(df, dilute_factor):
    df = df[::dilute_factor]
    return df


def __remove_percentiles(df, percentile, column):
    bottom = df.quantile(percentile / 100)[column]
    top = df.quantile(1 - percentile / 100)[column]

    df = df[(df[column] < top) & (df[column] > bottom)]

    return df


def equate_lengths(df1, df2):
    length = min((len(df1), len(df2)))
    df1 = df1[:length]
    df2 = df2[:length]
    return df1, df2


def preprocess_data(results, conf):
    trim_percentile, dilute_factor, burn_in = conf.get_data_prep_attributes()

    results = __trim_head(results, burn_in)
    results = __remove_percentiles(results, trim_percentile, 'hyp_gene_likelihood')
    results = __dilute_data(results, dilute_factor)

    return results


def normalize_data(dataframe):
    for column in dataframe.columns:
        dataframe['norm_' + column] = ln_normalize(dataframe[column])
    return dataframe
