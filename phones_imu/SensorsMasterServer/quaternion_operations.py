from scipy.spatial.transform import Rotation as R


def rotate(quat, r2):
    r1 = R.from_quat(quat)
    r3 = r2 * r1
    return r3


def rotate180x(quat):
    r2 = R.from_matrix([[1, 0, 0],
                        [0, -1, 0],
                        [0, 0, -1]])
    r3 = rotate(quat, r2)
    return r3


def rotate180y(quat):
    r2 = R.from_matrix([[-1, 0, 0],
                        [0, 1, 0],
                        [0, 0, -1]])
    r3 = rotate(quat, r2)
    return r3


def rotate180z(quat):
    r2 = R.from_matrix([[-1, 0, 0],
                        [0, -1, 0],
                        [0, 0, 1]])
    r3 = rotate(quat, r2)
    return r3
