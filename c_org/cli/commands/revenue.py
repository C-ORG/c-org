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

from c_org.cli.command import COrgCommand


class COrgRevenue(COrgCommand):

    def __init__(self):
        super().__init__(command_id='revenue',  leaf=True,
                         description='Provide some statistics')
        self.subcommand = True



    def run(self):
        self.func = COrgRevenue.save_revenue
        self.parse_args()
        self.run_command()

    @staticmethod
    def save_revenue():
        print("Revenue")
