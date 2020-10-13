"""Application module to manage email formatting."""


def email(_df):
    """Read a configuration file.

    Args:
        _df: DataFrame

    Returns:
        result: Formatted string

    """
    # Initialize key variables
    df_ = _df.copy()
    drops = 'timestamp open high low close volume k_s d_s delta_s'

    # Drop unwanted columns. Reset index to 'date'
    df_ = df_.drop(columns=drops.split())
    df_.set_index('date', inplace=True)
    result = df_.to_string()
    # print(result)
    return result
