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
from c_org.cli.command import COrgCommand
from c_org import ContinuousOrganisationManager
import c_org.utils as utils
from c_org.manager import GlobalParams


class COrgInit(COrgCommand):
    def __init__(self):
        super().__init__(
            command_id='init',
            leaf=True,
            description='Initialize a Continuous Organisation')
        self.subcommand = True

    def run(self):
        self.parser.add_argument(
            'name',
            help='Continuous Organisation\'s name',
            type=str,
            metavar="name")
        self.parser.add_argument(
            '--output',
            help='Folder to save the continuous organisation',
            type=str)
        self.parse_args()
        self.func = self.command_init
        self.run_command()

    def command_init(self):
        directory = self.output if self.output else os.getcwd()
        global_params = GlobalParams()
        global_params.create_or_update(self.name, directory)

        c_org_manager = ContinuousOrganisationManager(self.name)
        configs = '''version: 0.1            # the version of the smart contract
name: {}         # the name of your continuous organisation
summary: ''             # summary of your organization (optional)
website: ''             # where users can mint/burn tokens (optional)
wallet: ''              # main wallet of the organization
slope: 1.0              # slope of the buying curve
investor_reserve: 0.1   # percentage of invested money put in reserve
revenue_reserve: 0.3    # percentage of revenues put in reserve
initial_tokens: 1000000 # the number of tokens initially available
          '''.format(self.name)
        with open(c_org_manager.param_file, 'w+') as f:
            f.write(configs)

        logging.info(
            "Please configure your continuous organisation in the file {}".
            format(c_org_manager.param_file))
