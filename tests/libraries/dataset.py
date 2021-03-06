"""Module to create datasets for unittesting."""

import pandas as pd
import random
import string


def dataset():
    """Create dataset for testing.

    Args:
        None

    Returns:
        result: Testing DataFrame

    """
    data = {
        'open': [
            85.882, 86.184, 86.419, 86.465, 86.964,
            86.983, 86.714, 87.117, 87.032, 87.175
        ],
        'high': [
            86.249, 86.420, 86.512, 86.991, 87.015,
            86.993, 87.139, 87.176, 87.078, 87.401,
        ],
        'low': [
            85.864, 86.126, 86.304, 86.456, 86.812,
            86.669, 86.681, 86.756, 86.731, 87.085
        ],
        'close': [
            86.184, 86.420, 86.467, 86.964, 86.985,
            86.714, 87.116, 87.030, 86.731, 87.365
        ],
        'volume': [
            29085, 19842, 12649, 22248, 17200,
            21321, 26309, 23287, 5450, 6023
        ],
        'timestamp': [
            1486641600, 1486656000, 1486670400, 1486684800, 1486699200,
            1486713600, 1486728000, 1486742400, 1486756800, 1486936800
        ]
    }
    result = pd.DataFrame(data=data)
    return result


def random_string(length=20):
    """Create random string for testing.

    Args:
        None

    Returns:
        result: Random string

    """
    # Return
    result = ''.join(random.SystemRandom().choice(
        string.ascii_uppercase + string.digits) for _ in range(length))
    return result
