import unittest
from unittest import mock
from ilabs.client.get_secret import get_secret
import os
import contextlib

def mock_fs(files={}):

    class MockFile:
        def __init__(self, data):
            self._lines = data.split('\n')
            self._current = 0

        def __enter__(self):
            return self

        def readline(self):
            if self._current >= len(self._lines):
                return ''
            line = self._lines[self._current]
            self._current += 1
            return line + '\n'

        def close(self):
            pass

        def __exit__(self, *av):
            pass

        def __iter__(self):
            return self

        def __next__(self):
            x = self.readline()
            if not x:
                raise StopIteration
            return x

    def mock_open(filename, mode='r', encoding='utf-8'):
        content = files.get(filename)
        if content:
            return MockFile(content)
        raise IOError('File not found')

    return mock_open


class TestGetSecret(unittest.TestCase):

    def test_smoke(self):
        with mock.patch.dict(os.environ, {}):
            with mock.patch(
                'ilabs.client.get_secret.configparser',
                mock.Mock(ConfigParser=mock.Mock(return_value=mock.Mock(
                    get=mock.Mock(return_value=None)
                )))
            ):
                user_key = get_secret().get('ilabs_user_key')

        self.assertIsNone(user_key)

    def test_env(self):

        with mock.patch.dict(os.environ, {'ILABS_USER_KEY': 'blah'}):
            user_key = get_secret().get('ilabs_user_key')

        self.assertEqual(user_key, 'blah')

    def test_file(self):

        config = '''
[default]
ilabs_user_key=foo
'''

        os.environ.pop('ILABS_USER_KEY', None)
        with mock.patch('ilabs.client.get_secret.configparser.open', mock_fs({
            '/etc/ilabs.conf': config
        })):
            with mock.patch.dict(os.environ, {}):
                user_key = get_secret().get('ilabs_user_key')

        self.assertEqual(user_key, 'foo')

    def test_section(self):

        config = '''
[default]
ilabs_user_key=foo
[ilabs]
ilabs_user_key=boo
'''

        os.environ.pop('ILABS_USER_KEY', None)
        with mock.patch('ilabs.client.get_secret.configparser.open', mock_fs({
            '/etc/ilabs.conf': config
        })):
            user_key = get_secret().get('ilabs_user_key')

        self.assertEqual(user_key, 'boo')

    def test_file_precedence(self):

        config1 = '''
[default]
ilabs_user_key=bar
'''

        config2 = '''
[default]
ilabs_user_key=foo
'''
        os.environ.pop('ILABS_USER_KEY', None)
        with mock.patch('ilabs.client.get_secret.configparser.open', mock_fs({
            '/etc/ilabs.conf': config2,
            os.path.expanduser(r'~/.config/ilabs/ilabs.conf'): config1
        })):
            user_key = get_secret().get('ilabs_user_key')

        self.assertEqual(user_key, 'bar')

    def test_datavault_env(self):

        with mock.patch.dict(os.environ, {'ILABS_DATAVAULT_KEY': 'blah'}):
            datavault_key = get_secret().get('ilabs_datavault_key')

        self.assertEqual(datavault_key, 'blah')

    def test_datavault_file(self):

        config = '''
[default]
ilabs_datavault_key=foo
'''
        os.environ.pop('ILABS_DATAVAULT_KEY', None)
        with mock.patch('ilabs.client.get_secret.configparser.open', mock_fs({
            '/etc/ilabs.conf': config
        })):
            datavault_key = get_secret().get('ilabs_datavault_key')

        self.assertEqual(datavault_key, 'foo')


if __name__ == '__main__':
    unittest.main()