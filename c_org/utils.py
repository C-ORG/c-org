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
try:
    import cPickle as pickle
except:
    import pickle
import web3
from web3 import Web3
from web3.auto import w3


def clean_name(name):
    return re.sub('\W+','', name.lower())


def get_config_path():
    """ Folder containing the Continuous Organisations' configuration file """
    path = os.environ.get('DERIVE_PATH', os.getcwd())
    return os.path.join(path,'configs')


def get_config_file(name = "", check=True):
    """ File containing a Continuous Organisations' configuration """
    path = os.path.join(get_config_path(), clean_name(name) + ".yaml")
    if check and not os.path.isfile(path):
        raise IOError("The continuous organisation's configuration file {} does not exist".format(path))
    return path


def get_build_path():
    """ Folder containing the Continuous Organisations' configuration file """
    path = os.environ.get('DERIVE_PATH', os.getcwd())
    return os.path.join(path,'builds/')


def get_build_file(name = "", check=True):
    """ File containing the build of a continuous organisation """
    path = os.path.join(get_build_path(), clean_name(name) + ".build.pkl")
    if check and not os.path.isfile(path):
        raise IOError("The continuous organisation's build file {} does not exist".format(path))
    return path

def get_source_path():
    """ Folder containing the Continuous Organisations' configuration file """
    path = os.environ.get('DERIVE_PATH', os.getcwd())
    return os.path.join(path,'contracts/')


def get_source_file(name = "", check=True):
    """ File containing the build of a continuous organisation """
    path = os.path.join(get_source_path(), clean_name(name) + ".sol")
    if check and not os.path.isfile(path):
        raise IOError("The continuous organisation's source {} does not exist".format(path))
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
