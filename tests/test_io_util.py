
import io
import os
import tempfile

import pytest_check as check

from unittest.mock import patch, Mock

from cdd_chem.util.io import local_file_from_url


@patch('cdd_chem.util.io.urlopen')
def test_file_from_http_url(urlopen):

    _mock = Mock()
    _mock.read.side_effect = io.BytesIO(b"Hello World")
    urlopen.return_value = _mock

    url = 'http://localhost/hello_world.txt'
    with local_file_from_url(url) as f:
        contents = f.read()
        check.equal(contents, b'Hello World')


def test_file_from_file_url():

    with tempfile.NamedTemporaryFile(delete=False) as f:
        f.write(b'Hello World')
        file_name = f.name
        f.close()

        url = f"file:{file_name}"
        with local_file_from_url(url, mode='rb') as lf:
            check.equal(lf.read(), b'Hello World')

        url2 = f"file://{file_name}"
        with local_file_from_url(url2, mode='rb') as lf:
            check.equal(lf.read(), b'Hello World')

        os.remove(file_name)

def test_file_from_file_path():

    with tempfile.NamedTemporaryFile(delete=False) as f:
        f.write(b'Hello World')
        file_name = f.name
        f.close()

        with local_file_from_url(file_name, mode='rb') as lf:
            check.equal(lf.read(), b'Hello World')

        os.remove(file_name)
