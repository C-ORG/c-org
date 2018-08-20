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
import c_org.utils as utils
from .test_base import TestBase
import pickle

class TestUtils(TestBase):
    '''Utils tests'''

    def setUp(self):
        self.temp_files()

    def test_clean_name(self):
        a = "2f vbr Ffrg"
        self.assertEqual(utils.clean_name(a), "2fvbrffrg")

    def test_restricted_unpickle_legal(self):
        a = {"abi": "foo", "address": "bar"}
        self.workdir = tempfile.TemporaryDirectory()
        legal = os.path.join(self.workdir.name, "legal.pkl")
        with open(legal, 'wb+') as f:
            pickle.dump(a, f)
        c = utils.restricted_unpickle(legal)
        self.assertEqual(c, a)
        self.workdir.cleanup()

    @unittest.expectedFailure
    def test_restricted_unpickle_illegal(self):
        b = set(1, 2, 5)
        self.workdir = tempfile.TemporaryDirectory()
        illegal = os.path.join(self.workdir.name, "illegal.pkl")
        with open(illegal, 'wb+') as f:
            pickle.dump(b, f)
        utils.restricted_unpickle(illegal)
        self.workdir.cleanup()


if __name__ == '__main__':
    unittest.main()
