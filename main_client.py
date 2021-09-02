"""
from system.object.ai.recognizer import Recognizer
from system.object.ai.trainer import create_model

create_model()
recognizer = Recognizer()

while True:
    message = input("")
    res = recognizer.get_response(message)
    print(res)
"""

from system.object.server.client_core import Client
import os

os.system("")

client = Client("192.168.1.24", 5050, True)
client.connect()
client.run()