#!/usr/bin/python3
#
# This manages the vault, in which are stored the wallets, in ~/.c-org/vault.yaml
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

'''c-org vault manager'''

import os
from web3.auto import w3
from c_org.manager.base import BaseManager
from c_org.utils import Wallet, get_c_org_path, get_vault_file



class Vault(BaseManager):
    ''' Manage the YAML file ~/.c-org/vault.yaml containing the wallets and other securities keys '''


    @property
    def filename(self):
        return get_vault_file()

    @property
    def wallets(self):
        return self.get('wallets', default=[])

    @property
    def names(self):
        return [w.get('name') for w in self.wallets]

    def create_wallet(self, name=""):
        '''
        Create a wallet given its name.

        >>> w = Vault().create_wallet("my-wallet")
        >>> Vault().exist_wallet('my-wallet')
        True
        '''
        account = w3.eth.account.create(name)
        if self.exist_wallet(name):
            raise ValueError("The wallet\'s name already exists.")
        wallet = Wallet(name, account.address, account.privateKey)
        w_dict = Wallet.to_dict(wallet)
        self.add(w_dict, 'wallets')
        return wallet

    def store_wallet(self, wallet):
        '''
        Store a wallet given as a dict or a Wallet instance.

        >>> wallet = Vault().create_wallet('test')
        >>> Vault().remove_wallet(wallet.name)
        >>> Vault().store_wallet(wallet)
        >>> Vault().exist_wallet(wallet.name)
        True
        '''
        if isinstance(wallet, Wallet):
            wallet = Wallet.to_dict(wallet)
        if self.exist_wallet(wallet.get('name')):
            raise ValueError("The wallet\'s name already exists.")
        self.add(wallet, 'wallets')

    def find_wallet(self, name="", address="", private_key=""):
        '''
        Find a wallet given its name, its address or its private_key

        >>> w = Vault().create_wallet("safe")
        >>> Vault().find_wallet(name="safe") != None
        True
        '''
        if name:
            for wallet in self.wallets:
                if wallet.get('name') == name:
                    return Wallet.from_dict(wallet)
        if private_key:
            address = web3.eth.Account.privateKeyToAccount(private_key).address
        if address:
            for wallet in self.wallets:
                if wallet.get('address') == address:
                    return Wallet.from_dict(wallet)
        raise ValueError("The wallet was not found")

    def exist_wallet(self, name):
        '''
        Check if a wallet exists in the vault given its name.

        >>> w = Vault().create_wallet('test')
        >>> Vault().exist_wallet('test')
        True
        '''
        return self.exists(name, 'name', 'wallets')

    def remove_wallet(self, name):
        '''
        Remove a wallet given its name.

        >>> v = Vault()
        >>> v.data =  {'wallets': [{'private_key': '', 'address': '', 'name': 'to-remove'}]}
        >>> v.remove_wallet('to-remove')
        >>> v.data
        {'wallets': []}
        '''
        self.remove(name, 'name', 'wallets')




if __name__ == "__main__":
    import doctest
    import tempfile
    private_key = "0xb25c7db31feed9122727bf0939dc769a96564b2de4c4726d035b36ecf1e5b364"
    workdir = tempfile.TemporaryDirectory()
    os.makedirs(os.path.join(workdir.name, ".c-org"))
    filename = os.path.join(workdir.name, ".c-org", "vault.yaml")
    with open(filename, "w+") as f:
        f.write('''infura: ~
wallets: []''')
    os.environ['HOME'] = workdir.name
    v = Vault()
    # v.data = {'wallets':[]}
    doctest.testmod(extraglobs={'v': v,
                                'wallet': Wallet(name="safe",
                                                 private_key=private_key)})
    workdir.cleanup()
