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

'''c_org buy command line'''

import logging

from c_org.cli.command import COrgCommand
from c_org import ContinuousOrganisationManager
from c_org.manager import Vault

class COrgBuy(COrgCommand):

    def __init__(self):
        super().__init__(command_id='buy', leaf=True,
                         description='Buy tokens')
        self.subcommand = True


    def run(self):
        self.parser.add_argument('--wallet',
                                 help='Name of the sender\'s wallet',
                                 type=str)
        self.parser.add_argument('--amount',
                                 help='Amount to send',
                                 type=float)
        self.parser.add_argument('name',
                                 help='Continuous Organisation\'s name',
                                 type=str,
                                 metavar="name")
        self.func = self.command_buy
        self.parse_args()
        self.run_command()

    def command_buy(self):
        vault = Vault()
        try:
            wallet = vault.find_wallet(name=self.wallet)
        except ValueError:
            return logging.error('The wallet is not recognized. Add a wallet with the wallet command.')

        c_org_manager = ContinuousOrganisationManager(self.name)
        if not c_org_manager.is_built():
            return logging.error('The continuous organisation is not deployed.  Run first `c-org deploy --help`.')

        logging.debug('Buying an amount of {:.3f} to {}'.
                       format(self.amount, self.name))
        c_org_manager.buy(self.amount, wallet)
