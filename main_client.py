from system.object.ai.recognizer import Recognizer
from system.object.ai.trainer import create_model

create_model()
recognizer = Recognizer()

while True:
    message = input("")
    res = recognizer.get_response(message)
    print(res)