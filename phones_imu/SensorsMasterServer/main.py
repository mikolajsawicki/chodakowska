import keyboard
from http.server import BaseHTTPRequestHandler, HTTPServer
import logging
from blender_interface import Packet
from Phone import Phone
import IMUSessionsManager
import argparse


"""
Very simple HTTP server in python for logging requests
Usage::
    sudo python main.py
"""

command = "STOP"
merger = IMUSessionsManager.IMUSessionsManager()


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-f', "--file", type=str, help="Display the previously saved session. Pass a file as an argument.")

    return parser.parse_args()


def to_imu_packets(data) -> list[Packet]:
    packets = list()

    # Decode from UTF-16-LE to utf-8
    data = data.replace(b'\x00', b'')

    lines = data.decode('utf-8').split('\n')

    label = lines[4]

    # Ignore the preambule and content after the message
    for line in lines[5:-3]:

        # Convert a message line to a list of floats for creating a valid packet
        packet_raw = [float(q) for q in line.split(' ') if q]

        if len(packet_raw) == 5:
            timestamp = packet_raw[0]

            quaternion = packet_raw[1:5]

            p = Packet(label, quaternion, int(timestamp))
            packets.append(p)

    return packets


class S(BaseHTTPRequestHandler):

    def _set_response(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

    def do_GET(self):
        # logging.info("GET request,\nPath: %s\nHeaders:\n%s\n", str(self.path), str(self.headers))
        # logging.info("GET")
        client_ip = self.client_address[0]

        if client_ip not in [phone.ip for phone in merger.phones]:
            merger.phones.append(Phone(client_ip, ''))

        self._set_response()

        self.wfile.write(bytes(command + '\n', "utf-8"))

    def do_POST(self):
        content_length = int(self.headers['Content-Length'])  # <--- Gets the size of data
        post_data = self.rfile.read(content_length)  # <--- Gets the data itself

        logging.info("POST request,\nPath: %s\nHeaders:\n%s\n\nBody:\n%s\n",
                     str(self.path), str(self.headers), post_data.decode('utf-8'))

        merger.add_session(to_imu_packets(post_data))

        self._set_response()
        self.wfile.write("POST request for {}".format(self.path).encode('utf-8'))


def run(server_class=HTTPServer, handler_class=S, port=8080):
    logging.basicConfig(level=logging.INFO)
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    logging.info('Starting httpd...\n')
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    httpd.server_close()
    logging.info('Stopping httpd...\n')


def set_command(cmd):
    global command

    command = cmd


if __name__ == '__main__':
    keyboard.on_press_key("q", lambda _: set_command('STOP'))
    keyboard.on_press_key("s", lambda _: set_command('START'))

    args = parse_args()

    if args.file:
        packets = IMUSessionsManager.read_packets_from_file(args.file)
        IMUSessionsManager.send_packets(packets)
    else:

        run()
