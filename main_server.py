from system.object.server.server import UlysseServer
import os

os.system("")

server = UlysseServer(port=1509, debug=False)
server.start()