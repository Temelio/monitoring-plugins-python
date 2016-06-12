#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_monitoring_plugins
----------------------------------

Tests for `monitoring_plugins` module.
"""

import subprocess


def test_main_without_config():
    """
    Test module entry point without configuration
    """

    command = ('PYTHONPATH=$PYTHONPATH:./:./monitoring_plugins '
               '/usr/bin/env python3 '
               './monitoring_plugins/main.py')

    assert subprocess.check_output(command, shell=True) == b''


def test_main_with_config():
    """
    Test module entry point with configuration
    """

    command = ('PYTHONPATH=$PYTHONPATH:./:./monitoring_plugins '
               '/usr/bin/env python3 '
               './monitoring_plugins/main.py foo')

    assert subprocess.check_output(command, shell=True) == b''
