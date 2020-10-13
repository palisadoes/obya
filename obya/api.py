"""Application API module."""

import json
from collections import namedtuple
from datetime import timezone
import datetime
import time
import re
import pandas as pd

# PIP imports
import urllib3

# Application imports
from obya import Config
from obya.db.table import data


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
        body = {
            'Password': self._config.api_password,
            'AppVersion': '1',
            'AppComments': '',
            'UserName': self._config.api_username,
            'AppKey': self._config.api_key
        }
        url = '{}/session'.format(self._base_url)

        _api = self._http.request(
            'POST', url,
            body=json.dumps(body),
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
        # Initialize key variables
        result = None

        # Get URI to query
        url = '{}/{}'.format(self._base_url, uri.lstrip('/'))

        # Get data
        try:
            _api = self._http.request(
                'GET', url,
                headers={
                    'Session': self.session_key,
                    'UserName': self._config.api_username
                }
            )
        except:
            return result

        # Return result
        if _api.status == 200:
            result = json.loads(_api.data.decode())
        return result

    def latest(self, pair, timeframe, limit=20):
        """Get latest historical results.

        Args:
            pair: Pair to identify
            timeframe: Timeframe to query represented in seconds
            limit: Maximum number of results to return

        Returns:
            result: Historical data

        """
        # Initialize key variables
        result = None

        # Return
        start = int(time.time()) - (timeframe * limit)
        result = self.historical(pair, timeframe, start=start)
        return result

    def historical(self, pair, timeframe, start=None, stop=None):
        """Get historical results.

        Args:
            pair: Pair to identify
            timeframe: Timeframe to query represented in seconds
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
        meta = _interval_span(timeframe)

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
        if bool(_result) is True:
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
        results = self.get(uri)
        markets = results.get('Markets')
        if bool(markets) is True:
            for market in markets:
                if market.get('Name') == cross.upper():
                    result = market.get('MarketId')
                    break
        return result


def _interval_span(timeframe):
    """Get interval and span for lookup.

    Args:
        timeframe: Timeframe to query represented in seconds

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
        if not(timeframe % key) and timeframe >= key:
            interval = value
            span = timeframe // key
            break

    # Return
    result = Meta(interval=interval, span=span)
    return result


def _convert(data_):
    """Convert data to be compatible with database.

    Args:
        data_: Historical data returned from API

    Returns:
        result: List of dicts

    """
    # Initialize key variables
    result = []

    # Create a DataFrame from the list of dicts in the result
    items = data_.get('PriceBars')
    if bool(items) is True:
        for item in items:
            result.append(
                {
                    'open': item['Open'],
                    'high': item['High'],
                    'low': item['Low'],
                    'close': item['Close'],
                    'volume': 0,
                    'timestamp': int(int(
                        re.match(
                            r'^.*?\((\d+)\).*?$',
                            item['BarDate']).group(1)
                    ) / 1000)
                }
            )
        result = pd.DataFrame(result)
    else:
        # Create an empty DataFrame
        result = pd.DataFrame()
    return result


def ingest(secondsago):
    """Ingest data from the API into the database.

    Args:
        secondsago: Amount of time to backfill

    Returns:
        None

    """
    # Initalize key variables
    timeframe = 14400
    batch = 3000
    config = Config()
    timestamps = []

    # Calculate start, start
    stop = int(datetime.datetime.now().replace(
        tzinfo=timezone.utc).timestamp())
    start = stop - secondsago

    # Get start and stop times
    items = list(range(start, stop, timeframe * batch))
    items.append(stop)
    for index, value in enumerate(items[:-1]):
        timestamps.append({'start': value, 'stop': items[index + 1]})

    # Get a list of pairs
    pairs = config.pairs

    # print(items)
    # from pprint import pprint
    # pprint(timestamps)
    # print(pairs)

    # Ingest data
    _api = API()
    for pair in pairs:
        print('Processing {}'.format(pair))
        for timestamp in timestamps:
            df_ = _api.historical(
                pair,
                timeframe,
                start=timestamp['start'],
                stop=timestamp['stop'])
            data.insert(pair, df_)
