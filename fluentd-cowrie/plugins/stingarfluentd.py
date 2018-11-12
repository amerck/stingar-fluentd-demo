# Copyright (C) 2018 Alexander Merck <merckedsec@gmail.com>
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc.,
# 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.

"""
Output plugin for the Stingar project using RabbitMQ.
Roughly based on the hpfeeds message format.41`
"""

from fluent import sender

import logging
logging.basicConfig(level=logging.INFO)

import cowrie.core.output

from cowrie.core.config import CONFIG

COWRIE_TOPIC = 'cowrie.sessions'


class Output(cowrie.core.output.Output):
    """
    Output plugin for Fluentd
    """

    def __init__(self):
        cowrie.core.output.Output.__init__(self)

    def start(self):
        host = CONFIG.get('output_stingarfluentd', 'host')
        port = CONFIG.getint('output_stingarfluentd', 'port')
        app = CONFIG.get('output_stingarfluentd', 'app')

        self.sender = sender.FluentSender(app, host=host, port=port)
        self.meta = {}

    def stop(self):
        self.sender.close()

    def write(self, entry):

        session = entry["session"]
        if entry["eventid"] == 'cowrie.session.connect':
            self.meta[session] = {'session': session,
                                  'startTime': entry["timestamp"],
                                  'endTime': '',
                                  'peerIP': entry["src_ip"],
                                  'peerPort': entry["src_port"],
                                  'hostIP': entry["dst_ip"],
                                  'hostPort': entry["dst_port"],
                                  'loggedin': None,
                                  'credentials': [],
                                  'commands': [],
                                  'unknownCommands': [],
                                  'urls': [],
                                  'versions': None,
                                  'ttylog': None}

        elif entry["eventid"] == 'cowrie.login.success':
            u, p = entry["username"], entry["password"]
            self.meta[session]["logged_in"] = (u, p)

        elif entry["eventid"] == 'cowrie.login.failed':
            u, p = entry["username"], entry["password"]
            self.meta[session]["credentials"].append((u, p))

        elif entry["eventid"] == 'cowrie.command.success':
            c = entry["input"]
            self.meta[session]["commands"].append(c)

        elif entry["eventid"] == 'cowrie.command.failed':
            uc = entry["input"]
            self.meta[session]["unknownCommands"].append(uc)

        elif entry["eventid"] == 'cowrie.session.file_download':
            url = entry["url"]
            self.meta[session]["urls"].append(url)

        elif entry["eventid"] == 'cowrie.client.version':
            v = entry["version"]
            self.meta[session]["version"] = v

        elif entry["eventid"] == 'cowrie.log.closed':
            with open(entry["ttylog"]) as ttylog:
                self.meta['ttylog'] = ttylog.read().encode('hex')

        elif entry["eventid"] == 'cowrie.session.closed':
            meta = self.meta[session]
            self.meta[session]['endTime'] = entry["timestamp"]
            self.sender.emit(COWRIE_TOPIC,
                             meta)
