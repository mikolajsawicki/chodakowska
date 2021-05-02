import socket

# Gets a list of quaternion lists, a list of labels for every device. Then, gets a sampling rate.
# Returns a JSON for the Chordata Blender addon
def convert_to_chordata(q_lists, labels, rate):

    if len(q_lists) != len(labels):
        raise ValueError('You should enter a label for every quaternion list')

    time_step = 1 / rate

    result = []

    t = 0

    samples = max([len(l) for l in q_lists])

    for s in range(samples):

        t += time_step

        frame = {'time': t, 'data': []}

        for i, l in enumerate(q_lists):
            frame['data'].append(labels[i])
            frame['data'].extend(l[s])

        result.append(frame)

    return result


def send_to_chordata(quaternions_json):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.settimeout(1)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    s.bind(('', 6565))