"""
check_redis_scalar_info.py monitoring plugin tests
"""

import subprocess

import pytest

from capturer import CaptureOutput
from monitoring_plugins.database.redis import check_redis_scalar_info


REDIS_INFO_MOCK = {
    'foo': 'bar',
    'foobar_int': 4,
    'foobar_float': 4.0,
    'keyspace_hits': 4,
    'keyspace_misses': 1,
}


def test_call_without_args():
    """
    Call monitoring plugin without args
    """

    command = ('PYTHONPATH=$PYTHONPATH:./:./monitoring_plugins '
               '/usr/bin/env python3 '
               './monitoring_plugins/database/redis/check_redis_scalar_info.py'
              )

    try:
        subprocess.check_output(command, shell=True, stderr=subprocess.STDOUT)

    except(subprocess.CalledProcessError) as subprocess_error:
        exp_output = (
            'error: the following arguments are required: --metric-name')
        assert exp_output in subprocess_error.output.decode('utf-8')
        assert subprocess_error.returncode == 2

    else:
        assert 'Must not pas here !'


def test_call_with_connection_error():
    """
    Call monitoring plugin without args
    """

    command = ('PYTHONPATH=$PYTHONPATH:./:./monitoring_plugins '
               '/usr/bin/env python3 '
               './monitoring_plugins/database/redis/check_redis_scalar_info.py'
               ' --host="foobar" --metric-name="foo"'
              )

    try:
        subprocess.check_output(command, shell=True, stderr=subprocess.STDOUT)

    except(subprocess.CalledProcessError) as subprocess_error:
        exp_output = (
            'SCALARINFOVALUE UNKNOWN - Error with Redis server connection')
        assert exp_output in subprocess_error.output.decode('utf-8')
        assert subprocess_error.returncode == 3

    else:
        assert 'Must not pas here !'


@pytest.mark.parametrize(
    'metric_name,database_id,warning,critical,return_code,expected_output', [
        (
            'bar', None, None, None, 3,
            'SCALARINFOVALUE UNKNOWN - "bar": Unknown info metric name'
        ),
        (
            'foo', None, None, None, 3,
            'SCALARINFOVALUE UNKNOWN - "foo" value is not an integer or float:'
        ),
        (
            'foobar_int', 0, '5', '5', 0,
            'SCALARINFOVALUE OK - db0_foobar_int is 4 | db0_foobar_int=4;5;5'
        ),
        (
            'foobar_int', 0, '3', '5', 1,
            (
                'SCALARINFOVALUE WARNING - db0_foobar_int is 4 '
                '(outside range 0:3) | db0_foobar_int=4;3;5'
            )
        ),
        (
            'foobar_int', 2, '2', '3', 2,
            (
                'SCALARINFOVALUE CRITICAL - db2_foobar_int is 4 '
                '(outside range 0:3) | db2_foobar_int=4;2;3'
            )
        ),
        (
            'foobar_float', 3, '5', '5', 0,
            (
                'SCALARINFOVALUE OK - db3_foobar_float is 4 '
                '| db3_foobar_float=4.0;5;5'
            )
        ),
        (
            'foobar_float', 0, '2.0', '5', 1,
            (
                'SCALARINFOVALUE WARNING - db0_foobar_float is 4 '
                '(outside range 0:2.0) | db0_foobar_float=4.0;2.0;5'
            )
        ),
        (
            'foobar_float', 0, '2', '3.0', 2,
            (
                'SCALARINFOVALUE CRITICAL - db0_foobar_float is 4 '
                '(outside range 0:3.0) | db0_foobar_float=4.0;2;3.0'
            )
        ),
        (
            'hit_rate', 0, '@0.9:', '@0.7:', 2,
            (
                'SCALARINFOVALUE CRITICAL - db0_hit_rate is 0.8 '
                '(outside range @0.7:) | db0_hit_rate=0.8;@0.9:;@0.7:'
            )
        ),
    ]
)
def test_call_with_valid_connection(mocker, database_id, metric_name, warning,
                                    critical, return_code, expected_output):
    """
    Call monitoring plugin with args
    """

    def fake_parser():
        """
        Fake argument passer
        """
        parser = mocker.MagicMock()
        parser.critical = critical
        parser.database_id = database_id
        parser.metric_name = metric_name
        parser.warning = warning

        return parser


    # Patch plugin argument parser
    mocker.patch(
        'monitoring_plugins.database.redis.check_redis_scalar_info.parse_args',
        fake_parser)

    class FakeStrictRedis(mocker.MagicMock):
        """
        StrictRedis magicmock class with info() method
        """

        def info(self):
            """
            Return fake redis info data

            :returns: fake info data
            :rtype: dict
            """
            self.foo()

            return REDIS_INFO_MOCK


    # Manage test contexts
    with mocker.patch(
        'temelio_monitoring.resource.database.'
        'redis.scalar_info_value.StrictRedis',
        new_callable=FakeStrictRedis), \
         pytest.raises(SystemExit) as sys_exit, \
         CaptureOutput() as capture:

        check_redis_scalar_info.main()

    assert sys_exit.value.code == return_code
    assert expected_output in capture.get_text()
