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

import requests
import globales
from lib.debug import *

__all__ = ['Telegram']

class Telegram():

    def __init__(self, token, chat_id):
        self.token = token
        self.chat_id = chat_id

    def send_message(self, message):
        if  message and self.token and self.chat_id:
            requests.post('https://api.telegram.org/bot{0}/sendMessage'.format(self.token), 
                          data={'chat_id': self.chat_id, 'text': message, 'parse_mode':'Markdown'})
            return True
        if not self.token:
            globales.GlobDebug.print("Error: Telegram Token is Null", DebugLevel.error)
        if not self.chat_id:
            globales.GlobDebug.print("Error: Telegram Chat ID is Null", DebugLevel.error)

        return False

#https://apps.timwhitlock.info/emoji/tables/unicode