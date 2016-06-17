"""
check_nginx_stub_status monitoring plugin tests
"""

import subprocess

import pytest
import requests_mock

from capturer import CaptureOutput
from monitoring_plugins.webserver.nginx import check_nginx_stub_status


def test_call_without_args():
    """
    Call monitoring plugin without args
    """

    command = ('PYTHONPATH=$PYTHONPATH:./:./monitoring_plugins '
               '/usr/bin/env python3 '
               './monitoring_plugins/webserver/nginx/'
               'check_nginx_stub_status.py')

    try:
        subprocess.check_output(command, shell=True, stderr=subprocess.STDOUT)

    except(subprocess.CalledProcessError) as subprocess_error:
        exp_output = 'error: the following arguments are required: --url'
        assert exp_output in subprocess_error.output.decode('utf-8')
        assert subprocess_error.returncode == 2

    else:
        assert 'Must not pas here !'


@pytest.mark.parametrize('script_args,exp_code,exp_output', [
    # Bad URL test
    (['--url=foobar'], 3, 'UNKNOWN - Invalid URL '),

    # OK check with default params test
    (['--url=http://foo.bar'], 0, 'OK - '),

    # Perfdata test
    (
        ['--url=http://foo.bar'],
        0,
        ('| active_connections=300;500;1000;0 active_reading=290;;;0 '
         'active_waiting=6;500;1000;0 active_writing=4;;;0 '
         'total_accept=390;;;0 total_connections=390;;;0 '
         'total_handled=390;;;0'),
    ),

    # OK check with user params test
    (
        [
            '--url=http://foo.bar',
            '--warn-active-connection=350',
            '--crit-active-connection=450',
            '--warn-waiting-connection=350',
            '--crit-waiting-connection=450'
        ],
        0,
        'OK - '
    ),

    # Check active connection warning result
    (
        [
            '--url=http://foo.bar',
            '--warn-active-connection=200',
            '--crit-active-connection=350',
            '--warn-waiting-connection=350',
            '--crit-waiting-connection=450'
        ],
        1,
        'WARNING - Active connections: 300 (outside range 0:200)'
    ),

    # Check active connection critical result
    (
        [
            '--url=http://foo.bar',
            '--warn-active-connection=200',
            '--crit-active-connection=250',
            '--warn-waiting-connection=350',
            '--crit-waiting-connection=450'
        ],
        2,
        'CRITICAL - Active connections: 300 (outside range 0:250)'
    ),

    # Check waiting active connection warning result
    (
        [
            '--url=http://foo.bar',
            '--warn-active-connection=400',
            '--crit-active-connection=450',
            '--warn-waiting-connection=3',
            '--crit-waiting-connection=10'
        ],
        1,
        'WARNING - Active waiting: 6 (outside range 0:3)'
    ),

    # Check waiting active connection critical result
    (
        [
            '--url=http://foo.bar',
            '--warn-active-connection=400',
            '--crit-active-connection=450',
            '--warn-waiting-connection=3',
            '--crit-waiting-connection=5'
        ],
        2,
        'CRITICAL - Active waiting: 6 (outside range 0:5)'
    ),
])
def test_call_with_params(mocker, script_args, exp_code, exp_output):
    """
    Call monitoring plugin with args
    """
    fake_args = ['check_nginx_stub_status.py'] + script_args

    request_mock_response = """
        Active connections: 300
        server accepts handled requests
         390  390  390
         Reading: 290 Writing: 4 Waiting: 6"""

    def fake_getitem(index):
        """
        Fake lambda to return needed arguments for tests
        """
        return fake_args[index]


    # Mock arguments list used with monitoring script parser
    sys_argv = mocker.MagicMock()
    sys_argv.__getitem__.side_effect = fake_getitem

    # Execute monitoring script main function
    with requests_mock.mock() as mock, \
         pytest.raises(SystemExit) as sys_exit, \
         CaptureOutput() as capture, \
         mocker.patch('sys.argv', sys_argv):

        mock.get('http://foo.bar', text=request_mock_response)
        check_nginx_stub_status.main()

    # Check returns
    assert exp_output in capture.get_text()
    assert sys_exit.value.code == exp_code
