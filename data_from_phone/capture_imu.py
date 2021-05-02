import socket
import numpy as np
from typing import Iterable, Sequence

"""
Returns a list of data streams for each device, e.g.

[
  [
      '86888.69429, 3,  -0.268, -0.038,  9.912, 5,  -8.313,-11.938,-37.500, 82,   0.040,  0.015,  0.345, 84,   0.009, -0.002, -0.943',
      '86888.75926, 3,  -0.115,  0.115,  9.768, 5,  -8.000,-11.688,-37.375, 82,  -0.105,  0.015,  0.345, 84,   0.010, -0.002, -0.944',
      '86888.88928, 3,  -0.115,  0.115,  9.912, 5,  -8.000,-11.250,-37.625, 82,   0.028,  0.021,  0.345, 84,   0.009, -0.002, -0.946',
      '86889.01927, 3,  -0.115,  0.115,  9.768, 5,  -7.750,-11.500,-37.688, 82,   0.028,  0.021,  0.041, 84,   0.009, -0.002, -0.947',
      '86889.08428, 3,  -0.268,  0.115,  9.768, 5,  -7.625,-11.250,-37.625, 82,   0.022,  0.027,  0.345, 84,   0.008, -0.002, -0.946',
  ],
  [
      '86889.21427, 3,  -0.268,  0.115,  9.912, 5,  -7.875,-11.813,-37.688, 82,   0.034,  0.009,  0.345, 84,   0.009, -0.003, -0.945',
      '86889.27928, 3,  -0.115,  0.115,  9.912, 5,  -8.063,-11.313,-37.313, 82,   0.021,  0.009,  0.198, 84,   0.009, -0.003, -0.946',
      '86889.40927, 3,  -0.268,  0.115,  9.912, 5,  -7.688,-10.938,-37.188, 82,  -0.123, -0.003,  0.345, 84,   0.009, -0.003, -0.946',
      '86889.47428, 3,  -0.115,  0.115,  9.912, 5,  -7.938,-11.875,-37.313, 82,   0.034,  0.003,  0.198, 84,   0.009, -0.003, -0.946',
      '86889.53929, 3,  -0.268,  0.115,  9.912, 5,  -7.875,-12.250,-38.000, 82,   0.027, -0.003,  0.345, 84,   0.009, -0.003, -0.947'
  ],
]

That's what a data frame is:
[ time, nr_of_sensor_1, x_1, y_1, z_1, nr_of_sensor_2, x_2, y_2, z_2, ... ]
"""


def capture_raw_streams(ports: Iterable) -> list[list[str]]:
    if len(set(ports)) != len(ports):
        raise ValueError('Ports have to be unique.')

    sockets = []

    for p in ports:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.settimeout(1)
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        s.bind(('', p))

        sockets.append(s)

    streams = [[] for _ in ports]

    # Wait for inputs - synchronize them
    for s in sockets:
        message = ''

        while not message:

            try:
                message, address = s.recvfrom(8192)

            except socket.timeout:
                pass

    while True:
        try:
            for i, s in enumerate(sockets):
                message, address = s.recvfrom(8192)
                streams[i].append(message.decode('utf-8'))

        except socket.timeout:
            break

    for i, s in enumerate(sockets):
        with open('data/raw_' + str(i) + '.csv', 'w') as file_out:
            file_out.write('\n'.join(streams[i]))

    return streams


# Returns a tuple of sensor data (x, y, z), extracted from a string data row
# 3 - Acclerometer, 4 - Gyroscope, 5 - Magnetic Field, 82 - Linear Accel., 84 - Rotation Vect.
def extract_sensor_data(frame: Sequence, sensor_number: int):

    try:
        i = frame.index(str(sensor_number))

        sensor_data = frame[i + 1: i + 4]

        return [float(x) for x in sensor_data]

    except ValueError:
        raise ValueError('Cant find a sensor data in the data stream.')


def avg_rate(time_serie):
    steps_sum = 0

    for i in range(1, len(time_serie)):
        steps_sum += time_serie[i] - time_serie[i - 1]

    avg_step = steps_sum / len(time_serie)

    return 1 / avg_step


def process_raw_stream(raw_stream):
    stream = {'timestamp': [], 'acc': [], 'omega': [], 'mag': []}

    for row in raw_stream:
        frame = [s.strip() for s in row.split(',')]
        stream['timestamp'].append(float(frame[0]))
        stream['acc'].append(extract_sensor_data(frame, 82))
        stream['omega'].append(extract_sensor_data(frame, 84))
        stream['mag'].append(extract_sensor_data(frame, 5))

    stream['rate'] = int(avg_rate(stream['timestamp']))

    stream['omega'] = np.array(stream['omega'], dtype=np.float32)

    return stream


def capture_imu_streams(ports):
    streams = capture_raw_streams(ports)

    for i in range(len(streams)):
        streams[i] = process_raw_stream(streams[i])

    return streams
