#!/usr/bin/python3
# Test ContinuousOrganisationManager
#
# Copyright (C) 2018 Continuous Organisation.
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
import tempfile
import unittest
from c_org.manager import ContinuousOrganisationManager
import c_org.utils as utils
from .test_base import TestBase

rootdir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


class TestContinuousOrganisationManager(TestBase):

    def setUp(self):
        self.temp_files()
        self.c_org_manager = ContinuousOrganisationManager('test')

    def tearDown(self):
        self.cleanup()

    def test_parse(self):
        config = self.c_org_manager.parse()
        self.assertIn('slope', config)
        self.assertIn('version', config)
        self.assertEqual(1000000, config.get('initial_tokens'))
        self.assertNotIn('c-org', config)


    def test_compile(self):
        self.c_org_manager.parse()
        self.c_org_manager.compile()
        abi = self.c_org_manager.interface['abi']
        self.assertEqual('setGreeting', abi[0]['name'])
        self.assertNotIn('_greeting', abi)

    def test_deploy(self):
        self.c_org_manager.parse()
        self.c_org_manager.compile()
        self.c_org_manager.deploy()
        self.assertNotEqual(self.c_org_manager.address, 0x0)

    def test_build(self):
        self.c_org_manager.parse()
        self.c_org_manager.compile()
        self.c_org_manager.deploy()
        self.c_org_manager.build()
        build_file = utils.get_build_file('test')
        self.assertEqual(os.path.isfile(build_file), True)


if __name__ == '__main__':
    unittest.main()
