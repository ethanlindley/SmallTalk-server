import sys

from core.server import Server
from core.channel import Channel

server = Server()
channel = Channel(server)
if sys.argv[1] == "server":
    server.start_server()
elif sys.argv[1] == "channel":
    channel.setup_channel()
