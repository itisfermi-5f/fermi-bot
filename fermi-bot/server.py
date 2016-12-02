"""
This file is part of the fermi-bot project.
"""

import socket
import threading


class Server:
    def __init__(self, ip, port, inactivity_timeout=20, buffer_size=1024):
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind((ip, port))
        self.inactivity_timeout = inactivity_timeout
        self.buffer_size = buffer_size
        self.threads = []

    def listen(self):
        self.server.listen(5)
        while True:
            client, address = self.server.accept()
            client.settimeout(self.inactivity_timeout)
            thread = threading.Thread(target=self.serve_client, args=(client, address))
            thread.start()
            self.threads.append(thread)

    def serve_client(self, client, address):
        fragments = []
        while True:
            try:
                fragment = client.recv(self.buffer_size)
                if not fragment:
                    break
                fragments.append(fragment)
            except:
                client.close()
                return False
        client.close()
        message = ''.join(fragments)
        return False
