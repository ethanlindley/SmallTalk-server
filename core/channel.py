from logger import Logger


class Channel(object):
    def __init__(self, parent, host='127.0.0.1', port=6668, name='undefined', topic='undefined'):
        self.notify = Logger('Channel')  # TODO - generate unique hashes for each channel?

        self.parent = parent
        assert self.parent, self.notify.warning('Make sure the channel is being instantiated with the parent server object!')

        self.host = host
        self.port = port
        self.name = name
        self.topic = topic
