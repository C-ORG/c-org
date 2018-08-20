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


class COrgInit(COrgCommand):

    def __init__(self):
        super().__init__(command_id='init', leaf=True,
                         description='Initialize a Continuous Organisation')
        self.subcommand = True

    def run(self):
        self.parse_args()
        self.func = self.command_init
        self.run_command()

    def command_init(self):
        path = os.environ.get('C_ORG_PATH', os.getcwd())
        corg = os.path.join(path, ".c-org")
        if os.path.isdir(corg):
            logging.error("The folder .c-org already exists.")
        else:
            os.makedirs(corg)
