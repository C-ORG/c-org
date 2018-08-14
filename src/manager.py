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

'''derive configuration manager'''

import logging
import os
import yaml
try:
    import cPickle as pickle
except:
    import pickle
import solc

import derive.utils as utils


class ContinuousOrganisationManager(object):

    def __init__(self, name):
        self.name = name

    def load(self):
        """ Read continuous organisation build file """
        filename = utils.get_build_file(self.name)
        logging.debug("Unpickling build file {}".format(filename))
        with open(filename, 'r') as f:
            c = pickle.load(f)
        self.contract = w3.eth.contract(abi=c['abi'],
                                         address=c['address'])
        return self.contract


    def parse(self):
        filename = utils.get_config_file(self.name)
        logging.debug("Parsing configuration filename {}".format(filename))
        with open(filename, 'r') as f:
            c = yaml.load(filename)
        self.config = c['c-org']
        return self.config

    def build(self):
        store = {'abi': self.interface['abi'], 'address': self.address}
        filename = utils.get_build_file(self.name, check=False)
        with open(filename, 'wb') as f:
            pickle.dump(store, f)

    def compile(self):
        with open(self.config['source'], 'r') as f:
            source_code = f.read()
        compiled_sol = solc.compile_source(source_code)
        self.id, self.interface = compiled_sol.popitem()

    def deploy(self):
        tx_hash = w3.eth.contract(abi=self.interface['abi'],
                                  bytecode=self.interface['bin']).deploy()
        self.address = w3.eth.getTransactionReceipt(tx_hash)['contractAddress']
        return self.address




class ConfigurationError(Exception):
    """
    Configuration could not be parsed or has otherwise failed to apply
    """
    pass
