from model_compare.probability_functions import ln_normalize
from numpy import exp, floor


def __trim_head(df, tail_length):
    df = df[-tail_length:]
    return df

def __dilute_data(df, dilute_factor):
    df = df[::dilute_factor]
    return df

def __remove_percentiles(df, percentile, column):

    bottom = df.quantile(percentile / 100)[column]
    top = df.quantile(1 - percentile / 100)[column]

    df = df[(df[column] < top) & (df[column] > bottom)]

    return df



def preprocess_data(results, conf):
    trim_percentile, dilute_factor, tail_length =  conf.get_data_prep_attributes()

    results = __trim_head(results, tail_length)
    results = __remove_percentiles(results, trim_percentile, 'hyp_gene_likelihood')
    results = __dilute_data(results, dilute_factor)

    return results

def normalize_data(dataframe):
    for column in dataframe.columns:
        dataframe['norm_' + column] = ln_normalize(dataframe[column])
    return dataframe

def exponent_normalized_data(dataframe):
    normalized_columns = (column for column in dataframe.columns if 'norm' in column)
    for column in normalized_columns:
        dataframe['exp_' + column] = exp(dataframe[column])

    floored_df = dataframe.apply(floor)
    exponented_columns = (column for column in floored_df.columns if 'exp' in column)
    for column in exponented_columns:
        print('\ncolumn ' + column + ':')
        print(floored_df[column].value_counts())

    return dataframe


