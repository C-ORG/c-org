#!/usr/bin/python3
# Unit tests for vault mixin.
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
from c_org.manager import Vault
from .test_base import TestBase


class TestVault(TestBase):
    '''Vault tests'''

    def setUp(self):
        self.generate_c_org()
        self.generate_wallet()
        self.v = Vault()

    def test_vault(self):
        self.assertIn('infura', self.v.data)
        self.assertIn('wallets', self.v.data)
        self.assertIn('my-wallet', self.v.names)

    def test_save(self):
        self.v.data['infura'] = "TEST"
        self.v.save()
        self.v.data = []
        self.v.load()
        self.assertEqual(self.v.data['infura'], "TEST")

    def test_exist(self):
        self.assertTrue(self.v.exist_wallet('my-wallet'))

    def test_create_wallet(self):
        self.assertFalse(self.v.exist_wallet('New Wallet'))
        self.v.create_wallet('New Wallet')
        self.assertTrue(self.v.exist_wallet('New Wallet'))

    def test_store_wallet_dict(self):
        self.assertFalse(self.v.exist_wallet('dict-wallet'))
        wallet = {
            'name': "dict-wallet",
            'private_key': utils.generate_random_private_key()
        }
        self.v.store_wallet(wallet)
        self.assertTrue(self.v.exist_wallet('dict-wallet'))

    def test_store_wallet(self):
        self.assertFalse(self.v.exist_wallet('wallet-wallet'))
        wallet = utils.Wallet(
            name="wallet-wallet",
            private_key=utils.generate_random_private_key())
        self.v.store_wallet(wallet)
        self.assertTrue(self.v.exist_wallet('wallet-wallet'))

    def test_remove_wallet(self):
        self.assertTrue(self.v.exist_wallet('my-wallet'))
        self.v.remove_wallet('my-wallet')
        self.assertFalse(self.v.exist_wallet('my-wallet'))

    def test_no_wallet(self):
        self.v.data['wallets'] = []
        self.v.save()
        self.assertFalse(self.v.exist_wallet('my-wallet'))


if __name__ == '__main__':
    unittest.main()
