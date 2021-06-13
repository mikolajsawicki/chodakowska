import keyboard
from http.server import BaseHTTPRequestHandler, HTTPServer
import logging
import threading
from blender_interface import Packet, send_packet
from Phone import Phone
from time import sleep

"""
Very simple HTTP server in python for logging requests
Usage::
    sudo python main.py
"""

command = "STOP"

phones_connected = []


def send_to_blender(data):
    # Decode from UTF-16-LE to utf-8
    data = data.replace(b'\x00', b'')

    lines = data.decode('utf-8').split('\n')

    print("The transfer has started.")

    print([str(i) + ": " + line for i, line in enumerate(lines[:6])])
    label = lines[4]

    # Ignore the preambule and content after the message
    for line in lines[5:-3]:
        # Send a packet

        quaternions = [float(q) for q in line.split(' ')[1:5]]

        if len(quaternions) == 4:
            p = Packet(label, quaternions)
            send_packet(p)
            # print('Packet ' + str(p.quaternions) + ' has been sent.')

            sleep(0.05)

    print("The transfer has stopped.")


class S(BaseHTTPRequestHandler):

    def _set_response(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

    def do_GET(self):
        # logging.info("GET request,\nPath: %s\nHeaders:\n%s\n", str(self.path), str(self.headers))
        # logging.info("GET")
        client_ip = self.client_address[0]

        if client_ip not in [phone.ip for phone in phones_connected]:
            phones_connected.append(Phone(client_ip, ''))

        self._set_response()

        self.wfile.write(bytes(command + '\n', "utf-8"))

    def do_POST(self):
        content_length = int(self.headers['Content-Length'])  # <--- Gets the size of data
        post_data = self.rfile.read(content_length)  # <--- Gets the data itself

        logging.info("POST request,\nPath: %s\nHeaders:\n%s\n\nBody:\n%s\n",
                     str(self.path), str(self.headers), post_data.decode('utf-8'))

        send_to_blender(post_data)

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
    from sys import argv

    keyboard.on_press_key("q", lambda _: set_command('STOP'))
    keyboard.on_press_key("s", lambda _: set_command('START'))

    if len(argv) == 2:
        run(port=int(argv[1]))
    else:
        run()
