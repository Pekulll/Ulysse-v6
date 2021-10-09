from system.object.server.client import UlysseClient
import os

os.system("")

client = UlysseClient("192.168.1.24", 5050, True)

if client.connect():
    client.run()