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

from system.object.server.client import UlysseClient
import os

os.system("")

client = UlysseClient("192.168.1.24", 5050, False)

if client.connect():
    client.run()