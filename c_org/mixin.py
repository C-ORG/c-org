#!/usr/bin/python3
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

''' Mixins for Continuous Organisation '''

import os
import yaml
from c_org.utils import Wallet


class KeysMixin(object):
    ''' Manage the file .c-org/keys.yaml containing informations on the wallets and other securities keys '''




    @property
    def keys(self):
        path = os.environ.get('C_ORG_PATH', os.getcwd())
        if not hasattr(self, '_keys'):
            filename = os.path.join(path, '.c-org', 'keys.yaml')
            with open(filename, 'r+') as f:
                self._keys = yaml.load(f)
        return self._keys

    def wallet_exists(self, name):
        names = [w.get('name') for w in self.keys.get('wallets')]
        return name in names

    def add_wallet(self, wallet):
        if isinstance(wallet, dict):
            wallet = Wallet.from_dict(wallet)
        self.keys['wallets'].append(vars(wallet))
        self.save()

    def remove_wallet(self, name):
        for wallet in self.keys.get('wallets'):
            if wallet.get('name') == name:
                self.keys.get('wallets').remove(wallet)
        self.save()
        return

    def save(self):
        path = os.environ.get('C_ORG_PATH', os.getcwd())
        filename = os.path.join(path, '.c-org', 'keys.yaml')
        with open(filename, 'w+') as f:
            yaml.dump(self.keys, f)
