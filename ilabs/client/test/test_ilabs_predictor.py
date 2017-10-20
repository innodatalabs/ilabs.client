import unittest
import mock
from ilabs.client import ilabs_predictor, ilabs_api


_DUMMY_USER_KEY = '0123456789'


class TestIlabsPredictor(unittest.TestCase):

    def test_prediction(self):
        api = ilabs_api.ILabsApi(user_key=_DUMMY_USER_KEY)
        api._request = mock.Mock(side_effect=[
            b'{ "bytes_accepted": 5, "input_filename": "123456.bin" }',
            b'{ "task_id": "task-0", "task_cancel_url": "https://api.innodatalabs.com/v1/cancel/task-0", "document_output_url": "do", "task_status_url": "ts", "output_filename": "of"}',
            b'{ "completed": false, "progress": 0, "steps": 5 }',
            b'{ "completed": true, "progress": 5, "steps": 5 }',
            b'prediction content',
        ])
        predictor = ilabs_predictor.ILabsPredictor(api, domain='foo-domain')

        progress=mock.Mock()
        rc = predictor(b'hello', progress=progress)
        self.assertEqual(api._request.call_count, 5)
        self.assertEqual(rc, b'prediction content')
        self.assertEqual(progress.call_count, 10)
        progress.assert_has_calls([
            mock.call('uploading 5 bytes'),
            mock.call('uploaded, accepted size=5'),
            mock.call('job submitted, taks id: task-0'),
            mock.call('retrying in: 1'),
            mock.call('progress: 0/5'),
            mock.call('retrying in: 2'),
            mock.call('retrying in: 1'),
            mock.call('progress: 5/5'),
            mock.call('fetching result'),
            mock.call('downloaded 18 bytes')
        ])

    def test_feedback(self):
        predictor = ilabs_predictor.ILabsPredictor.init(
            domain='foo-domain', user_key=_DUMMY_USER_KEY)

        with mock.patch('ilabs.client.ilabs_api.ILabsApi.upload_feedback') as feedback:
            predictor.upload_feedback('my-batch-id', b'some contents')

            feedback.assert_called_once_with('foo-domain', 'my-batch-id', b'some contents')


if __name__ == '__main__':
    unittest.main()
