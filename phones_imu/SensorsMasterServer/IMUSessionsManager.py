from time import sleep

from Packet import Packet
import Phone
from blender_interface import send_packet
from datetime import datetime
import os


SESSIONS_DIR = 'sessions'


def send_packets(packets):
    for i, packet in enumerate(packets):
        send_packet(packet)

        sleep(0.02)

        if i > 0 and i % 150 == 0:
            print(str(i) + ' packets have been sent')

    print(str(len(packets)) + ' packets have been sent')


def packets_save_to_file(packets):

    if not os.path.exists(SESSIONS_DIR):
        os.mkdir(SESSIONS_DIR)

    filename = 'session_' + datetime.now().strftime('%d_%m_%Y_%H:%M:%S') + '.txt'

    txt = ''

    for p in packets:
        txt += str(p) + '\n'

    with open(os.path.join(SESSIONS_DIR, filename), 'w') as file:
        file.write(txt)


class IMUSessionsManager:
    def __init__(self):
        self.phones: list[Phone] = list()

        self.imu_sessions: list[list[Packet]] = list()

    def add_session(self, session: list[Packet]):
        self.imu_sessions.append(session)

        # A session for each phone has been created. It's time to send the whole data to blender.
        if len(self.imu_sessions) == len(self.phones):

            packets = self.merge_sessions()

            send_packets(packets)

            packets_save_to_file(packets)

            self.imu_sessions.clear()

    def merge_sessions(self):
        #self.cut_shift()

        # Shift the timestamp counters to 0
        for i in range(len(self.imu_sessions)):
            for j in range(1, len(self.imu_sessions[i])):
                self.imu_sessions[i][j].timestamp -= self.imu_sessions[i][0].timestamp

        packets_merged = sum(self.imu_sessions, [])

        packets_merged.sort(key=lambda packet: packet.timestamp)

        return packets_merged

    """
    Eliminate the time shift in the sessions. Simply ignore the latency.
    Used for synchronization.
    
    
    removed. unfortunately the timestamps are incompatible for multiple phones.
    todo: make a timestamps based on the real clock
    """

    # def cut_shift(self):
    #
    #     init_timestamps = [s[0].timestamp for s in self.imu_sessions]
    #     latest = max(init_timestamps)
    #
    #     for s, packets in enumerate(self.imu_sessions):
    #
    #         cut_point = 0
    #
    #         for i, p in enumerate(packets):
    #             if p.timestamp >= latest:
    #                 cut_point = i
    #                 break
    #
    #         self.imu_sessions[s] = self.imu_sessions[s][cut_point:]
