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

'''c_org configuration manager'''

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
from c_org.manager import ContractManager


class ContinuousOrganisationManager(ContractManager):

    def param_constructor(self):
        slope =  int(self.config.get('slope')*1000);
        alpha = int(self.config.get('investor_reserve')*1000);
        beta = int(self.config.get('revenue_reserve')*1000);
        return [slope, alpha, beta]

    def burn(self, tokens, sender):
        tx_hash = self.contract.functions.burning(int(tokens)).transact({
            'from': sender,
            'gas': 100000})
        tx_receipt = w3.eth.getTransactionReceipt(tx_hash)['contractAddress']
        return tx_receipt

    def mint(self, amount, sender):
        wei = Web3.toWei(amount, 'ether')
        tx_hash = self.contract.functions.minting().transact({
            'from': sender,
            'gas': 100000,
            'value': wei})
        tx_receipt = w3.eth.getTransactionReceipt(tx_hash)['contractAddress']
        return tx_receipt

    def revenue(self, amount):
        wei = Web3.toWei(amount, 'ether')
        sender = w3.eth.accounts[0]
        tx_hash = self.contract.functions.revenue().transact({
            'from': sender,
            'gas': 100000,
            'value': wei})
        tx_receipt = w3.eth.getTransactionReceipt(tx_hash)['contractAddress']
        return tx_receipt


    def free_tokens(self, tokens):
        sender = w3.eth.accounts[0]
        tx_hash = self.contract.functions.freeTokens(tokens).transact({
            'from': sender,
            'gas': 100000})
        tx_receipt = w3.eth.getTransactionReceipt(tx_hash)['contractAddress']
        return tx_receipt

    def get_balance(self, sender):
        return self.contract.functions.getBalance().call({'from': sender})

    def get_n_tokens(self):
        return self.contract.functions.getNumTokens().call()

    def get_sell_reserve(self):
        return self.contract.functions.getSellReserve().call()
