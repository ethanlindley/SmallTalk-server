import socket

from core.structs import Packet
from core.logger import Logger


class Channel(object):
    def __init__(self, parent, host='127.0.0.1', port=6668, name='undefined', topic='undefined'):
        self.notify = Logger('Channel')  # TODO - generate unique hashes for each channel?

        self.parent = parent

        self.host = host
        self.port = port
        self.name = name
        self.topic = topic

    def setup_channel(self):
        self.notify.warning('attempting to establish connection to server...')
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((self.host, self.parent.port))
            s.sendall(bytes([1]))
            try:
                data = s.recv(4096)
                self.notify.debug('received data - {}'.format(data))
                self.handle_data(Packet(data))
            except Exception as e:
                raise Exception(e)

    def handle_data(self, packet):
        if packet.data[0] == 2:
            self.notify.info('successfully established connection to server!')
