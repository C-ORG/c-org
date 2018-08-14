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
import argparse
import re

import web3
from web3 import Web3
import web3.auto import w3


def clean_name(name):
    return re.sub('\W+','', name.lower())


def get_config_path():
    """ Folder containing the Continuous Organisations' configuration file """
    return os.environ.get('DERIVE_CONFIG_PATH', os.getcwd() + '../c-orgs/')


def get_config_file(name = "", check=True):
    """ File containing a Continuous Organisations' configuration """
    path = get_build_path() + clean_name(name) + ".yaml"
    if check and not os.path.isfile(path):
        raise IOError("The continuous orginisation's configuration file does not exist")
    return path


def get_build_path():
    """ Folder containing the Continuous Organisations' configuration file """
    return os.environ.get('DERIVE_BUILD_PATH', os.getcwd()+'../build/')


def get_build_file(name = "", check=True):
    """ File containing the build of a continuous organisation """
    path = get_build_path() + clean_name + ".build.pkl"
    if check and not os.path.isfile(path):
        raise IOError("The continuous orginisation's build file does not exist")
    return path



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
        raise pickle.UnpicklingError("global '%s.%s' is forbidden" %
                                     (module, name))

def restricted_unpickle(filename):
    """Helper function analogous to pickle.load()."""
    with open(fileName, 'rb') as f:
        return RestrictedUnpickler(io.BytesIO(f)).load()
