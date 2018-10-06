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
'''c_org command line'''

import logging
import os
import sys
import argparse
import c_org.utils as utils


class COrgCommand(argparse.Namespace):
    def __init__(self, command_id, description, testing=False, leaf=False):
        self.command_id = command_id
        self.description = description
        self.testing = testing
        self._args = None
        self.debug = False
        self.subcommands = {}
        self.subcommand = None
        self.func = None
        self._c_org_manager = None
        self.leaf_command = leaf
        self.commandclass = None

        self.parser = argparse.ArgumentParser(
            prog="%s %s" % (sys.argv[0], command_id),
            description=description,
            add_help=True)
        self.parser.add_argument(
            '--debug', action='store_true', help='Enable debug messages')

        if not leaf:
            self.subparsers = self.parser.add_subparsers(
                title='Available commands', metavar='', dest='subcommand')
            p_help = self.subparsers.add_parser(
                'help',
                description='Show this help message',
                help='Show this help message')
            p_help.set_defaults(func=self.print_usage)

    def update(self, args):
        self._args = args

    def parse_args(self):
        ns, self._args = self.parser.parse_known_args(
            args=self._args, namespace=self)

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
        self.contact = w3.eth.contract(address=self.address, abi=self.abi)

    def _add_subparser_from_class(self, name, commandclass):
        instance = commandclass()

        self.subcommands[name] = {}
        self.subcommands[name]['class'] = name
        self.subcommands[name]['instance'] = instance

        if instance.testing:
            if not os.environ.get('ENABLE_TEST_COMMANDS', None):
                return

        p = self.subparsers.add_parser(
            instance.command_id,
            description=instance.description,
            help=instance.description,
            add_help=False)
        p.set_defaults(func=instance.run, commandclass=instance)
        self.subcommands[name]['parser'] = p

    def _import_subcommands(self, submodules):
        import inspect
        for name, obj in inspect.getmembers(submodules):
            if inspect.isclass(obj) and issubclass(obj, COrgCommand):
                self._add_subparser_from_class(name, obj)

    def run_command(self):
        if self.commandclass:
            self.commandclass.update(self._args)

        # TODO: (cyphermox) this is actually testable in tests/cli.py; add it.
        if self.leaf_command and 'help' in self._args:  # pragma: nocover (covered in autopkgtest)
            self.print_usage()

        self.func()
