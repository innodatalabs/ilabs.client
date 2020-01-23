import logging
import sys
from ilabs.client import __version__


from urllib.request import Request, urlopen
from urllib.parse import urlencode
from urllib.error import HTTPError


MAX_ATTEMPTS = 3
ILABS_USER_AGENT = 'ILabs API client ' + __version__


def send_request(method, url, data=None, headers=None, query=None):
    logging.debug('%s %s %s', method, url, query)
    assert method in ('GET', 'POST', 'DELETE')
    if data is not None:
        assert method == 'POST'
    else:
        assert method in ('GET', 'POST', 'DELETE')

    if query is not None:
        url = url + '?' + urlencode(query)
        logging.debug('url with query string encoded: %s', url)

    for _ in range(MAX_ATTEMPTS-1):
        try:
            return urlopen(Request(url, headers=headers, data=data))
        except HTTPError as err:
            if 500 <= err.status_code <= 599:
                logging.error('HTTP 500: will retry')
                continue
            raise err

    return urlopen(Request(url, headers=headers, data=data))
