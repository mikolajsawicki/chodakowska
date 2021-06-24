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
    return r3.as_quat().tolist()


def rotate180y(quat):
    r2 = R.from_matrix([[-1, 0, 0],
                        [0, 1, 0],
                        [0, 0, -1]])
    r3 = rotate(quat, r2)
    return r3.as_quat().tolist()


def rotate180z(quat):
    r2 = R.from_matrix([[-1, 0, 0],
                        [0, -1, 0],
                        [0, 0, 1]])
    r3 = rotate(quat, r2)
    return r3.as_quat().tolist()


def rotate90x(quat):
    r2 = R.from_matrix([[1, 0, 0],
                        [0, 0, -1],
                        [0, 1, 0]])
    r3 = rotate(quat, r2)
    return r3.as_quat().tolist()


def rotate90y(quat):
    r2 = R.from_matrix([[0, 0, 1],
                        [0, 1, 0],
                        [-1, 0, 0]])
    r3 = rotate(quat, r2)
    return r3.as_quat().tolist()


def rotate90z(quat):
    r2 = R.from_matrix([[0, -1, 0],
                        [1, 0, 0],
                        [0, 0, 1]])
    r3 = rotate(quat, r2)
    return r3.as_quat().tolist()


def swap_axis(quat):
    r1 = R.from_quat(quat)
    l = r1.as_euler('xyz', degrees=True).tolist()
    z = list[2]
    x = list[0]
    l[2] = x
    l[0] = z
    return l
