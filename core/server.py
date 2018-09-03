import socket

from core.structs import Packet
from core.logger import Logger


class Server(object):
    def __init__(self, host='127.0.0.1', port=6667, backlog=10000):
        self.notify = Logger('Server')

        self.host = host
        self.port = port
        self.backlog = backlog

        self.channels = {}  # store connected channels to the server
        self.nicknames = []  # registered nicknames across all channels on the server

    def start_server(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server_addr = (self.host, self.port)
        
        self.notify.info('starting server at {0}:{1}'.format(*server_addr))
        s.bind(server_addr)
        s.listen(self.backlog)

        while True:
            conn, client_addr = s.accept()
            try:
                self.notify.debug('incoming connection from {0}:{1}'.format(*client_addr))
                # TODO - determine whether new suggestion is a channel or a client
                while True:
                    data = conn.recv(1024)
                    self.notify.debug('incoming data received from {0}:{1} - {2}'.format(client_addr[0], client_addr[1], data))
                    if data:
                        # TODO - handle packet data
                        self.handle_data(Packet(data), conn)
                    else:
                        self.notify.warning('invalid data received from {0}:{1} - {2}'.format(client_addr[0], client_addr[1], data))
                        break
            finally:
                conn.close()

    def handle_data(self, packet, conn):
        if packet.data[0] == 1:
            try:
                self.register_channel(conn)
                self.notify.info('successfully registered new channel to server!')
                self.notify.debug(self.channels)
            except:
                raise Exception('unable to register new channel - is the client still connected to the server?')

    def register_channel(self, conn):
        try:
            channel = self.channels[len(self.channels)] + 1
            self.channels[channel] = conn
            conn.sendall([2])
        except KeyError:
            channel = 1000000
            self.channels[channel] = conn
            conn.sendall([2])
