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

import c_org
from .test_base import TestBase, exe_cli, init_ether
from c_org.cli import main
from c_org import ContinuousOrganisationManager
import c_org.utils as utils
from c_org.manager import Vault

from web3.auto import w3

# from web3.providers.eth_tester import EthereumTesterProvider
# w3 = Web3(EthereumTesterProvider(backend=MockBackend()))


class TestDeploy(TestBase):
    def setUp(self):
        self.generate_c_org()
        self.generate_manager()
        self.generate_wallet()

    def test_deploy(self):
        config_file = os.path.join(self.my_co_path, "config.yaml")
        sys.argv = [
            exe_cli, "deploy", config_file, "--wallet", self.wallet.name
        ]
        main()
        self.assertTrue(os.path.isfile(self.c_org_manager.build_file))
        contract = self.c_org_manager.contract
        self.assertTrue(len(contract.find_functions_by_name('buy')))

    def test_deploy_default_wallet(self):
        Vault().default_wallet().add_ether(init_ether)
        config_file = os.path.join(self.my_co_path, "config.yaml")
        sys.argv = [exe_cli, "deploy", config_file]
        main()
        self.assertTrue(os.path.isfile(self.c_org_manager.build_file))
        contract = self.c_org_manager.contract
        self.assertTrue(len(contract.find_functions_by_name('buy')))

    def test_no_enough_funds(self):
        config_file = os.path.join(self.my_co_path, "config.yaml")
        wallet = Vault().create_wallet('poor-wallet')
        command = [exe_cli, "deploy", config_file, "--wallet", wallet.name]
        p = subprocess.Popen(
            command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        (out, err) = p.communicate()
        self.assertEqual(out, b'')
        self.assertIn(wallet.address.encode('utf-8'), err)


class TestCommandWallet(TestBase):
    def setUp(self):
        self.generate_c_org()
        self.generate_manager()

    def test_add_wallet(self):
        sys.argv = [exe_cli] + [
            "wallet", "add", "test",
            utils.generate_random_private_key()
        ]
        main()
        self.assertTrue(Vault().exist_wallet("test"))

    def test_rm_wallet(self):
        Vault().create_wallet(name="name")
        self.assertTrue(Vault().exist_wallet("name"))
        sys.argv = [exe_cli, "wallet", "remove", "name"]
        main()
        self.assertFalse(Vault().exist_wallet("name"))

    def test_create_wallet(self):
        sys.argv = [exe_cli, "wallet", "create", "my-wallet"]
        main()
        self.assertTrue(Vault().exist_wallet("my-wallet"))

    def test_list_wallet(self):
        Vault().create_wallet(name="test-list")
        with self.assertLogs() as cm:
            sys.argv = [exe_cli, "wallet", "list"]
            main()
        self.assertIn(True, ['test-list' in i for i in cm.output])

    def test_add_ether_wallet(self):
        wallet = Vault().create_wallet(name="test-add-ether")
        sys.argv = [exe_cli, "wallet", "add_ether", "test-add-ether"]
        main()
        self.assertEqual(init_ether, wallet.balance)


class TestOtherCommands(TestBase):
    def setUp(self):
        self.generate_c_org()
        self.generate_manager()
        self.generate_wallet()
        self.c_org_manager.deploy(self.wallet)

    def test_buy(self):
        sys.argv = [exe_cli] + [
            "buy", "my-co", "--wallet", self.wallet.name, "--amount", "0.1"
        ]
        main()

    def test_sell(self):
        self.c_org_manager.buy(0.1, self.wallet)
        sys.argv = [exe_cli] + [
            "sell", "my-co", "--wallet", self.wallet.name, "--amount", "1"
        ]
        main()

    def test_revenue(self):
        sys.argv = [exe_cli] + ["revenue", "my-co", "--revenue", "0.1"]
        main()

    def test_stats(self):
        self.c_org_manager.buy(0.1, self.wallet)
        sys.argv = [exe_cli] + ["stats", "my-co", "--wallet", self.wallet.name]
        main()


if __name__ == '__main__':
    unittest.main()
