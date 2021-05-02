from capture_imu import capture_imu_streams
from imu_to_quaternions import imu_to_quaternions, angle
from convert_to_chordata import convert_to_chordata
import json

import argparse


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-d', "--display", help="Display the animation.", action="store_true")
    parser.add_argument('-p', "--ports", nargs='+', help="Specify the ports for the capturing devices.", type=int)
    parser.add_argument('-c', "--chordata", help="Create a json file for chordata.", action="store_true")
    parser.add_argument('-b', "--blender", help="Send the stream to the blender addon.", action="store_true")
    parser.add_argument('-e', "--euler",
                        help="Calculate the Euler angles (only for 2 devices - temporarily). (pre)BETA.",
                        action="store_true")

    return parser.parse_args()



if __name__ == "__main__":
    args = parse_args()

    # Capture the data

    # Default port
    ports = [5555]

    if args.ports:
        ports = [int(p) for p in args.ports]

    imu_streams = capture_imu_streams(ports)



    # A quaternions list for each device
    q_lists = []

    for i, stream in enumerate(imu_streams):

        # Convert to quaternions
        quaternions = imu_to_quaternions(stream)
        q_lists.append(quaternions)


        # Generate the output:
        output = ''

        for q in quaternions:
            line = ','.join([str(n) for n in q])
            output += line + '\n'

        with open('data/quaternions_' + str(i), 'w') as f:
            f.write(output)

        print('Device ' + str(i) + ':')
        print(output + '\n' * 2)



    if args.chordata:

        # Chordata needs a label for each device
        labels = [str(i) for i in range(len(q_lists))]

        q_json = convert_to_chordata(q_lists, labels, imu_streams[0]['rate'])

        with open('data/chordata_quaternions.json', 'w') as file:
            json.dump(q_json, file)



    if args.euler:

        with open('data/euler', 'w') as f:
            for q1, q2 in zip(q_lists[0], q_lists[1]):
                line = ', '.join([str(a) for a in angle(q1, q2)]) + '\n'
                f.write(line)
