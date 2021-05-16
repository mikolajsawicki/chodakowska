import threading
from time import sleep

from aiohttp import web
import keyboard

command = "START"


async def handle(request):
    return web.Response(text=command)


def get_command():
    global command

    while True:
        if keyboard.is_pressed('q'):
            print("STOP")
            command = "STOP"
        elif keyboard.is_pressed('s'):
            print("START")
            command = "START"

        sleep(0.05)


if __name__ == '__main__':
    command_listener = threading.Thread(target=get_command)
    command_listener.setDaemon(True)
    command_listener.start()

    app = web.Application()
    app.add_routes([web.get('/', handle),
                    web.get('/{name}', handle)])
    web.run_app(app)
