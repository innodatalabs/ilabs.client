import unittest
import mock

from ilabs.client import ilabs_api, ilabs_datavault_api
from ilabs.client import ilabs_datavault_predictor

_DUMMY_USER_KEY = '0123456789'
_DUMMY_DATAVAULT_TOKEN = 'JWT0123456789'

class TestIlabsDatavaultPredictor(unittest.TestCase):

    def test_prediction(self):
        api = ilabs_api.ILabsApi(_DUMMY_USER_KEY)
        api._request = mock.Mock(side_effect=[
            b'{ "task_id": "task-0", "task_cancel_url": "cancel", "document_output_url": "do", "task_status_url": "ts", "output_filename": "of"}',
            b'{ "completed": false, "progress": 1, "steps": 5 }',
            b'{ "completed": true, "progress": 5, "steps": 5 }',
        ])

        datavault_api = ilabs_datavault_api.ILabsDatavaultApi(_DUMMY_USER_KEY, _DUMMY_DATAVAULT_TOKEN)
        datavault_api._request = mock.Mock(side_effect=[
            b'',
            b'prediction'
        ])

        predictor = ilabs_datavault_predictor.ILabsDatavaultPredictor(api, datavault_api, domain='foo-domain')
        progress=mock.Mock()
        rc = predictor(b'hello', 'test-collection', 'test.json', progress=progress)
        self.assertEqual(api._request.call_count, 3)
        self.assertEqual(datavault_api._request.call_count, 2)
        self.assertEqual(rc, b'prediction')
        self.assertEqual(progress.call_count, 10)
        progress.assert_has_calls([
            mock.call('Uploading document test.json in test-collection/master'),
            mock.call('Job submitted, task id: task-0'),
            mock.call('retrying in: 1'),
            mock.call('progress: 1/5'),
            mock.call('retrying in: 2'),
            mock.call('retrying in: 1'),
            mock.call('progress: 5/5'),
            mock.call('Fetching result'),
            mock.call('Downloading document test.json from test-collection/prediction'),
            mock.call('Downloaded 10 bytes')
        ])

    def test_feedback(self):
        api = ilabs_api.ILabsApi(_DUMMY_USER_KEY)
        datavault_api = ilabs_datavault_api.ILabsDatavaultApi(_DUMMY_USER_KEY, _DUMMY_DATAVAULT_TOKEN)
        predictor = ilabs_datavault_predictor.ILabsDatavaultPredictor(api, datavault_api, domain='foo-domain')

        with mock.patch('ilabs.client.ilabs_datavault_api.ILabsDatavaultApi.upload') as upload:
            predictor.upload_feedback(b'some contents', 'test-collection', 'test.json')
            upload.assert_called_once_with(b'some contents', 'test-collection', 'test.json', facet='feedback')
