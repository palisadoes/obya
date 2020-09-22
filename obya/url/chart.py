"""Application page url module."""

from obya import OBYA_WEB_SITE_PREFIX


def stoch(pair):
    """Return URL for showing chart pages.

    Args:
        pair: Pair to be viewed

    Returns:
        result: URL

    """
    # Return
    result = '{}/chart/stoch/{}'.format(OBYA_WEB_SITE_PREFIX, pair)
    return result
