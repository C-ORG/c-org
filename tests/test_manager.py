#!/usr/bin/python3
# Test ContinuousOrganisationManager
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

import os
import tempfile
import unittest

from derive.manager import ContinuousOrganisationManager


class TestContinuousOrganisationManager(unittest.TestCase):

    def setUp(self):
        self.workdir = tempfile.TemporaryDirectory()
        self.c_org_manager = ContinuousOrganisationManager()
        os.environ.set('DERIVE_PATH', self.workdir)
        os.makedirs(os.path.join(self.workdir.name, "contracts/"))
        os.makedirs(os.path.join(self.workdir.name, "configs/"))
        with open(os.path.join(self.workdir.name, "configs/test.yaml"), 'w') as fd:
            print('''c-org:
  version: 0.1
  deployed: false
  parameters:
    slope: 1.0
    alpha: 0.1
    beta: 0.3
  addresses:
    smart-contract: ~
    owner: ~
  node-provider: ganache
''', file=fd)
        with open(os.path.join(self.workdir.name, "contracts/test.sol"), 'w') as fd:
            print('''pragma solidity ^0.4.21;
contract Greeter {
    string public greeting;
    function Greeter() public {
        greeting = 'Hello';
    }
    function setGreeting(string _greeting) public {
        greeting = _greeting;
    }
    function greet() view public returns (string) {
        return greeting;
    }
}
''', file=fd)


    def test_parse(self):
        c_org_manager = ContinuousOrganisationManager('test')
        config = c_org_manager.parse()
        self.assertIn('slope', config.get('parameters'))
        self.assertIn('smart-contract', config.get('addresses'))
        self.assertEquals(False, config.get('deployed')
        self.assertNotIn('gamma', config.get('parameters'))
        self.assertNotIn('owner', config)


    def test_build(self):
        pass
