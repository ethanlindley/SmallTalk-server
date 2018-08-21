import socket
from logger import Logger


class Server(object):
    def __init__(self, host='127.0.0.1', port=6667, backlog=10000, channels={}):
        self.notify = Logger('Server')

        self.host = host
        self.port = port
        self.backlog = backlog

        self.channels = channels  # each server can have multiple channels
        self.peers = []  # active channel connections to server
        self.nicknames = []  # registered nicknames across all channels on the server

    def start_server(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_addr = (self.host, self.port)
        
        self.notify.info('starting server at {0}:{1}'.format(*server_addr))
        s.bind(server_addr)
        s.listen(self.backlog)  # should never exceed 10000 connection attempts on the socket listener

        while True:
            conn, client_addr = s.accept()
            try:
                self.notify.warning('new incoming connection from {0}:{1}'.format(*client_addr))
                self.peers.append(conn)
                while True:
                    data = conn.recv(1024)
                    self.notify.debug('new data received - {!r}'.format(data))
                    if data:
                        for client in self.peers:
                            if client == conn:
                                continue
                            # TODO - handle packet data
                    else:
                        self.notify.warning('invalid data received from {0}:{1} - {!r}'.format(client_addr[0], client_addr[1], data))
                        break
            finally:
                conn.close()
