#!/usr/bin/python3
# Unit tests for keys mixin.
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
from c_org.mixin import KeysMixin
from .test_base import TestBase


class TestKeysMixin(KeysMixin, TestBase):
    '''Keys mixin tests'''

    def setUp(self):
        self.temp_files()

    def test_keys(self):
        self.assertIn('infura', self.keys)
        self.assertIn('wallets', self.keys)
        names = [w.get('name') for w in self.keys.get('wallets')]
        self.assertIn('my-wallet', names)

    def test_save(self):
        self.keys['infura'] = "TEST"
        self.save()
        del self._keys
        self.assertEqual(self.keys['infura'], "TEST")

    def test_exist(self):
        self.assertTrue(self.wallet_exists('my-wallet'))

    def test_add_dict(self):
        self.assertFalse(self.wallet_exists('dict-wallet'))
        wallet = {'name': "dict-wallet",
                  'private_key': '0123456789ABCDEF0123456789ABCDEF0123456789ABCDEF0123456789ABCDEF'}
        self.add_wallet(wallet)
        self.assertTrue(self.wallet_exists('dict-wallet'))

    def test_add_wallet(self):
        self.assertFalse(self.wallet_exists('wallet-wallet'))
        wallet = utils.Wallet(name="wallet-wallet",
                              private_key='0123456789ABCDEF0123456789ABCDEF0123456789ABCDEF0123456789ABCDEF')
        self.add_wallet(wallet)
        self.assertTrue(self.wallet_exists('wallet-wallet'))

    def test_remove_wallet(self):
        self.assertTrue(self.wallet_exists('my-wallet'))
        self.remove_wallet('my-wallet')
        self.assertFalse(self.wallet_exists('my-wallet'))



if __name__ == '__main__':
    unittest.main()
