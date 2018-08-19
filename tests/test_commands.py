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
from web3 import Web3
from web3.auto import w3
import c_org
from .test_base import TestBase
from c_org.cli import main
from c_org.c_org_manager import ContinuousOrganisationManager

class TestDerive(TestBase):

    def setUp(self):
        self.temp_files()

    def tearDown(self):
        self.cleanup()

    def test_derive(self):
        sys.argv = [sys.argv[0]] + ["derive", "--name", "test"]
        main()
        file_exists = os.path.isfile(os.path.join(self.workdir.name, "builds", "test.build.pkl"))
        self.assertEqual(file_exists, True)
        self.c_org_manager = ContinuousOrganisationManager('test')
        contract = self.c_org_manager.load()
        self.assertNotEqual([], contract.all_functions())



class TestCommands(TestBase):

    def setUp(self):
        self.temp_files()
        self.account = w3.eth.accounts[1]
        # create a smart contract
        sys.argv = [sys.argv[0]] + ["derive", "--name", "test"]
        main()


    def tearDown(self):
        self.cleanup()


    def test_buy(self):
        sys.argv = [sys.argv[0]] + ["buy", "--name", "test", "--account", self.account, "--amount", "10"]
        main()

    def test_sell(self):
        # buy 10
        self.c_org_manager = ContinuousOrganisationManager('test')
        contract = self.c_org_manager.load()
        self.c_org_manager.mint(10, self.account)
        # sell 10
        sys.argv = [sys.argv[0]] + ["sell", "--name", "test", "--account", self.account, "--amount", "1"]
        main()

    # def test_revenue(self):
    #     sys.argv = [sys.argv[0]] + ["revenue", "--name", "test", "--revenue", "10"]
    #     main()

    def test_stats(self):
        sys.argv = [sys.argv[0]] + ["stats", "--name", "test"]
        main()




#if __name__ == '__main__':
#    unittest.main()
