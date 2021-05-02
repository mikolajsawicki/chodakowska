import numpy as np
from skinematics.sensors.manual import MyOwnSensor
from skinematics.view import orientation
from skinematics.quat import q_conj, quat2seq

sensor = None


def visualize(quaternions, rate):
    orientation(quaternions, 'data/animation.mp4', 'The visualisation of captured quaternions', deltaT=1000. / rate)


def imu_to_quaternions(data):
    initial_orientation = np.array([[1, 0, 0], [0, 0, -1], [0, 1, 0]])

    sensor = MyOwnSensor(in_data=data, R_init=initial_orientation)

    return sensor.quat


# Returns the Euler's angle: a tuple of phi, theta, psi
def angle(q1, q2):
    qd = q_conj(q1) * q2

    return quat2seq(qd, 'Euler')
