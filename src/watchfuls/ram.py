#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Monitorize your Raspberry Pi
#
# Copyright © 2019  Lorenzo Carbonell (aka atareao)
# <lorenzo.carbonell.cerezo at gmail dot com>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import importlib
import pprint
import re

class Watchful():
    debugMode = False

    def __init__(self, monitor):
        self.monitor = monitor
        pass

    def debug(self, message):
        if self.debugMode:
            if isinstance(message, str):
                print(message)
            else:
                pprint.pprint(message)

    def check(self):
        utils = importlib.import_module('__utils')
        stdout, stderr = utils.execute('free')
        self.debug(stdout)
        x = re.findall(r'Mem\w*:\s+(\d+)\s+(\d+)', stdout)
        per = float(x[0][1])/float(x[0][0]) * 100.0
        if per < 50:
            return True, 'Normal ram used {0:.1f}%'.format(per)
        return False, 'Excesive ram used {0:.1f}%'.format(per)

if __name__ == '__main__':
    wf = Watchful()
    print(wf.check())
