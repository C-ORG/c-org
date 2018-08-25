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
import shutil
import c_org.utils as utils
from c_org import ContinuousOrganisationManager
from c_org.manager import GlobalParams, Vault




class TestBase(unittest.TestCase):

    def generate_wallet(self):
        if not self.has_temporary_files():
            self.temp_files()

        vault = Vault()
        self.wallet = vault.create_wallet('test')
        self.wallet.add_ether(1000000000000000000)

    def temp_files(self):
        self.workdir = tempfile.TemporaryDirectory()
        os.environ['HOME'] = self.workdir.name
        self._temporary = True

    def generate_c_org(self):
        if not self.has_temporary_files():
            self.temp_files()

        rootdir = os.path.dirname(os.path.abspath(__file__))
        c_orgs = utils.get_c_org_path()
        os.makedirs(c_orgs)
        contracts = os.path.join(c_orgs, "contracts")
        os.makedirs(contracts)
        contract = os.path.join(rootdir,
                                "ressources",
                                ".c-org",
                                "contracts",
                                "ContinuousOrganisation.sol")
        shutil.copy(contract, contracts)
        global_file = os.path.join(rootdir,
                                   "ressources",
                                   ".c-org",
                                   "global.yaml")
        shutil.copy(global_file, c_orgs)
        vault_file = os.path.join(rootdir,
                                  "ressources",
                                  ".c-org",
                                  "vault.yaml")
        shutil.copy(vault_file, c_orgs)

    def has_temporary_files(self):
        return hasattr(self, '_temporary') and self._temporary

    def generate_manager(self):
        if not self.has_temporary_files():
            self.temp_files()

        name = "my-co"
        c_name = utils.clean_name(name)
        my_co_path = os.path.join(utils.get_c_org_path(), c_name)
        os.makedirs(my_co_path)
        global_params = GlobalParams()
        global_params.create_or_update(name, my_co_path)
        rootdir = os.path.dirname(os.path.abspath(__file__))
        config_file = os.path.join(rootdir, "ressources", "config.yaml")
        shutil.copy(config_file, my_co_path)
        self.c_org_manager = ContinuousOrganisationManager(name)

    def cleanup(self):
        if self.has_temporary_files():
            self.workdir.cleanup()

    def tearDown(self):
        self.cleanup()
