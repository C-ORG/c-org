#!/usr/bin/python3
#
# This manages the global parameters stored in ~/.c-org/global.yaml
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
'''c-org global params'''

import os
from c_org.manager.base import BaseManager
from c_org.utils import get_c_org_path, get_global_params_file


class GlobalParams(BaseManager):
    ''' Manage the YAML file ~/.c-org/global.yaml containing global informations on the CO's folders '''

    @property
    def filename(self):
        return get_global_params_file()

    @property
    def c_orgs(self):
        return self.get('c-orgs', default=[])

    @property
    def names(self):
        '''
        Return the list of Continuous Organisations' names.

        >>> g = GlobalParams(os.path.join(get_c_org_path(), "global.yaml"))
        >>> g.data = {'c-orgs': [{'name':'foo'}, {'name':'bar'}]}
        >>> g.names
        ['foo', 'bar']
        '''
        return [co.get('name') for co in self.c_orgs]

    def find_by_name(self, name):
        ''' Return the path to a continuous organisation whose name is givenself.

        >>> g = GlobalParams(os.path.join(get_c_org_path(), "global.yaml"))
        >>> g.data = {'c-orgs': [{'name':'foo', 'dir':'/dev/'},{'name':'bar', 'dir':'/homes/'}]}
        >>> g.find_by_name('foo')
        '/dev/'
        '''
        for co in self.c_orgs:
            if co.get('name') == name:
                return co.get('dir')

    def create_or_update(self, name, dir):
        ''' Create a continuous organisation folder or update the folder in the database (the files are not moved nor suppressed)

        >>> g = GlobalParams(os.path.join(get_c_org_path(), "global.yaml"))
        >>> g.data = {'c-orgs': []}
        >>> g.create_or_update('foo', '/dev/')
        >>> g.data
        {'c-orgs': [{'name': 'foo', 'dir': '/dev/'}]}
        >>> g.create_or_update('foo', '/etc/')
        >>> g.data
        {'c-orgs': [{'name': 'foo', 'dir': '/etc/'}]}
        '''
        if self.exists(name, "name", "c-orgs"):
            self.remove(name, 'name', 'c-orgs')
        self.c_orgs.append({'name': name, 'dir': dir})
        self.save()


if __name__ == "__main__":
    import doctest
    import tempfile
    doctest.testmod()
