import unittest
from unittest import mock
from ilabs.client import ilabs_datavault_api as dv, __version__


_DUMMY_USER_KEY = 'dummy-user-key'
_DUMMY_DATAVAULT_KEY = '0123456789'


class TestIlabsApi(unittest.TestCase):

    def test_request(self):

        api = dv.ILabsDatavaultApi(user_key=_DUMMY_USER_KEY, datavault_key=_DUMMY_DATAVAULT_KEY)

        mock_response = mock.Mock()
        mock_response.getcode = lambda: 200
        mock_request = mock.Mock(return_value=mock_response)
        with mock.patch('ilabs.client.ilabs_datavault_api.send_request', mock_request) as request:

            api._request('OPTIONS', 'http://www.google.com', b'some content',
                content_type='test/test')

            self.assertEqual(request.call_count, 1)
            request.assert_called_with(
                'OPTIONS',
                'http://www.google.com',
                data=b'some content',
                headers={
                    'User-Agent'   : 'ILabs API client ' + __version__,
                    'Content-Type' : 'test/test',
                    'User-Key'     : 'dummy-user-key',
                    'X-ILABS-KEY'  : '0123456789',
                    'Cache-Control': 'no-cache'
                },
                query=None
            )

    def test_ping(self):

        api = dv.ILabsDatavaultApi(user_key=_DUMMY_USER_KEY, datavault_key=_DUMMY_DATAVAULT_KEY)
        api._request = mock.Mock(return_value=b'{ "ping": "pong" }')

        rc = api.ping()
        api._request.assert_called_once_with('GET', 'https://ilabs-api.innodata.com/datavault/ping', query=None)

        self.assertEqual(rc, {'ping': 'pong'})



if __name__ == '__main__':
    unittest.main()
