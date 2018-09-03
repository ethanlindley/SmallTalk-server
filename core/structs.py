""" Module `structs` contains miscellaneous classes and other objects used throughout the server application """


class Packet(object):
    def __init__(self, data=None):
        self.data = list(data)
