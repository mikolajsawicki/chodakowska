from capture_raw import capture_raw_sim
from raw_to_quat import data_to_quat, process_raw_data, angle
import argparse


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-d', "--display", help="Display the animation.", action="store_true")
    parser.add_argument('-p', "--ports", nargs='+', help="Specify the ports of the capturing devices.", type=int)
    parser.add_argument('-e', "--euler", help="Calculate the Euler angles (only for 2 devices - temporarily).",
                        action="store_true")

    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()

    # Capture the data

    ports = [5555]

    if args.ports:
        ports = [int(p) for p in args.ports]

    raw_data = capture_raw_sim(ports)

    q_list = []

    for i, raw in enumerate(raw_data):

        data = process_raw_data(raw)

        # Convert to quaternions
        quaternions = data_to_quat(data)
        q_list.append(quaternions)

        # Generate the output

        output = ''

        for q in quaternions:
            line = ','.join([str(n) for n in q])
            output += line + '\n'

        with open('quaternions_' + str(i), 'w') as f:
            f.write(output)

        print('Device ' + str(i) + ':')
        print(output + '\n' * 2)

    if args.euler:

        with open('euler', 'w') as f:
            for q1, q2 in zip(q_list[0], q_list[1]):
                f.write(str(angle(q1, q2)) + '\n')
