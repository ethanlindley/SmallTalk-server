import socket
from logger import Logger


class Server(object):
    def __init__(self, host='127.0.0.1', port=6667, backlog=10000, channels={}):
        self.notify = Logger('Server')

        self.host = host
        self.port = port
        self.backlog = backlog

        self.channels = channels  # store connected channels to the server
        self.nicknames = []  # registered nicknames across all channels on the server

    def start_server(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
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
                    self.notify.debug('incoming data received from {0}:{1} - {!r}'.format(client_addr[0], client_addr[1], data))
                    if data:
                        # TODO - handle packet data
                        pass
                    else:
                        self.notify.warning('invalid data received from {0}:{1} - {!r}'.format(client_addr[0], client_addr[1], data))
                        break
            finally:
                conn.close()
