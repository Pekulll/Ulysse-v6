from system.object.server.client_core import Client
from system.object.debug import log, warn, error, debug
from system.object.ui.main_screen import MainScreen
from system.object.console import Console

from speech_recognition import Microphone, Recognizer
from PyQt5.QtWidgets import *

import json
import importlib

class UlysseClient(Client):
    def __init__(self, server, port, debug=False):
        super().__init__(server, port, debug)
        
        self.console = Console()
        
        self.load_configuration()
        self.load_language()
        self.load_contact()
    
    
    """ Load data section """
    
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
                self.HOUSE = config['house_name']
                self.ROOM = config['room_name']
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
    
    def load_contact(self):
        """
        Load the assistant's contact file
        """
        
        try:
            with open(f"./system/data/contact.json", "r", encoding="utf-8") as json_contact:
                self.contacts = json.load(json_contact)
        except Exception as e:
            error(f"[SYSTEM] Unable to load './system/data/contact.json'!")
        else:
            log(self.language['sys_contact_file_loaded'])
    
    """ END """
    
    
    def oauth(self):
        oauth_request = {
            'local_version': self.VERSION,
            'local_name': self.NAME,
            'house_name': self.HOUSE,
            'room_name': self.ROOM
        }
        
        self.send('oauth', str(oauth_request))
    
    def run(self):
        self.create_thread()
    
    
    """ Thread's creation section """
    
    def create_thread(self):
        """
        Create one thread to write input.
        Launch the listenning sequence.
        """
        
        from threading import Thread
        
        rt = Thread(target=self.listen_server, name="Ulysse.request")
        rt.start()
        if self.debug: debug(f"Ulysse.request thread started!")
        
        if self.debug:
            Thread(target=self.listen_keyboard, name="Ulysse.keyboard").start()
            debug(f"Ulysse.keyboard thread started!")
        
        Thread(target=self.create_gui, name="Ulysse.gui", daemon=True).start()
        
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
    
    """ END """
    
    
    """ Interface section """
    
    def create_gui(self):
        """
        Create the app's GUI
        """
        
        self.app = QApplication([])
        self.window = MainScreen(self.language['ui_placeholder'], self.on_submit, self.on_close_gui)
        self.app.exec_()
    
    def on_submit(self):
        """
        Method call when the user press the ENTER key.
        Used to answer to the user.
        """
        
        speech = self.window.get_user_input()
        
        log(f"[USER] {speech}")
        self.window.append(f"[ <span style=\"color: #00c4ff;\"> {self.language.get('user_name')} </span> ] {speech}")
        
        if speech != "":
            self.send("speech", speech)
    
    def on_close_gui(self):
        """
        Call when the user close the application"s GUI
        """
        
        self.console.execute_cmd("clear")
        self.disconnect()
    
    """ END """
    
    
    """ Processing section """
    
    def process_request(self, request: dict):
        """
        Process a request.
        :param request The request to process
        """
        
        if request['name'] == "speech":
            self.write(request['content'])
            # say(request['content'])
        elif request['name'] == "tell":
            tell_request = eval(request['content'])
            
            for contact in self.contacts:
                if contact['house_name'].lower() == tell_request['from']['house_name'].lower():
                    if contact['room_name'].lower() == tell_request['from']['room_name'].lower():
                        self.write(f"[ {self.language.get('message_from')} <span style=\"color: #00c4ff;\">{contact['contact_name']}</span> ] {tell_request['message']}")
                        return
            
            debug(self.language.get('message_ignored').format(sender=f"{tell_request['from']['house_name']}"))
        elif 'cmd_' in request['name']:
            self.process_command(request['name'], request['content'])
    
    def process_command(self, command_tag, command_content):
        """
        Process an assistant command.
        :param command_tag The tag/name of the command
        :param command_content The content/args of the command
        """
        
        try:
            command = importlib.import_module(f"system.command.{command_tag}").AssistantCommand(self)
            command.execute(command_content)
        except Exception as e:
            error(f"Command error! {e}")
    
    """ END """
    
    def write(self, message):
        """
        Write a message in the log and/or on the GUI.
        :param message The message to write
        """
        
        self.window.append("[ <span style=\"color: #00ff1e;\">{self.NAME}</span> ] {message}".format(**locals(), **globals()))
        
        if self.debug:
            log(message)