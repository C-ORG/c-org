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

'''c_org stats command line'''

import logging
from web3.auto import w3
from c_org.cli.command import COrgCommand
from c_org.c_org_manager import ContinuousOrganisationManager

class COrgStats(COrgCommand):

    def __init__(self):
        super().__init__(command_id='stats',  leaf=True,
                         description='Provide some statistics')
        self.subcommand = True


    def run(self):
        self.parser.add_argument('--name',
                                 help='Continuous Organisation\'s name',
                                 type=str)
        self.parser.add_argument('--account',
                                 help='Your account\'s address',
                                 type=str)
        self.func = self.command_stats
        self.parse_args()
        self.run_command()

    def command_stats(self):
        c_org_manager = ContinuousOrganisationManager(self.name)
        self.contract = c_org_manager.load()
        logging.debug('Retrieving the statistics')
        balance = c_org_manager.get_balance(self.account)
        logging.info("Balance: {:.3f} tokens".format(balance))
        tokens = c_org_manager.get_n_tokens()
        logging.info("Total tokens: {:.3f} tokens".format(tokens))
        reserve = c_org_manager.get_sell_reserve()
        logging.info("Reserve: {:.3f}".format(reserve))
