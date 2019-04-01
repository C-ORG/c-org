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

import sys
import os
import shutil
import argparse
import re
import random
import web3
from web3.auto import w3
try:
    import cPickle as pickle
except:
    import pickle

rootdir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def clean_name(name):
    return re.sub('\W+', '', name.lower())


def get_c_org_path():
    """ Folder containing the Continuous Organisations' configuration file """
    path = os.path.join(os.path.expanduser("~"), '.c-org/')
    #if not os.path.isdir(path):
    #    os.makedirs(path)
    return path


def get_default_path(name):
    name = clean_name(name)
    return os.path.join(get_c_org_path(), name)


def get_source_file():
    return os.path.join(get_c_org_path(), "contracts",
                        "ContinuousOrganisation.sol")


def get_vault_file():
    return os.path.join(get_c_org_path(), "vault.yaml")


def get_global_params_file():
    return os.path.join(get_c_org_path(), "global.yaml")


hex = "0123456789ABCDEF"


def generate_random_private_key():
    ''' Create a random private key

    >>> key = generate_random_private_key()
    >>> account = web3.eth.Account.privateKeyToAccount(key)
    >>> account != None
    True
    '''
    return ''.join(random.choices(hex, k=64))


class Wallet(object):
    def __init__(self, name="", address="", private_key=""):
        self.private_key = private_key
        if address:
            self.address = address
        else:
            self.address = web3.eth.Account.privateKeyToAccount(
                private_key).address
        self.name = name if name != "" else self.address

    @property
    def balance(self):
        return w3.eth.getBalance(self.address)

    def add_ether(self, amount):
        ''' Add ether to a wallet. This is only for testing purpose. Of course, this does not work on mainnet.

        >>> a = w3.eth.account.create('test')
        >>> w = Wallet('test', a.address, a.privateKey)
        >>> w.add_ether(10)
        >>> w.balance
        10'''
        # sender = w3.eth.accounts[0]
        sender = w3.eth.coinbase
        if amount > w3.eth.getBalance(sender):
            raise ValueError("The sender does not have enough coins.")
        w3.eth.sendTransaction({
            'from': sender,
            'to': self.address,
            'value': amount
        })

    @classmethod
    def from_dict(cls, dict):
        return cls(
            dict.get('name'), dict.get('address'), dict.get('private_key'))

    @staticmethod
    def to_dict(wallet):
        return vars(wallet)

    def __repr__(self):
        return "<class 'Wallet': name={}, address={}, private_key={}>".format(
            self.name, self.address, self.private_key)


class RestrictedUnpickler(pickle.Unpickler):

    safe_builtins = {
        'range',
        'dict',
        'slice',
    }

    def find_class(self, module, name):
        # Only allow safe classes from builtins.
        if module == "builtins" and name in self.safe_builtins:
            return getattr(builtins, name)
        # Forbid everything else.
        raise pickle.UnpicklingError(
            "global '%s.%s' is forbidden" % (module, name))


def restricted_unpickle(filename):
    """Helper function analogous to pickle.load()."""
    with open(filename, 'rb') as f:
        return RestrictedUnpickler(f).load()


class BaseError(Exception):
    """Base class for exceptions in this module."""
    pass


class ConfigurationError(BaseError):
    """
    Configuration could not be parsed or has otherwise failed to apply
    """
    pass


if __name__ == "__main__":
    import doctest
    doctest.testmod()


def check_files():
    c_org = os.path.join(os.path.expanduser("~"), '.c-org/')
    if not os.path.isdir(c_org):
        os.makedirs(c_org)
    contracts = os.path.join(c_org, "contracts")
    if not os.path.isdir(contracts):
        os.makedirs(contracts)
        contract = os.path.join(rootdir, "contracts", "ContinuousOrganisation.sol")
        shutil.copy(contract, contracts)
    vault_file = os.path.join(c_org, "vault.yaml")
    if not os.path.isfile(vault_file):
        with open(vault_file, 'w+') as f:
            f.write('''infura: ~
wallets: []''')
    global_file = os.path.join(c_org, "global.yaml")
    if not os.path.isfile(global_file):
        with open(global_file, 'w+') as f:
            f.write('c-orgs: []')


