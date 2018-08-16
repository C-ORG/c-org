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

'''c_org command line'''

import logging
import os
import argparse
import c_org.utils as utils
from c_org.cli.command import COrgCommand


class COrg(COrgCommand):

    def __init__(self):
        super().__init__(command_id='',
                         description='Utility for Continuous Organisation')

    def parse_args(self):
        self._import_subcommands(c_org.cli.commands)
        super().parse_args()

    def main(self):
        self.parse_args()

        if self.debug:
            logging.basicConfig(level=logging.DEBUG, format='%(levelname)s:%(message)s')
            os.environ['G_MESSAGES_DEBUG'] = 'all'
        else:
            logging.basicConfig(level=logging.INFO, format='%(message)s')

        self.run_command()
