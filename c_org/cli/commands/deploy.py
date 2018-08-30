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

'''c_org apply command line'''

import logging
import os
import sys

from c_org.cli.command import COrgCommand
from c_org import ContinuousOrganisationManager
import c_org.utils as utils
from c_org.manager import Vault, GlobalParams, LocalParams

class COrgDeploy(COrgCommand):

    def __init__(self):
        super().__init__(command_id='deploy', leaf=True,
                         description='Create a Continuous Organisation')
        self.subcommand = True

    def run(self):
        self.parser.add_argument('output',
                                 help='Path to config.yaml',
                                 type=str,
                                 metavar="path")
        self.parser.add_argument('--wallet',
                                  help='Name of the wallet',
                                  type=str)
        self.func = self.command_deploy
        self.parse_args()
        self.run_command()

    def command_deploy(self):
        if os.path.isdir(self.output):
            self.output = os.path.join(self.output, "config.yaml")

        if not os.path.isfile(self.output):
            return logging.error('The path is not valid. Please add a path to the config.yaml file.')
        dirname = os.path.dirname(os.path.abspath(self.output))

        if not self.wallet:
            return logging.error('No wallet has been specified. Please add --wallet NAME. Add a wallet with the wallet command.')
        else:
            try:
                wallet = Vault().find_wallet(name=self.wallet)
            except ValueError:
                return logging.error('The wallet is not recognized. Add a wallet with the wallet command.')

        name = LocalParams(self.output).name
        GlobalParams().create_or_update(name, dirname)

        c_org_manager = ContinuousOrganisationManager(name)
        c_org_manager.deploy(wallet)


        # create free tokens
        #c_org_manager.free_tokens(config.get('initial_tokens'))

        logging.info("Great! Your continuous organisation exists!")
