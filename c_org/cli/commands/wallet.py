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

'''c_org wallet command line'''

import logging
import os
import sys
from c_org.utils import Wallet
from c_org.cli.command import COrgCommand
from c_org import ContinuousOrganisationManager
from c_org.manager import Vault

class COrgWallet(COrgCommand):

    def __init__(self):
        super().__init__(command_id='wallet', leaf=True,
                         description='Manage a wallet')
        self.subcommand = True

    def run(self):
        subparsers = self.parser.add_subparsers(help="Options to manage wallets")
        parser_create = subparsers.add_parser('create', help='Create a wallet')
        parser_create.add_argument('name',
                                   help='wallet\'s name',
                                   type=str,
                                   metavar="name")
        parser_create.set_defaults(func=self.command_create_wallet)
        parser_add = subparsers.add_parser('add', help='Add a wallet')
        parser_add.add_argument('name',
                                 help='wallet\'s name',
                                 type=str,
                                 metavar="name")
        parser_add.add_argument('private_key',
                                 help='wallet\'s private key',
                                 type=str,
                                 metavar="privateKey")
        parser_add.set_defaults(func=self.command_add_wallet)
        parser_rm = subparsers.add_parser('remove', help='Remove a wallet')
        parser_rm.add_argument('name',
                                   help='wallet\'s name',
                                   type=str,
                                   metavar="name")
        parser_rm.set_defaults(func=self.command_rm_wallet)
        self.parse_args()
        self.run_command()


    def command_add_wallet(self):
        vault = Vault()
        if vault.exist_wallet(name=self.name):
            return logging.error("The wallet's name already exists.")

        if self.name:
            logging.debug("Adding a wallet with name {}.".format(self.name))
        else:
            logging.debug("Adding a wallet with private key")

        wallet = Wallet(name=self.name, private_key=self.private_key)
        vault.store_wallet(wallet)
        logging.info("The wallet is added.")


    def command_create_wallet(self):
        vault = Vault()
        if vault.exist_wallet(name=self.name):
            return logging.error("The wallet's name already exists.")
        logging.debug("Creating a wallet with name {}.".format(self.name))
        vault.create_wallet(wallet)
        logging.info("The wallet is created.")


    def command_rm_wallet(self):
        vault = Vault()
        if not vault.exist_wallet(name=self.name):
            return logging.error("The wallet's name can not be found.")

        logging.debug("Removing a wallet with name {}.".format(self.name))
        vault.remove_wallet(self.name)
        logging.info("The wallet is removed.")
