

def __dilute_data(df, dilute_factor):
    df = df[::dilute_factor]
    return df

def __trim_data(df, percentile, column):

    bottom = df.quantile(percentile / 100)[column]
    top = df.quantile(1 - percentile / 100)[column]

    df = df[(df[column] < top) & (df[column] > bottom)]

    return df


def prepare_data(results, conf):
    trim_percentile, dilute_factor =  conf.get_data_prep_attributes()

    results = __trim_data(results, trim_percentile, 'hyp_gene_likelihood')
    results = __dilute_data(results, dilute_factor)

    return results




