#!/usr/bin/python3
#
# This manages a continuous organisation
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

'''c-org manager'''

import logging
import os
import yaml
try:
    import cPickle as pickle
except:
    import pickle
import solc
from web3 import Web3
from web3.auto import w3
import c_org.utils as utils
from c_org.manager import *



class ContinuousOrganisationManager(object):

    def __init__(self, name):
        self.global_params = GlobalParams()
        self.folder = self.global_params.find_by_name(name)
        print(self.folder)
        if not self.folder: # the CO is not recognized
            self.folder = utils.get_default_path(name)
            self.global_params.create_or_update(name, self.folder)
        if not os.path.isdir(self.folder):
            os.makedirs(self.folder)
        if not os.path.isfile(self.param_file):
            logging.debug("Creating the config file of the continuous organisation.")
            open(self.param_file, "a").close()
        self.params = LocalParams(self.param_file)
        self._contract = None
        self._interface = None

    @property
    def param_file(self):
        return os.path.join(self.folder, "config.yaml")

    @property
    def build_file(self):
        return os.path.join(self.folder, "build.yaml")

    @property
    def interface(self):
        if not self._interface:
            try:
                with open(self.build_file, 'r') as f:
                    self._interface = yaml.load(f)
            except FileNotFoundError:
                raise utils.ConfigurationError("The build file does not exist. {}".format(self.build_file))
        return self._interface

    @property
    def contract(self):
        if not self._contract:
            self._contract = w3.eth.contract(abi=self.interface['abi'],
                                             address=self.interface['address'])
        return self._contract

    def is_built(self):
        try:
            self.interface
            return True
        except FileNotFoundError:
            return False

    # DEPLOY
    # --------------------------------------------------------------------------
    def _generate_ui(self):
        pass

    def _compile(self):
        with open(utils.get_source_file(), 'r') as f:
            source_code = f.read()
        compiled_sol = solc.compile_source(source_code)
        return compiled_sol

    def _store_build(self, interface, address):
        store = {'abi': interface['abi'],
                 'address': address}
        with open(self.build_file, 'w+') as f:
            yaml.dump(store, f)
        build_file_js = os.path.join(self.folder, "config.js")
        with open(build_file_js, 'w+') as f:
            f.write('''const address = {};
const abi = {};'''.format(address, str(interface['abi'])))

    def _deploy_contract(self, wallet, contract):
        slope =  int(self.params.get('slope')*1000)
        alpha = int(self.params.get('investor_reserve')*1000)
        beta = int(self.params.get('revenue_reserve')*1000)
        nonce = w3.eth.getTransactionCount(wallet.address)
        transaction = contract.constructor(slope, alpha, beta) \
                              .buildTransaction({'gas': 4712388,
                                                 'gasPrice': 100000,
                                                 'from': wallet.address,
                                                 'nonce': nonce})
        tx_sign = w3.eth.account.signTransaction(transaction,
                                                 private_key=wallet.private_key)
        tx_hash = w3.eth.sendRawTransaction(tx_sign.rawTransaction)
        address = w3.eth.getTransactionReceipt(tx_hash)['contractAddress']
        return address

    def deploy(self, wallet):
        ''' Deploy a Continuous Organisation '''
        compiled_sol = self._compile()
        id, interface = compiled_sol.popitem()
        contract = w3.eth.contract(abi=interface['abi'],
                                   bytecode=interface['bin'])
        address = self._deploy_contract(wallet, contract)
        self._store_build(interface, address)
        self._generate_ui()



    # SELL
    # --------------------------------------------------------------------------
    def sell(self, tokens, wallet):
        tokens = int(tokens) #FIXME what is a wei for our tokens?
        nonce = w3.eth.getTransactionCount(wallet.address)
        transaction = self.contract.functions.sell(tokens).buildTransaction({
                        'gas': 4712388,
                        'gasPrice': 100000,
                        'from': wallet.address,
                        'nonce': nonce})
        tx_sign = w3.eth.account.signTransaction(transaction,
                                                 private_key=wallet.private_key)
        tx_hash = w3.eth.sendRawTransaction(tx_sign.rawTransaction)
        tx_receipt = w3.eth.getTransactionReceipt(tx_hash)['contractAddress']
        return tx_receipt

    # BUY
    # --------------------------------------------------------------------------
    def buy(self, amount, wallet):
        wei = Web3.toWei(amount, 'ether')
        nonce = w3.eth.getTransactionCount(wallet.address)
        transaction = self.contract.functions.buy().buildTransaction({
                        'from': wallet.address,
                        'gas': 4712388,
                        'gasPrice': 100000,
                        'nonce': nonce,
                        'value': wei})
        tx_sign = w3.eth.account.signTransaction(transaction,
                                                 private_key=wallet.private_key)
        tx_hash = w3.eth.sendRawTransaction(tx_sign.rawTransaction)
        tx_receipt = w3.eth.getTransactionReceipt(tx_hash)['contractAddress']
        return tx_receipt

    # REVENUE
    # --------------------------------------------------------------------------
    def revenue(self, amount, wallet):
        wei = Web3.toWei(amount, 'ether')
        nonce = w3.eth.getTransactionCount(wallet.address)
        transaction = self.contract.functions.revenue().buildTransaction({
                        'from': wallet.address,
                        'gas': 4712388,
                        'gasPrice': 100000,
                        'nonce': nonce,
                        'value': wei})
        tx_sign = w3.eth.account.signTransaction(transaction,
                                                 private_key=wallet.private_key)
        tx_hash = w3.eth.sendRawTransaction(tx_sign.rawTransaction)
        tx_receipt = w3.eth.getTransactionReceipt(tx_hash)['contractAddress']
        return tx_receipt

    # FREE TOKENS
    # --------------------------------------------------------------------------
    def free_tokens(self, tokens, wallet):
        nonce = w3.eth.getTransactionCount(wallet.address)
        transaction = self.contract.functions.freeTokens(tokens).buildTransaction({
                        'from': wallet.address,
                        'gas': 4712388,
                        'gasPrice': 100000,
                        'nonce': nonce})
        tx_sign = w3.eth.account.signTransaction(transaction,
                                                 private_key=wallet.private_key)
        tx_hash = w3.eth.sendRawTransaction(tx_sign.rawTransaction)
        tx_receipt = w3.eth.getTransactionReceipt(tx_hash)['contractAddress']
        return tx_receipt

    # STATISTICS
    # --------------------------------------------------------------------------
    def get_balance(self, sender):
        return self.contract.functions.getBalance().call({'from': sender.address})

    def get_n_tokens(self):
        return self.contract.functions.getNumTokens().call()

    def get_sell_reserve(self):
        return self.contract.functions.getSellReserve().call()
