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

'''derive command line'''

import logging
import os
import argparse
import derive.utils as utils



class DeriveCommand(argparse.Namespace):

    def __init__(self, command_id, description, testing=False):
        self.command_id = command_id
        self.description = description
        self.testing = testing
        self._args = None
        self.debug = False
        self.subcommands = {}
        self.subcommand = None
        self.func = None
        self._c_org_manager = None

        self.parser = argparse.ArgumentParser(prog="%s %s" % (sys.argv[0], command_id),
                                              description=description,
                                              add_help=True)
        self.parser.add_argument('--debug', action='store_true',
                                 help='Enable debug messages')

    # @property()
    # def c_org_manager(self):  # pragma: nocover (called by later commands)
    #     if not self._c_org_manager:
    #         self._c_org_manager = ContinuousOrganisationManager()
    #     return self._c_org_manager

    def update(self, args):
        self._args = args

    def parse_args(self):
        ns, self._args = self.parser.parse_known_args(args=self._args, namespace=self)

        if not self.subcommand:
            print('You need to specify a command', file=sys.stderr)
            self.print_usage()


    def print_usage(self):
        self.parser.print_help(file=sys.stderr)
        sys.exit(os.EX_USAGE)

    def load_c_org(self):
        """ Read continuous organisation build file """
        filename = utils.get_build_file(self.c_org)
        unpickle = utils.restricted_unpickle()
        self.address = unpickle['address']
        self.abi = unpickle['abi']
        self.contact = w3.eth.contract(address=self.address,
                                       abi=self.abi)


    def _import_subcommands(self, submodules):
        import inspect
        for name, obj in inspect.getmembers(submodules):
            if inspect.isclass(obj) and issubclass(obj, DeriveCommand):
                self._add_subparser_from_class(name, obj)
