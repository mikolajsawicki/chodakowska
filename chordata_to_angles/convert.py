import json
import pyquaternion as pyq
import math
import numpy as np

def quaternion_to_angle(q1, q2):
    q1 = pyq.Quaternion(q1)
    q2 = pyq.Quaternion(q2)

    # Get the 3D difference between these two orientations
    qd = q1.conjugate * q2

    # Calculate Euler angles from this difference quaternion
    phi = math.atan2(2 * (qd.w * qd.x + qd.y * qd.z), 1 - 2 * (qd.x ** 2 + qd.y ** 2))

    # TODO: angles greater than 90deg
    theta = math.asin(2 * (qd.w * qd.y - qd.z * qd.x))

    psi = math.atan2(2 * (qd.w * qd.z + qd.x * qd.y), 1 - 2 * (qd.y ** 2 + qd.z ** 2))

    # Result:
    return phi, theta, psi


with open("data.json", "r") as read_file:
    data = json.load(read_file)

    with open("data.csv", "w") as write_file:

        for d in data[1:]:
            quaternions = dict()

            for q in d['data']:
                name = q[0]
                quaternions[name] = q[1:]

            try:
                angles = np.array([
                    quaternion_to_angle(quaternions['l-arm'], quaternions['l-forarm']),
                    quaternion_to_angle(quaternions['l-arm'], quaternions['l-hand']),
                ])
            except ValueError:
                print('code it in a better way, pussy')
                pass

            write_file.write(', '.join(str(a) for a in angles.flatten()) + '\n')

            #print(angles)

