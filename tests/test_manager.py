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
import unittest
from c_org.c_org_manager import ContinuousOrganisationManager
import c_org.utils as utils
from .test_base import TestBase



class TestContinuousOrganisationManager(TestBase):

    def setUp(self):
        self.temp_files()


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
        self.assertEqual('setAlpha', abi[0]['name'])
        self.assertNotIn('slope', abi)

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
        build_file = utils.get_build_file('decusis')
        self.assertEqual(os.path.isfile(build_file), True)

    def test_load(self):
        self.c_org_manager.parse()
        self.c_org_manager.compile()
        self.c_org_manager.deploy()
        self.c_org_manager.build()
        contract = self.c_org_manager.load()
        self.assertNotEqual([], contract.all_functions())
        setter = contract.get_function_by_signature('setAlpha(uint256)')
        self.assertNotEqual(setter, None)
        setter2 = contract.get_function_by_name('setAlpha')
        self.assertNotEqual(setter, None)


if __name__ == '__main__':
    unittest.main()
