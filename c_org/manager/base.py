#!/usr/bin/python3
#
# This is the parent class for all context managers
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

'''c-org base manager'''

import yaml
from c_org.utils import get_c_org_path
import os


class BaseManager(object):

    def __init__(self, filename=""):
        # _data is assumed to be a dict
        self._data = None
        # filename should be implemented in child function
        self._filename = filename

    @property
    def filename(self):
        return self._filename

    @filename.setter
    def filename(self, value):
        self._filename = value

    @property
    def data(self):
        if not self._data:
            self.load()
        return self._data

    @data.setter
    def data(self, value):
        self._data = value

    def save(self):
        '''
        >>> b = BaseManager(os.path.join(get_c_org_path(), "vault.yaml"))
        >>> b.data = {'wallets': [{'name': 'bar'}]}
        >>> b.filename = "test.txt"
        >>> b.save()
        >>> with open(b.filename, 'r') as f:
        ...    print(yaml.load(f))
        {'wallets': [{'name': 'bar'}]}
        '''
        with open(self.filename, 'w+') as f:
            yaml.dump(self.data, f)

    def load(self):
        '''
        >>> b = BaseManager(os.path.join(get_c_org_path(), "vault.yaml"))
        >>> b.data = {'wallets': [{'name': 'bar'}]}
        >>> b.save()
        >>> b.data = {}
        >>> b.load()
        >>> b.data
        {'wallets': [{'name': 'bar'}]}
        '''
        with open(self.filename, 'r') as f:
            self.data = yaml.load(f)
        # TODO: load only dict and list

    def __enter__(self):
        self.load()

    def __exit__(self):
        self.save()

    def get(self, key, *keys, data=None, default=None):
        '''
        >>> b = BaseManager(os.path.join(get_c_org_path(), "vault.yaml"))
        >>> b.data = {'safe': {'wallets': [{'name':'bar'}]}}
        >>> b.get('safe', 'wallets')
        [{'name': 'bar'}]
        '''
        if not data:
            data = self.data
        if keys:
            return self.get(*keys, data=data.get(key))
        return data.get(key, default)

    def set(self, old_value, value, cmp, *keys, data=None):
        '''
        >>> b = BaseManager(os.path.join(get_c_org_path(), "vault.yaml"))
        >>> b.data = {'wallets':[{'name':'foo'}]}
        >>> b.set('foo', 'bar', 'name', 'wallets')
        >>> b.data
        {'wallets': [{'name': 'bar'}]}
        '''
        data = self.get(*keys)
        for d in data:
            if d.get(cmp) == old_value:
                d[cmp] = value
        self.save()

    def exists(self, value, cmp, *keys):
        '''
        >>> b = BaseManager(os.path.join(get_c_org_path(), "vault.yaml"))
        >>> b.data = {'wallets':[{'name':'foo'},{'name':'bar'}]}
        >>> b.exists('bar', 'name', 'wallets')
        True
        '''
        data = self.get(*keys)
        for d in data:
            if d.get(cmp) == value:
                return True
        return False

    def add(self, element, key, *keys):
        '''
        >>> b = BaseManager(os.path.join(get_c_org_path(), "vault.yaml"))
        >>> b.data = {'wallets':[]}
        >>> b.add({'name': 'bar'}, 'wallets')
        >>> b.data
        {'wallets': [{'name': 'bar'}]}
        '''
        data = self.get(key, *keys)
        data.append(element)
        self.save()

    def remove(self, value, cmp, *keys):
        '''
        >>> b = BaseManager(os.path.join(get_c_org_path(), "vault.yaml"))
        >>> b.data = {'wallets':[{'name':'foo'},{'name':'bar'}]}
        >>> b.remove('bar', 'name', 'wallets')
        >>> b.data
        {'wallets': [{'name': 'foo'}]}
        '''
        data = self.get(*keys)
        for d in data:
            if d.get(cmp) == value:
                data.remove(d)
        self.save()


if __name__ == "__main__":
    import doctest
    doctest.testmod()
