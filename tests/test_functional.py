#!/usr/bin/python3
# A few walktroughs of the utility
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
from urllib.request import urlretrieve
import re
from tempfile import mkstemp
import shutil
from web3 import Web3
from web3.auto import w3
import c_org
from c_org.cli import main
from c_org import ContinuousOrganisationManager
import c_org.utils as utils
from c_org.manager import Vault
from .test_base import TestBase

exe_cli = "c-org"
init_ether = 2000000000000000000


def sed(pattern, replace, source):
    """ Copy the sed bash function. Details on  https://stackoverflow.com/a/40843600/4986615 """
    fin = open(source, 'r')
    fd, name = mkstemp()
    fout = open(name, 'w')
    for line in fin:
        out = re.sub(pattern, replace, line)
        fout.write(out)
    shutil.move(name, source)


class TestNewIssuer(TestBase):
    def setUp(self):
        # we assume Edith has correctly installed the utility
        self.generate_c_org()
        self.old_path = os.getcwd()
        os.chdir(self.workdir.name)

    def tearDown(self):
        self.cleanup()
        os.chdir(self.old_path)

    def test_new_issuer(self):
        # Edith creates a new folder, jumps on it and downloads the config.yaml given in the repository.
        os.makedirs("my-co")
        os.chdir("my-co")
        urlretrieve(
            "https://raw.githubusercontent.com/C-ORG/c-org/master/config.yaml",
            "config.yaml")

        # Edith edits the config.yaml
        sed("summary: ''", "summary: 'My CO is the best in the world!'",
            "config.yaml")

        # Edith creates a wallet and adds Ether on it
        sys.argv = [exe_cli] + ["wallet", "create", "edith-wallet"]
        main()
        self.assertTrue(Vault().exist_wallet("edith-wallet"))

        # Edith adds some ethers on it
        sys.argv = [exe_cli] + ["wallet", "add_ether", "edith-wallet"]
        main()
        wallet = Vault().find_wallet(name="edith-wallet")
        self.assertEqual(init_ether, wallet.balance)

        # Edith deploys her continuous organisation
        sys.argv = [exe_cli] + [
            "deploy", "config.yaml", "--wallet", wallet.name, "--output",
            os.getcwd()
        ]
        main()
        self.assertTrue(os.path.isfile("build.yaml"))

        # Edith buys and sells some tokens
        sys.argv = [exe_cli] + [
            "buy", "my-co", "--wallet", wallet.name, "--amount", "1"
        ]
        main()
        self.assertTrue(init_ether > wallet.balance)

        sys.argv = [exe_cli] + [
            "sell", "my-co", "--wallet", wallet.name, "--amount", "1"
        ]
        main()


if __name__ == '__main__':
    unittest.main()
