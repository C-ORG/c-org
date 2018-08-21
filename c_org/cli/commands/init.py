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
from c_org.c_org_manager import ContinuousOrganisationManager
import c_org.utils as utils

class COrgInit(COrgCommand):

    def __init__(self):
        super().__init__(command_id='init', leaf=True,
                         description='Initialize a Continuous Organisation')
        self.subcommand = True

    def run(self):
        self.parser.add_argument('name',
                                 help='Continuous Organisation\'s name',
                                 type=str,
                                 metavar="name")
        self.parse_args()
        self.func = self.command_init
        self.run_command()

    def command_init(self):
        corg = utils.get_corg_path()
        if os.path.isdir(corg):
            logging.error("The folder .c-org already exists.")
        else:
            os.makedirs(corg)

        configs = '''c-org:
    version: 0.1            # the version of the smart contract
    name: {}         # the name of your continuous organization
    summary: 'The 1st continuous organization'
                          # summary of your organization (optional)
    website: 'https://invest.decusis.com'
                          # where users can mint/burn tokens (optional)
    wallet: '0x3aebb26a66b328cd8a60415710ce4de147657b0b'
                          # main wallet of the organization
    slope: 1.0              # slope of the buying curve
    investor_reserve: 0.1   # percentage of invested money put in reserve
    revenue_reserve: 0.3    # percentage of revenues put in reserve
    initial_tokens: 1000000 # the number of tokens initially available
          '''.format(self.name)
        with open(utils.get_config_file(), 'w+') as f:
            f.write(configs)

        with open(utils.get_corg_file(), 'w+') as f:
            f.write('''infura: ~
    wallets: ~''')
