"""
This file is part of the fermi-bot project.
"""

import socket
import threading


class Server:
    protocol_auth = '##AUTH##'
    protocol_start = '##MESSAGE START##'
    protocol_end = '##MESSAGE END##'
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
        print("==] Connected to {}:{}.".format(address[0], address[1]))
        received = ""
        while True:
            try:
                fragment = client.recv(self.buffer_size)
                if not fragment:
                    break
                fragment = fragment.decode('utf-8')
                received += fragment
                print(received)
                if received.strip() == self.protocol_auth:
                    client.sendall(b'Processing authentication... ')
                    if self.handle_authentication(address):
                        client.sendall(b'Authentication granted.')
                    else:
                        client.sendall(b'Authentication failed.')
                    client.close()
                elif received.lstrip().startswith(self.protocol_start) and received.rstrip().endswith(self.protocol_end):
                    client.sendall(b'Processing message... ')
                    if self.handle_message(address, received[len(self.protocol_start):-(len(self.protocol_end)+1)]):
                        client.sendall(b'Message delivered.')
                    else:
                        client.sendall(b'Falied to send message.')
                    client.close()
#                elif received.startswith(self.protocol_start) and not received.endswith(self.protocol_end):
#                     continue
                else:
                    client.sendall(b'ERROR: message malformed')
                    print('ERROR: message malformed')
            except Exception as exc:
                print("==] Connection to {}:{} closed.".format(address[0], address[1]))
                client.close()
                return False
        print("==] Connection to {}:{} closed.".format(address[0], address[1]))
        client.close()
        return False

    # to be overridden by the Bot
    def handle_message(self, sender, message):
        print(sender, '|', message)
        return
        raise NotImplementedError('this method needs to be overridden externally.')

    def handle_authentication(self, sender):
        print('AUTH |', sender)
        return
        raise NotImplementedError('this method needs to be overridden externally.')

