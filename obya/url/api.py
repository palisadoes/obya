"""Application api url module."""

from obya import OBYA_API_SITE_PREFIX


def stoch(pair, periods=None):
    """Return URL for showing chart pages.

    Args:
        pair: Pair to be viewed
        periods: Number of periods for summarization

    Returns:
        result: URL

    """
    # Return
    result = '{}/stoch/{}'.format(OBYA_API_SITE_PREFIX, pair)
    if bool(periods) and isinstance(periods, int):
        result = '{}?periods={}'.format(result, periods)
    return result
