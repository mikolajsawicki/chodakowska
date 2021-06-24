# Chordata Open Pose Protocol (COPP) server
# -- Pose data server for the Chordata Open Source motion capture system
#
# http://chordata.cc
# contact@chordata.cc
#
# Copyright 2019 Bruno Laurencich
#
# This file is part of Chordata Open Pose Protocol (COPP) server.
#
# COPP server is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# COPP server is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with COPP server.  If not, see <https://www.gnu.org/licenses/>.

import socket
import time
from copp_server.osc4py3_buildparse import oscbuildparse as oscparse

from Packet import Packet


port = 6565
server_address = ('localhost', port)

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)


def send_packet(packet: Packet):
    """ This function creates a dummy UDP server to send messages to the client. """

    test_timetag = time.time()
    test_timetag = oscparse.unixtime2timetag(0.001 * test_timetag)
    test_target = "q"
    first_msg_addr = "/%%/Chordata/" + test_target

    msgs = [oscparse.OSCMessage('/%/{}'.format(packet.label), ',ffff', packet.quaternion)]

    first_msg = [oscparse.OSCMessage(first_msg_addr, ",N", [None])]

    bun = oscparse.OSCBundle(test_timetag, first_msg + msgs)

    raw_bun = oscparse.encode_packet(bun)

    sock.sendto(raw_bun, server_address)


def dispose():
    sock.close()
