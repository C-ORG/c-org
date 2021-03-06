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
'''storing a revenue'''

import logging
import os
import sys
from c_org import ContinuousOrganisationManager
from c_org.cli.command import COrgCommand
from c_org.manager import Vault


class COrgRevenue(COrgCommand):
    def __init__(self):
        super().__init__(
            command_id='revenue',
            leaf=True,
            description='Provide some statistics')
        self.subcommand = True

    def run(self):
        self.parser.add_argument(
            '--revenue', help='Revenue to register', type=float)
        self.parser.add_argument(
            'name',
            help='Continuous Organisation\'s name',
            type=str,
            metavar="name")
        self.func = self.command_revenue
        self.parse_args()
        self.run_command()

    def command_revenue(self):
        return logging.error("Not yet implemented")

        logging.debug('Recording a revenue of {:.3f}'.format(self.revenue))
        c_org_manager.revenue(self.revenue)
