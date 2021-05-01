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
