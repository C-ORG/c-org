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
import shutil

import c_org.utils as utils
from c_org.c_org_manager import ContinuousOrganisationManager

rootdir = os.path.dirname(os.path.abspath(__file__))

class TestBase(unittest.TestCase):

    def temp_files(self):
        self.workdir = tempfile.TemporaryDirectory()
        os.environ['C_ORG_PATH'] = self.workdir.name

        # ressources
        configs_folder = utils.get_config_path()
        config_file = os.path.join(rootdir, "ressources", "config.yaml")
        shutil.copy(config_file, configs_folder)
        private_folder = utils.get_corg_path()
        private_file = os.path.join(rootdir, "ressources", ".c-org", "keys.yaml")
        os.makedirs(private_folder)
        shutil.copy(private_file, private_folder)
        # manager
        self.c_org_manager = ContinuousOrganisationManager()

    def cleanup(self):
        self.workdir.cleanup()

    def tearDown(self):
        self.cleanup()
