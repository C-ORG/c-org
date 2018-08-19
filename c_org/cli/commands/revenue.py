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

'''derive migrate command line'''

import logging
import os
import sys
from web3.auto import w3
from web3 import Web3
from c_org.c_org_manager import ContinuousOrganisationManager
from c_org.cli.command import COrgCommand


class COrgRevenue(COrgCommand):

    def __init__(self):
        super().__init__(command_id='revenue',  leaf=True,
                         description='Provide some statistics')
        self.subcommand = True



    def run(self):
        self.parser.add_argument('--revenue',
                                 help='Revenue to register',
                                 type=float)
        self.parser.add_argument('--name',
                                 help='Continuous Organisation\'s name',
                                 type=str)

        self.func = self.command_revenue
        self.parse_args()
        self.run_command()

    def command_revenue(self):
        c_org_manager = ContinuousOrganisationManager(self.name)
        self.contract = c_org_manager.load()
        logging.debug('Recording a revenue of {:.3f}'.format(self.revenue))
        c_org_manager.revenue(self.revenue)
