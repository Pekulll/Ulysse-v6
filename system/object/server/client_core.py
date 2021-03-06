#!/usr/bin/python
# -*- coding: UTF-8 -*-

from system.object.debug import log, warn, error, debug
from threading import Thread
import socket

class Client():
    def __init__(self, server, port, debug=False):
        self.HEADER = 64
        self.FORMAT = "utf-8"

        self.PORT = port
        self.SERVER = server
        self.ADDR = (self.SERVER, self.PORT)
        
        self.debug = debug

    def connect(self):
        """
        Connect the client to the server.
        :return True if connected
        """
        
        try:
            self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.client.connect(self.ADDR)
            self.connected = True
            self.on_client_connected()
            return True
        except Exception as e:
            self.on_client_error(e)
            self.connected = False
            return False

    def run(self):
        """
        Starts the run loop of the client.
        """
        
        while True:
            msg = str(input("> "))
            self.send('basic_input', msg)

    def send(self, request_name, request_content=""):
        """
        Send a request to the server.
        :param msg The request to send
        """
        
        if not self.connected:
            return
        
        msg = str({"name": request_name, "content": request_content})
        
        if msg != "" and type(msg) == str:
            request = msg.encode(self.FORMAT)
            request_length = len(request)
            
            send_length = str(request_length).encode(self.FORMAT)
            send_length += b' ' * (self.HEADER - len(send_length))
            
            self.client.send(send_length)
            self.client.send(request)
            
            self.on_request_sended(msg)

    def receive(self):
        """
        Receive a request from the server.
        :return The request, or none if there is no request
        """
        
        request_length = self.client.recv(self.HEADER).decode(self.FORMAT)
        request_length = int(request_length)

        if request_length:
            request = str(self.client.recv(request_length).decode(self.FORMAT))
            return eval(request)

        return None

    def disconnect(self):
        """
        Disconnect the client from the server.
        """
        
        self.send("disconnect")
        self.on_client_disconnected()
    
    def on_client_connected(self):
        """
        Method calls when the client is connected.
        """
        
        log(f"This client has successfully been connected to the server [{self.SERVER}].")
        self.oauth()
    
    def oauth(self):
        """
        Method calls to authentificate the client.
        """
        
        warn("This client don't have an oauth method.")
    
    def on_request_sended(self, request):
        """
        Method calls when the client has send a request to the server.
        :param request The sended request
        """
        
        if self.debug:
            debug(f"Request sended to the server [{self.SERVER}] on port {self.PORT}. Request's content: {request} .")
    
    def on_request_received(self, request):
        """
        Method calls when the client has receive a request from the server.
        :param request The received request
        """
        
        if self.debug:
            debug(f"Request received from the server [{self.SERVER}] on port {self.PORT}. Request's content: {request} .")
    
    def on_client_disconnected(self):
        """
        Method calls when the client is disconnected.
        """
        
        warn(f"This client has been disconnected from the server.")
    
    def on_client_error(self, client_error):
        """
        Method calls when the client triggers an error.
        :param client_error The raised error
        """
        
        if type(client_error) == ConnectionRefusedError:
            error(f"Server unreachable. Please contact an administrator to solve this issue.")
            return
        
        error(f"An error has occurred! {client_error}")