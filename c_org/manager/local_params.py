#!/usr/bin/python3
#
# This manages the parameters of a continuous organisation
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
'''c-org parameters manager'''

from c_org.manager.base import BaseManager


class LocalParams(BaseManager):
    @property
    def name(self):
        """ Return the path to the continuous organisation's config.yaml file

        >>> l = LocalParams()
        >>> l._data = {'name': "My C-Org"}
        >>> l.name
        'My C-Org'
        """
        return self.get('name')
