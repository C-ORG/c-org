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
from c_org import ContinuousOrganisationManager
from c_org.manager import Vault
import c_org.utils as utils
from .test_base import TestBase



class TestContinuousOrganisationManager(TestBase):

    def setUp(self):
        self.temp_files()
        vault = Vault()
        self.wallet = vault.create_wallet('test')
        self.wallet.add_ether(10000000000000000000)


    def test_local_params(self):
        self.assertIn('slope', self.c_org_manager.params.data)
        self.assertIn('version', self.c_org_manager.params.data)
        self.assertEqual(1000000, self.c_org_manager.params.get('initial_tokens'))
        self.assertNotIn('c-org', self.c_org_manager.params.data)


    def test_generate_ui(self):
        pass

    def test_abi(self):
        self.c_org_manager.deploy(self.wallet)
        abi = self.c_org_manager.interface.get('abi')
        functions = [i['name'] for i in abi if i['type'] == 'function']
        self.assertEqual(len(functions), len(self.c_org_manager.contract.all_functions()))
        self.assertIn('buy', functions)
        self.assertNotIn('UpdateTokens', functions) # this is an event not a function

    def test_deploy(self):
        self.c_org_manager.deploy(self.wallet)
        self.assertIn('abi', self.c_org_manager.interface)
        self.assertIn('address', self.c_org_manager.interface)
        self.assertNotEqual(self.c_org_manager.interface.get('address'), 0x0)

    def test_store_build(self):
        self.c_org_manager.deploy(self.wallet)
        self.assertTrue(os.path.isfile(self.c_org_manager.build_file))
        build_file_js = os.path.join(self.c_org_manager.folder, "config.js")
        self.assertTrue(os.path.isfile(build_file_js))

    def test_buy(self):
        self.c_org_manager.deploy(self.wallet)
        self.c_org_manager.buy(0.1, self.wallet)
        # TODO add test

    def test_sell(self):
        pass
        # TODO add test


if __name__ == '__main__':
    unittest.main()
