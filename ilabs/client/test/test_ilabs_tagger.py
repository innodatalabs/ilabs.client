import unittest
import mock
from ilabs.client import ilabs_predictor, ilabs_tagger
import lxml.etree as et

_DUMMY_USER_KEY = '0123456789'


class TestIlabsTagger(unittest.TestCase):

    def test_prediction(self):
        tagger = ilabs_tagger.ILabsTagger(domain='address', user_key=_DUMMY_USER_KEY)

        prediction = b'''\
<brs:b xmlns:brs="http://innodatalabs.com/brs">
    <brs:r>Hello, <brs:s l="subject">world</brs:s>!</brs:r>
    <brs:r>Bye-bye <brs:s l="subject">girl</brs:s></brs:r>
</brs:b>
'''
        tagger.predictor = mock.Mock(return_value=prediction)

        progress=mock.Mock()
        result = tagger([
            'Hello, world!',
            'Bye-bye girl'
        ], progress=progress)

        self.assertEqual(result, [
            [
                ('Hello, ', None),
                ('world', 'subject'),
                ('!', None)
            ],
            [
                ('Bye-bye ', None),
                ('girl', 'subject')
            ]
        ])
        self.assertEqual(progress.mock_calls, [
            mock.call('created XML file from 2 records')
        ])

    def test_feedback(self):
        tagger = ilabs_tagger.ILabsTagger(domain='address', user_key=_DUMMY_USER_KEY)

        tagger.predictor = mock.Mock()

        annotations = [
            [
                ('Hello, ', None),
                ('world', 'subject'),
                ('!', None)
            ],
            [
                ('Bye-bye ', None),
                ('girl', 'subject')
            ]
        ]

        result = tagger.feedback('my-file-id', annotations)

        expected_xml_text = b'''<?xml version='1.0' encoding='utf-8'?>
<brs:b xmlns:brs="http://innodatalabs.com/brs">
<brs:r>Hello, <brs:s l="subject">world</brs:s>!</brs:r>
<brs:r>Bye-bye <brs:s l="subject">girl</brs:s></brs:r>
</brs:b>'''
        tagger.predictor.feedback.assert_called_with(
            'my-file-id',
            expected_xml_text)

if __name__ == '__main__':
    unittest.main()
