import unittest
import mock

from ilabs.client import ilabs_api, ilabs_datavault_api
from ilabs.client import ilabs_datavault_predictor

_DUMMY_USER_KEY = '0123456789'
_DUMMY_DATAVAULT_TOKEN = 'JWT0123456789'

class TestIlabsDatavaultPredictor(unittest.TestCase):

    def test_prediction(self):


        predictor = ilabs_datavault_predictor.ILabsDatavaultPredictor.init(
            domain='foo-domain',
            collection='test-collection',
            user_key=_DUMMY_USER_KEY,
            datavault_key=_DUMMY_DATAVAULT_TOKEN
        )
        predictor.api._request = mock.Mock(side_effect=[
            b'{ "task_id": "task-0", "task_cancel_url": "cancel", "document_output_url": "do", "task_status_url": "ts", "output_filename": "of"}',
            b'{ "completed": false, "progress": 1, "steps": 5 }',
            b'{ "completed": true, "progress": 5, "steps": 5 }',
        ])
        predictor._datavault._request = mock.Mock(side_effect=[
            b'',
            b'prediction'
        ])

        progress=mock.Mock()
        rc = predictor(b'hello', name='test.json', progress=progress)
        self.assertEqual(predictor.api._request.call_count, 3)
        self.assertEqual(predictor._datavault._request.call_count, 2)
        self.assertEqual(rc, b'prediction')
        self.assertEqual(progress.call_count, 10)
        progress.assert_has_calls([
            mock.call('uploading 5 bytes'),
            mock.call('uploaded'),
            mock.call('job submitted, taks id: task-0'),
            mock.call('retrying in: 1'),
            mock.call('progress: 1/5'),
            mock.call('retrying in: 2'),
            mock.call('retrying in: 1'),
            mock.call('progress: 5/5'),
            mock.call('fetching result'),
            mock.call('downloaded 10 bytes')
        ])

    def test_feedback(self):
        api = ilabs_api.ILabsApi(_DUMMY_USER_KEY)
        datavault_api = ilabs_datavault_api.ILabsDatavaultApi(_DUMMY_USER_KEY, _DUMMY_DATAVAULT_TOKEN)

        predictor = ilabs_datavault_predictor.ILabsDatavaultPredictor.init(
            domain='foo-domain',
            collection='test-collection',
            user_key=_DUMMY_USER_KEY,
            datavault_key=_DUMMY_DATAVAULT_TOKEN
        )

        predictor._datavault._request = mock.Mock()
        predictor.upload(b'some contents', 'test.json', facet='feedback')
        predictor._datavault._request.assert_called_once_with(
            'POST', 'https://api.innodatalabs.com/datavault/test-collection/test.json/feedback',
            b'some contents',
            content_type='application/octet-stream',
            query=None
        )
