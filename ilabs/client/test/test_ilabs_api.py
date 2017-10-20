import unittest
import mock
from ilabs.client import ilabs_api, __version__


_DUMMY_USER_KEY = '0123456789'


class TestIlabsApi(unittest.TestCase):

    def test_request(self):

        api = ilabs_api.ILabsApi(user_key=_DUMMY_USER_KEY)

        with mock.patch('ilabs.client.ilabs_api.requests') as requests:
            mock_response = mock.Mock()
            mock_response.status_code = 200
            requests.request = mock.Mock(return_value=mock_response)

            api._request('OPTIONS', 'http://www.gogole.com', b'some content',
                content_type='test/test')

            self.assertEqual(requests.request.call_count, 1)
            requests.request.assert_called_with(
                'OPTIONS',
                'http://www.gogole.com',
                data=b'some content',
                headers={
                    b'User-Agent': b'ILabs API client ' + __version__.encode(),
                    b'Content-Type': b'test/test',
                    b'User-Key': b'0123456789',
                    b'Cache-Control': b'no-cache'
                },
                stream=True
            )

    def test_ping(self):

        api = ilabs_api.ILabsApi(user_key=_DUMMY_USER_KEY)
        api._request = mock.Mock(return_value=b'{ "ping": "pong" }')

        rc = api.ping()
        api._request.assert_called_once_with('GET', 'https://api.innodatalabs.com/v1/ping')

        self.assertEqual(rc, {'ping': 'pong'})

    def test_upload_input(self):
        api = ilabs_api.ILabsApi(user_key=_DUMMY_USER_KEY)
        api._request = mock.Mock(return_value=b'{ "bytes_accepted": 5, "input_filename": "123456.bin" }')

        rc = api.upload_input(b'hello')
        api._request.assert_called_once_with(
            'POST',
            'https://api.innodatalabs.com/v1/documents/input/',
            b'hello',
            content_type='application/octet-stream')

        self.assertEqual(rc, {'bytes_accepted': 5, 'input_filename': '123456.bin'})

        rc = api.upload_input(b'hello', filename='XXX')
        api._request.assert_called_with(
            'POST',
            'https://api.innodatalabs.com/v1/documents/input/XXX',
            b'hello',
            content_type='application/octet-stream')

        self.assertEqual(rc, {'bytes_accepted': 5, 'input_filename': '123456.bin'})

    def test_download_input(self):
        api = ilabs_api.ILabsApi(user_key=_DUMMY_USER_KEY)
        api._request = mock.Mock(return_value=b'contents')

        rc = api.download_input('XXX')
        api._request.assert_called_once_with(
            'GET',
            'https://api.innodatalabs.com/v1/documents/input/XXX')

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
            'https://api.innodatalabs.com/v1/reference/test-domain/123456.bin'
        )

        self.assertEqual(rc, {
    "task_id"            : "test-task-id",
    "task_cancel_url"    : "https://api.innodatalabs.com/v1/cancel/xxx",
    "task_status_url"    : "https://api.innodatalabs.com/v1/status/xxx",
    "document_output_url": "https://api.innodatalabs.com/v1/output/123456.bin",
    "output_filename"    : "https://api.innodatalabs.com/v1/output/yyyy"
})

    def test_status(self):
        api = ilabs_api.ILabsApi(user_key=_DUMMY_USER_KEY)
        api._request = mock.Mock(return_value=b'{ "completed": false }')

        rc = api.status('test-domain', 'test-job-id')
        api._request.assert_called_once_with(
            'GET',
            'https://api.innodatalabs.com/v1/reference/test-domain/test-job-id/status')

        self.assertEqual(rc, {'completed': False})

    def test_cancel(self):
        api = ilabs_api.ILabsApi(user_key=_DUMMY_USER_KEY)
        api._request = mock.Mock(return_value=b'[]')

        rc = api.cancel('test-domain', 'test-job-id')
        api._request.assert_called_once_with(
            'GET',
            'https://api.innodatalabs.com/v1/reference/test-domain/test-job-id/cancel')

        self.assertEqual(rc, [])

    def test_feedback(self):
        api = ilabs_api.ILabsApi(user_key=_DUMMY_USER_KEY)
        api._request = mock.Mock(return_value=b'{ "bytes_accepted": 8 }')

        rc = api.upload_feedback('test-domain', '000-123.xml', b'contents')
        api._request.assert_called_once_with(
            'POST',
            'https://api.innodatalabs.com/v1/documents/training/test-domain/000-123.xml',
            b'contents',
            content_type='application/octet-stream')

        self.assertEqual(rc, {"bytes_accepted": 8})

if __name__ == '__main__':
    unittest.main()
