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


from c_org.cli.command import C_OrgCommand


class C_OrgStats(C_OrgCommand):

    def __init__(self):
        super().__init__(command_id='stats',
                         description='Provide some statistics')



    def run(self):  # pragma: nocover (requires user input)
        self.parser.add_argument('--config-file',
                                 help='Apply the config file in argument in addition to current configuration.')
        self.parser.add_argument('--timeout',
                                 type=int,
                                 help="Maximum number of seconds to wait for the user's confirmation")
        self.parse_args()
        self.run_command()

    def run_command():
        pass
