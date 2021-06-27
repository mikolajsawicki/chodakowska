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
from quaternion_operations import *
from Packet import Packet
from time import sleep



port = 6565
server_address = ('localhost', port)

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)


def send_packets(packets):

    # Process the quaternions - for compatibility with Blender addon
    for i, packet in enumerate(packets):

        if packet.label == 'r-hand':
            packets[i].quaternion = rotate90z(packets[i].quaternion)
            packets[i].quaternion = swap_x_z_axis(packets[i].quaternion)
            packets[i].quaternion = invert_axis(packets[i].quaternion, 'x')
            packets[i].quaternion = invert_axis(packets[i].quaternion, 'y')

        elif packet.label == 'r-arm':
            packets[i].quaternion = rotate90z(packets[i].quaternion)
            packets[i].quaternion = swap_x_z_axis(packets[i].quaternion)
            packets[i].quaternion = invert_axis(packets[i].quaternion, 'x')
            packets[i].quaternion = invert_axis(packets[i].quaternion, 'y')

        elif packet.label == 'r-forarm':
            packets[i].quaternion = rotate90z(packets[i].quaternion)
            packets[i].quaternion = rotate180y(packets[i].quaternion)
            packets[i].quaternion = swap_x_z_axis(packets[i].quaternion)
            packets[i].quaternion = invert_axis(packets[i].quaternion, 'y')
            packets[i].quaternion = invert_axis(packets[i].quaternion, 'z')


    for i, packet in enumerate(packets):
        send_packet(packet)

        sleep(0.02)

        if i > 0 and i % 150 == 0:
            print(str(i) + ' packets have been sent')

    print(str(len(packets)) + ' packets have been sent')


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
