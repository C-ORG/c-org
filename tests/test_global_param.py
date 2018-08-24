#!/usr/bin/python3
# Unit tests for vault mixin.
#
# Copyright (C) 2018 Continuous Organisation
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

import os
import sys
import unittest
import tempfile
import subprocess
import yaml
import c_org.utils as utils
from c_org.manager import GlobalParams
from .test_base import TestBase



class TestGlobalParam(TestBase):
    '''Param mixin tests'''

    def setUp(self):
        self.temp_files()
        self.g = GlobalParams()

    def test_names(self):
        self.assertNotIn('c-orgs', self.g.names)
        self.assertIn('My C-Org', self.g.names)
        self.assertEqual(self.g.names, ['My C-Org', 'Super C-Org', 'my-co'])

    def test_save(self):
        self.g.data = ['foo']
        self.g.save()
        self.g.data = ['foo']
        self.g.load()
        self.assertEqual(self.g.data, ['foo'])

    def test_find_by_name(self):
        self.assertTrue(self.g.exists('My C-Org', 'name', 'c-orgs'))
        self.assertFalse(self.g.exists('my c-org', 'name', 'c-orgs'))
        self.assertFalse(self.g.exists('myc-org', 'name', 'c-orgs'))

    def test_create_or_update(self):
        self.assertFalse(self.g.exists('New C-Org', 'name', 'c-orgs'))
        self.g.create_or_update(name="New C-Org", dir="/etc/")
        self.assertTrue(self.g.exists('New C-Org', 'name', 'c-orgs'))

    def test_remove(self):
        self.assertTrue(self.g.exists('My C-Org', 'name', 'c-orgs'))
        self.g.remove('My C-Org', 'name', 'c-orgs')
        self.assertFalse(self.g.exists('My C-Org', 'name', 'c-orgs'))

    def test_no_c_org(self):
        self.assertTrue(self.g.exists('My C-Org', 'name', 'c-orgs'))
        self.g.data = {'c-orgs': []}
        self.g.save()
        self.assertFalse(self.g.exists('My C-Org', 'name', 'c-orgs'))



if __name__ == '__main__':
    unittest.main()
