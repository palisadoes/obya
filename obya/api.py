"""Application API module."""

# PIP imports
import urllib3
import json

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

    def hours(self, pair, interval=1, max_results=20):
        """Get hourly historical results.

        Args:
            pair: Pair to identify
            interval: Hourly interval
            max_results: Maximum number of results to return

        Returns:
            result: Historical data

        """
        # Initialize key variables
        id_ = self._market_id(pair)
        uri = (
            '/market/{}/barhistory?interval=HOUR&span={}&PriceBars={}'.format(
                id_, interval, max_results))
        result = self.get(uri)
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
