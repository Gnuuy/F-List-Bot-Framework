import socket
import atexit
import signal

import json

# This script allows you to MANUALLY INJECT RAW CHAT messages to be sent to your output stream via the bot.
# Be careful with this. You can break the bot's runtime and might have to restart the bot if you screw up.
# As an example, you might enter the following as input to this command prompt, if you want to send a message to a channel:
# MSG {"channel": "channel_name_or_id_here", "message": "Your Message here"}
# You can also make the bot send other F-list chat protocol codes.
# Use this only if you know F-list's chat protocol.

def close_sock(signum, frame):
    global client_socket
    client_socket.close()


# The bot has a socket listening on a local host port for local connections.
def client_program():
    host = socket.gethostname()  # as both code is running on same pc
    port = 5000  # socket server port number

    global client_socket
    client_socket = socket.socket()  # instantiate
    client_socket.connect((host, port))  # connect to the server

    message = input(" -> ")  # take input

    while True:
        client_socket.send(message.encode())  # send message

        message = input(" -> ")  # again take input


if __name__ == '__main__':
    atexit.register(close_sock, 1, 2)
    signal.signal(signal.SIGINT, close_sock)
    client_program()