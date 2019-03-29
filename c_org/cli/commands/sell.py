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
'''c_org sell command line'''

import logging
from c_org.cli.command import COrgCommand
from c_org import ContinuousOrganisationManager
from c_org.manager import Vault


class COrgSell(COrgCommand):
    def __init__(self):
        super().__init__(
            command_id='sell', leaf=True, description='Sell tokens')
        self.subcommand = True

    def run(self):
        self.parser.add_argument('--wallet', help='Wallet\'s sender', type=str)
        self.parser.add_argument(
            '--amount', help='Tokens\' amount to send', type=float)
        self.parser.add_argument(
            'name',
            help='Continuous Organisation\'s name',
            type=str,
            metavar="name")
        self.func = self.command_sell
        self.parse_args()
        self.run_command()

    def command_sell(self):
        if not isinstance(self.amount, float) or self.amount < 0:
            return logging.error("Please add a positive amount to sell.")

        vault = Vault()
        try:
            wallet = vault.find_wallet(name=self.wallet)
        except ValueError:
            return logging.error(
                'The wallet is not recognized. Add a wallet with the wallet command.'
            )

        c_org_manager = ContinuousOrganisationManager(self.name)
        if not c_org_manager.is_built():
            return logging.error(
                'The continuous organisation is not deployed.  Run first `c-org deploy --help`.'
            )

        logging.debug('Selling an amount of {:.3f}'.format(self.amount))
        c_org_manager.sell(self.amount, wallet)

        balance = c_org_manager.get_balance(wallet)
        logging.info(
            "Your sell tokens! Your balance is now {:d}".format(balance))
