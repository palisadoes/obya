"""Application api url module."""

from obya import OBYA_API_SITE_PREFIX

def stoch(pair):
    """Return URL for showing chart pages.

    Args:
        pair: Pair to be viewed

    Returns:
        result: URL

    """
    # Return
    result = '{}/stoch/{}'.format(OBYA_API_SITE_PREFIX, pair)
    return result
