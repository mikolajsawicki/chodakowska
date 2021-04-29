import csv
import numpy as np
from skinematics.sensors.manual import MyOwnSensor
from skinematics.view import orientation
from skinematics.quat import q_conj, quat2seq

sensor = None


def avg_rate(time_serie):
    steps_sum = 0

    for i in range(1, len(time_serie)):
        steps_sum += time_serie[i] - time_serie[i - 1]

    avg_step = steps_sum / len(time_serie)

    return 1 / avg_step


def process_raw_data(raw_data):
    data = {'timestamp': [], 'acc': [], 'omega': [], 'mag': []}

    for row in raw_data:
        r = row.split(',')

        data['timestamp'].append(float(r[0]))

        data['acc'].append([float(s) for s in r[10:13]])
        data['omega'].append([float(s) for s in r[13:16]])
        data['mag'].append([float(s) for s in r[6:7]])

    data['rate'] = int(avg_rate(data['timestamp']))

    data['omega'] = np.array(data['omega'], dtype=np.float32)

    return data


def visualize(quaternions, rate):
    orientation(quaternions, 'animation.mp4', 'The visualisation of captured quaternions', deltaT=1000. / rate)


def data_to_quat(data):
    initial_orientation = np.array([[1, 0, 0], [0, 0, -1], [0, 1, 0]])

    sensor = MyOwnSensor(in_data=data, R_init=initial_orientation)

    return sensor.quat


# Returns the Euler's angle: a tuple of phi, theta, psi
def angle(q1, q2):
    qd = q_conj(q1) * q2

    return quat2seq(qd, 'Euler')
