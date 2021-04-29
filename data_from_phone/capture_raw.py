import socket


# Returns a list of data for each device

def capture_raw_sim(ports):

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

    data = [[] for _ in ports]

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
                data[i].append(message.decode('utf-8'))

        except socket.timeout:
            break


    for i, s in enumerate(sockets):
        with open('raw_' + str(i) + '.csv', 'w') as file_out:
            file_out.write('\n'.join(data[i]))

    return data
