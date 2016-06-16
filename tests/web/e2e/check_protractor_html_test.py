"""
check_protractor_html monitoring plugin tests
"""

import subprocess

import pytest
import requests_mock

from capturer import CaptureOutput
from monitoring_plugins.web.e2e import check_protractor_html


def test_call_without_args():
    """
    Call monitoring plugin without args
    """

    command = ('PYTHONPATH=$PYTHONPATH:./:./monitoring_plugins '
               '/usr/bin/env python3 '
               './monitoring_plugins/web/e2e/check_protractor_html.py')

    try:
        subprocess.check_output(command, shell=True, stderr=subprocess.STDOUT)

    except(subprocess.CalledProcessError) as subprocess_error:
        exp_output = 'error: the following arguments are required: --url'
        assert exp_output in subprocess_error.output.decode('utf-8')
        assert subprocess_error.returncode == 2

    else:
        assert 'Must not pas here !'


@pytest.mark.parametrize('url,response,return_code,exp_output', [
    ('foobar', '{}', 3, 'GETVALUEBYJSONPATH UNKNOWN: '),
    (
        'http://foo.bar',
        '{}',
        0,
        ("GETVALUEBYJSONPATH OK - Failed tests: 0 ([]) | failed_exp=0;;@1: "
         "failed_tests=0;;@1: total_exp=0 total_tests=0")
    ),
    (
        'http://foo.bar',
        '[{"id":"foobar","failedExpectations": [ {"passed": 1}]}]',
        2,
        ("GETVALUEBYJSONPATH CRITICAL - Failed tests: 1 (['foobar']) "
         "(outside range @1:) | failed_exp=1;;@1: failed_tests=1;;@1: "
         "total_exp=1 total_tests=1")
    ),
])
def test_call_with_url(mocker, url, response, return_code, exp_output):
    """
    Call monitoring plugin with args
    """

    def fake_parser():
        """
        Fake argument passer
        """
        parser = mocker.MagicMock()
        parser.url = 'http://foo.bar'

        return parser


    # Patch plugin argument parser
    mocker.patch('monitoring_plugins.web.e2e.check_protractor_html.parse_args',
                 fake_parser)

    # Manage test contexts
    with requests_mock.mock() as mock, \
         pytest.raises(SystemExit) as sys_exit, \
         CaptureOutput() as capture:

        mock.get(url, text=response)
        check_protractor_html.main()

    assert sys_exit.value.code == return_code
    assert exp_output in capture.get_text()
