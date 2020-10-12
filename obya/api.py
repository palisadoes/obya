"""Application API module."""

import json
from collections import namedtuple
from datetime import timezone
import datetime
import time
import re

# PIP imports
import urllib3

# Application imports
from obya import Config


class API():
    """Class to get API data."""

    def __init__(self):
        """Initialize the class.

        Args:
            None

        Returns:
            None

        """
        # Initialize key variables
        self._http = urllib3.PoolManager()
        self._config = Config()
        self._base_url = 'https://{}/TradingAPI'.format(
            self._config.api_hostname)

        # Get the session key
        self.session_key = self._login()

    def _login(self):
        """Login to the API.

        Args:
            None

        Returns:
            None

        """
        # Get data
        data = {
            'Password': self._config.api_password,
            'AppVersion': '1',
            'AppComments': '',
            'UserName': self._config.api_username,
            'AppKey': self._config.api_key
        }
        url = '{}/session'.format(self._base_url)

        _api = self._http.request(
            'POST', url,
            body=json.dumps(data),
            headers={'Content-Type': 'application/json'}
        )
        result = json.loads(_api.data.decode())
        session = result['Session']
        return session

    def get(self, uri):
        """Get data from the API.

        Args:
            uri: URI to query

        Returns:
            result: Data from API

        """
        # Get URI to query
        url = '{}/{}'.format(self._base_url, uri.lstrip('/'))

        # Get data
        _api = self._http.request(
            'GET', url,
            headers={
                'Session': self.session_key,
                'UserName': self._config.api_username
            }
        )
        result = json.loads(_api.data.decode())
        return result

    def latest(self, pair, seconds, limit=20):
        """Get latest historical results.

        Args:
            pair: Pair to identify
            seconds: Timeframe to query represented in seconds
            limit: Maximum number of results to return

        Returns:
            result: Historical data

        """
        # Initialize key variables
        result = None

        # Return
        start = int(time.time()) - (seconds * limit)
        result = self.historical(pair, seconds, start=start)
        return result

    def historical(self, pair, seconds, start=None, stop=None):
        """Get historical results.

        Args:
            pair: Pair to identify
            seconds: Timeframe to query represented in seconds
            start: UTC timestamp start
            stop: UTC timestamp stop

        Returns:
            result: Historical data

        """
        # Initialize key variables
        result = None
        if stop is None:
            stop = int(datetime.datetime.now().replace(
                tzinfo=timezone.utc).timestamp())

        # Get the interval
        meta = _interval_span(seconds)

        # Return if timeframe is not found
        if meta.interval is None:
            return result

        # Get market ID
        id_ = self._market_id(pair)

        # Return if not found
        if id_ is False:
            return result

        # Get result
        uri = '''\
/market/{}/barhistorybetween?interval={}&span={}\
&fromTimestampUTC={}&toTimestampUTC={}\
'''.format(id_, meta.interval, meta.span, start, stop)
        _result = self.get(uri)
        result = _convert(_result)
        return result

    def _market_id(self, pair):
        """Get market ID for FX pair.

        Args:
            pair: Pair to identify

        Returns:
            result: Market ID

        """
        # Initialize key variables
        result = None

        # Get URI to query
        p1_ = pair[:3]
        p2_ = pair[3:]
        query = '{}%2F{}'.format(p1_, p2_)
        cross = '{}/{}'.format(p1_, p2_)
        uri = '''\
market/search?SearchByMarketName=TRUE&Query={}&MaxResults=10'''.format(query)

        # Get data
        data = self.get(uri)
        results = data.get('Markets')
        if bool(results) is True:
            for item in results:
                if item.get('Name') == cross.upper():
                    result = item.get('MarketId')
                    break
        return result


def _interval_span(seconds):
    """Get interval and span for lookup.

    Args:
        seconds: Timeframe to query represented in seconds

    Returns:
        result: Meta object

    """
    # Initialize key variables
    Meta = namedtuple('Meta', 'interval span')
    interval = None
    span = None
    result = None
    lookup = {
        3600: 'HOUR',
        60: 'MINUTE',
        86400: 'DAY',
        604800: 'WEEK'
    }

    # Get the interval
    for key, value in sorted(lookup.items(), reverse=True):
        if not(seconds % key) and seconds >= key:
            interval = value
            span = seconds // key
            break

    # Return
    result = Meta(interval=interval, span=span)
    return result


def _convert(data):
    """Convert data to be compatible with database.

    Args:
        data: Historical data returned from API

    Returns:
        result: List of dicts

    """
    # Initialize key variables
    result = []
    items = data['PriceBars']

    # Get result
    for item in items:
        result.append(
            {
                'open': item['Open'],
                'high': item['High'],
                'low': item['Low'],
                'close': item['Close'],
                'timestamp': int(int(
                    re.match(r'^.*?\((\d+)\).*?$', item['BarDate']).group(1)
                ) / 1000)
            }
        )
    return result
