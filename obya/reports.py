"""Application module to manage email formatting."""


def email(_df, pair):
    """Read a configuration file.

    Args:
        _df: DataFrame
        pair: Pair corresponding to DataFrame

    Returns:
        result: Formatted string

    """
    # Initialize key variables
    result = ''
    drops = 'timestamp open high low close volume k_s d_s delta_s'
    df_ = _df.copy()

    if df_.empty is False:
        # Create heading for the pair
        result = '\n{}\n\n{}\n'.format('-' * 80, pair.upper())

        # Drop unwanted columns. Reset index to 'date'
        df_ = df_.drop(columns=drops.split())
        df_.set_index('date', inplace=True)

        # Add data to report
        result = '{}\n{}'.format(result, df_.to_string())
    return result
