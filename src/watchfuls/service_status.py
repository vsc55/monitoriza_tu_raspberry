#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Monitorize your Raspberry Pi
#
# Copyright © 2019  Javier Pastor (aka VSC55)
# <jpastor at cerebelum dot net>
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

import concurrent.futures
import lib.tools
import globales
import lib.debug
import lib.module_base
import lib.monitor


class Watchful(lib.module_base.ModuleBase):

    def __init__(self, monitor):
        super().__init__(monitor, __name__)

    def check(self):
        listservice = []
        for (key, value) in self.get_conf('list', {}).items():
            globales.GlobDebug.print("Service: {0} - Enabled: {1}".format(key, value), lib.debug.DebugLevel.info)
            if value:
                listservice.append(key)

        returnDict = {}
        with concurrent.futures.ThreadPoolExecutor(max_workers=self.get_conf('threads', self._default_threads)) as executor:
            future_to_service = {executor.submit(self.__service_check, service): service for service in listservice}
            for future in concurrent.futures.as_completed(future_to_service):
                service = future_to_service[future]
                try:
                    returnDict[service] = future.result()
                except Exception as exc:
                    returnDict[service] = {}
                    returnDict[service]['status'] = False
                    returnDict[service]['message'] = 'Service: {0} - *Error: {1}* {1}'.format(service, exc, u'\U0001F4A5')

        msg_debug = '*'*60 + '\n'
        msg_debug = msg_debug + "Debug [{0}] - Data Return:\n".format(self.NameModule)
        msg_debug = msg_debug + "Type: {0}\n".format(type(returnDict))
        msg_debug = msg_debug + str(returnDict) + '\n'
        msg_debug = msg_debug + '*'*60 + '\n'
        globales.GlobDebug.print(msg_debug, lib.debug.DebugLevel.debug)
        return True, returnDict

    def __service_check(self, service):
        status, message = self.__service_return(service)
        rCheck = {}
        rCheck['status'] = status
        rCheck['message'] = ''
        if self.chcek_status(status, self.NameModule, service):
            sMessage = 'Service: {0}'.format(service)
            if status:
                sMessage = '{0} {1}'.format(sMessage, u'\U00002705')
            else:
                sMessage = '{0} - *Error: {1}* {2}'.format(sMessage, message, u'\U000026A0')
            self.send_message(sMessage, status)
        return rCheck

    def __service_return(self, service):
        stdout, stderr = lib.tools.execute('systemctl status '+service)
        if stdout == '':
            return False, stderr[:-1]
        return True, ''


if __name__ == '__main__':

    wf = Watchful(None)
    print(wf.check())
