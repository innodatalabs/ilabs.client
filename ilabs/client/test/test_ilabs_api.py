import unittest
import mock
from ilabs.client import ilabs_api, __version__


_DUMMY_USER_KEY = '0123456789'


class TestIlabsApi(unittest.TestCase):

    def test_request(self):

        api = ilabs_api.ILabsApi(user_key=_DUMMY_USER_KEY)

        mock_response = mock.Mock()
        mock_response.getcode = lambda: 200
        mock_request = mock.Mock(return_value=mock_response)
        with mock.patch('ilabs.client.ilabs_api.send_request', mock_request) as request:

            api._request('OPTIONS', 'http://www.gogole.com', b'some content',
                content_type='test/test')

            self.assertEqual(request.call_count, 1)
            request.assert_called_with(
                'OPTIONS',
                'http://www.gogole.com',
                data=b'some content',
                query=None,
                headers={
                    'User-Agent': 'ILabs API client ' + __version__,
                    'Content-Type': 'test/test',
                    'User-Key': '0123456789',
                    'Cache-Control': 'no-cache'
                }
            )

    def test_ping(self):

        api = ilabs_api.ILabsApi(user_key=_DUMMY_USER_KEY)
        api._request = mock.Mock(return_value=b'{ "ping": "pong" }')

        rc = api.ping()
        api._request.assert_called_once_with('GET', 'https://api.innodatalabs.com/v1/ping', query=None)

        self.assertEqual(rc, {'ping': 'pong'})

    def test_upload_input(self):
        api = ilabs_api.ILabsApi(user_key=_DUMMY_USER_KEY)
        api._request = mock.Mock(return_value=b'{ "bytes_accepted": 5, "input_filename": "123456.bin" }')

        rc = api.upload_input(b'hello')
        api._request.assert_called_once_with(
            'POST',
            'https://api.innodatalabs.com/v1/documents/input/',
            b'hello',
            content_type='application/octet-stream', query=None)

        self.assertEqual(rc, {'bytes_accepted': 5, 'input_filename': '123456.bin'})

        rc = api.upload_input(b'hello', filename='XXX')
        api._request.assert_called_with(
            'POST',
            'https://api.innodatalabs.com/v1/documents/input/XXX',
            b'hello',
            content_type='application/octet-stream', query=None)

        self.assertEqual(rc, {'bytes_accepted': 5, 'input_filename': '123456.bin'})

    def test_download_input(self):
        api = ilabs_api.ILabsApi(user_key=_DUMMY_USER_KEY)
        api._request = mock.Mock(return_value=b'contents')

        rc = api.download_input('XXX')
        api._request.assert_called_once_with(
            'GET',
            'https://api.innodatalabs.com/v1/documents/input/XXX',
            query=None)

        self.assertEqual(rc, b'contents')

    def test_predict(self):
        api = ilabs_api.ILabsApi(user_key=_DUMMY_USER_KEY)
        api._request = mock.Mock(return_value=b'''\
{
    "task_id"            : "test-task-id",
    "task_cancel_url"    : "https://api.innodatalabs.com/v1/cancel/xxx",
    "task_status_url"    : "https://api.innodatalabs.com/v1/status/xxx",
    "document_output_url": "https://api.innodatalabs.com/v1/output/123456.bin",
    "output_filename"    : "https://api.innodatalabs.com/v1/output/yyyy"
}
''')

        rc = api.predict(domain='test-domain', filename='123456.bin')
        api._request.assert_called_once_with(
            'GET',
            'https://api.innodatalabs.com/v1/reference/test-domain/123456.bin',
            query=None
        )

        self.assertEqual(rc, {
    "task_id"            : "test-task-id",
    "task_cancel_url"    : "https://api.innodatalabs.com/v1/cancel/xxx",
    "task_status_url"    : "https://api.innodatalabs.com/v1/status/xxx",
    "document_output_url": "https://api.innodatalabs.com/v1/output/123456.bin",
    "output_filename"    : "https://api.innodatalabs.com/v1/output/yyyy"
})

    def test_predict_from_datavault(self):
        api = ilabs_api.ILabsApi(user_key=_DUMMY_USER_KEY)
        api._request = mock.Mock(return_value=b'''\
{
    "task_id"            : "test-task-id",
    "task_cancel_url"    : "https://api.innodatalabs.com/v1/cancel/xxx",
    "task_status_url"    : "https://api.innodatalabs.com/v1/status/xxx",
    "document_output_url": "https://api.innodatalabs.com/datavault/test-collection/123456.bin/prediction",
    "output_filename"    : "123456.bin"
}
''')
        rc = api.predict_from_datavault(domain='test-domain',
            collection='test-collection', filename='123456.bin')

        api._request.assert_called_once_with(
            'POST',
            'https://api.innodatalabs.com/v1/prediction/test-domain/test-collection/123456.bin',
            b'',
            query={'input_facet': 'master', 'output_facet': 'prediction'},
            content_type=None
        )

    def test_status(self):
        api = ilabs_api.ILabsApi(user_key=_DUMMY_USER_KEY)
        api._request = mock.Mock(return_value=b'{ "completed": false }')

        rc = api.status('test-domain', 'test-job-id')
        api._request.assert_called_once_with(
            'GET',
            'https://api.innodatalabs.com/v1/reference/test-domain/test-job-id/status',
            query=None)

        self.assertEqual(rc, {'completed': False})

    def test_cancel(self):
        api = ilabs_api.ILabsApi(user_key=_DUMMY_USER_KEY)
        api._request = mock.Mock(return_value=b'[]')

        rc = api.cancel('test-domain', 'test-job-id')
        api._request.assert_called_once_with(
            'GET',
            'https://api.innodatalabs.com/v1/reference/test-domain/test-job-id/cancel',
            query=None)

        self.assertEqual(rc, [])

    def test_feedback(self):
        api = ilabs_api.ILabsApi(user_key=_DUMMY_USER_KEY)
        api._request = mock.Mock(return_value=b'{ "bytes_accepted": 8 }')

        rc = api.upload_feedback('test-domain', '000-123.xml', b'contents')
        api._request.assert_called_once_with(
            'POST',
            'https://api.innodatalabs.com/v1/documents/training/test-domain/000-123.xml',
            b'contents',
            content_type='application/octet-stream', query=None)

        self.assertEqual(rc, {"bytes_accepted": 8})

if __name__ == '__main__':
    unittest.main()
