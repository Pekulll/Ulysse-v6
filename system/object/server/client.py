from system.object.server.client_core import Client
from system.object.debug import log, warn, error, debug

from speech_recognition import Microphone, Recognizer

import json
import os

class UlysseClient(Client):
    def __init__(self, server, port, debug=False):
        super().__init__(server, port, debug)
        self.load_configuration()
        self.load_language()
    
    
    
    def load_configuration(self):
        """
        Load the assistant's configuration
        """
        
        try:
            with open("./system/config.json", "r", encoding="utf-8") as json_config:
                config = json.load(json_config)
                self.VERSION = config['version']
                self.NAME = config['name']
                self.LANGUAGE = config['language']
                self.TIMEOUT = config['timeout']
                self.THRESHOLD = config['threshold']
        except Exception as e:
            error(f"[SYSTEM] Unable to load config.json!")
        else:
            log("[SYSTEM] Configuration loaded!")
    
    def load_language(self):
        """
        Load the assistant's language system file
        """
        
        try:
            with open(f"./system/data/language/{self.LANGUAGE}/system.json", "r", encoding="utf-8") as json_lang:
                self.language = json.load(json_lang)
        except Exception as e:
            error(f"[SYSTEM] Unable to load './system/language/{self.LANGUAGE}/system.json'!")
        else:
            log(self.language['sys_lang_file_loaded'])
    
    
    
    def run(self):
        self.create_thread()
    
    def create_thread(self):
        """
        Create one thread to write input.
        Launch the listenning sequence.
        """
        
        from threading import Thread
        
        rt = Thread(target=self.listen_server, name="Ulysse.request")
        rt.start()
        if self.debug: debug(f"Ulysse.request thread started!")
        
        Thread(target=self.listen_keyboard, name="Ulysse.keyboard").start()
        if self.debug: debug(f"Ulysse.keyboard thread started!")
        
        # Thread(target=self.listen_mic, name="Ulysse.mic").start()
        # if self.debug: debug(f"Ulysse.mic started!")
        
        rt.join()
    
    def listen_server(self):
        """
        Listen every request from the server.
        """
        
        if not self.connected:
            return
        
        try: request = self.receive()
        except Exception as e:
            error("Server has been disconnected! Stopping client...")
            log("Press any key to end...")
            self.connected = False
            return
        
        if request == None:
            error("Can't achieve the reception of the request from the server.")
            return
        
        self.on_request_received(request)
        self.process_request(request)
        self.listen_server()
    
    def listen_keyboard(self):
        """
        Listen user keyboard input, 
        and send it to the server.
        """
        
        if not self.connected:
            return
        
        speech = str(input())
        if speech != "": self.send("speech", speech)
        self.listen_keyboard()
    
    def listen_mic(self):
        """
        Listen the microphone of the user,
        and send the speech to the server.
        """
        
        if not self.connected:
            return
        
        try:
            log(self.language["voice_listenning"])

            recognizer = Recognizer()

            with Microphone() as source:
                audio = recognizer.listen(source)
                log(self.language["voice_analyze"])
                print("")

            try: 
                data = recognizer.recognize_google(audio, show_all=True, language=self.LANGUAGE)
                speech = str(data['alternative'][0]['transcript'])
                self.send("speech", speech)
            except Exception as e:
                warn(self.language["voice_not_recognize"])
        except Exception as e:
            error("An error as occured during listenning! " + str(e))
        
        self.listen_mic()
    
    
    
    def process_request(self, request: dict):
        """
        Process a request.
        """
        
        if request['name'] == "speech":
            log(request['content'])
            # say(request['content'])