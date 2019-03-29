#!/usr/bin/python3
#
# The manager class is an abstract class to manage a Continuous Organisation without any blockchain dependancies
# It is used to be stable and absolutely backward-compatible
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
'''c_org configuration manager'''

from c_org.manager.vault import Vault
from c_org.manager.global_params import GlobalParams
from c_org.manager.local_params import LocalParams
from c_org.manager.base import BaseManager

__all__ = ['Vault', 'GlobalParams', 'BaseManager', 'LocalParams']
