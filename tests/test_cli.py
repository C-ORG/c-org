#!/usr/bin/python3
# Blackbox tests of C-ORG.
#
# Copyright (C) 2018 Continuous Organisation
# Author: Pierre-Louis Guhur <pierre-louis.guhur@laposte.net>
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; version 3.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import os
import sys
import unittest
import tempfile
import subprocess
import yaml

from .test_base import TestBase

exe_cli = ["c-org"]

os.environ.update({'PYTHONPATH': '.'})


class TestArgs(TestBase):
    '''Generic argument parsing tests'''

    def setUp(self):
        self.temp_files()

    def test_global_help(self):
        out = subprocess.check_output(exe_cli + ['--help'])
        self.assertIn(b'Available commands', out)
        self.assertIn(b'sell', out)
        self.assertIn(b'--debug', out)

    def test_command_help(self):
        out = subprocess.check_output(exe_cli + ['buy', '--help'])
        self.assertIn(b'--amount', out)

    def test_no_command(self):
        p = subprocess.Popen(exe_cli, stdout=subprocess.PIPE,
                             stderr=subprocess.PIPE)
        (out, err) = p.communicate()
        self.assertEqual(out, b'')
        self.assertIn(b'need to specify a command', err)
        self.assertNotEqual(p.returncode, 0)


if __name__ == '__main__':
    unittest.main()
