#!/usr/bin/python
# -*- coding: UTF-8 -*-

import socket

from system.object.debug import log, warn, error, debug

from traceback import format_exc
from threading import Thread

class Server():
    def __init__(self, port=5050, debug=False):
        self.HEADER = 64
        self.FORMAT = "utf-8"

        self.PORT = port
        self.SERVER = socket.gethostbyname(socket.gethostname())
        self.ADDR = (self.SERVER, self.PORT)

        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind(self.ADDR)
        
        self.debug = debug

    def start(self):
        """
        Starts the server.
        """
        
        self.on_server_startup()
        self.server.listen()

        Thread(target=self.handle_server_command, name="Server/Command_Input").start()
        
        while True:
            conn, addr = self.server.accept()
            Thread(target=self.handle_client, args=(conn, addr)).start()

    def handle_client(self, conn, addr):
        """
        Handle the connection of a client
        :param conn The established connection with the current client
        :param addr The address of the current client
        """
        
        self.on_client_connection(conn, addr)
        
        while True:
            try: request:dict = self.receive(conn)
            except Exception as e: self.on_client_exception(e, addr); return
            
            result = self.on_client_request(conn, addr, request)
            
            # Check if the server must close the connection after client's request
            if result: break

        conn.close()
        self.on_client_disconnection(conn, addr)

    def handle_server_command(self):
        """
        Handle the reception of the server command.
        """
        
        while True:
            cmd = str(input())
            self.on_server_command(cmd)

    def receive(self, conn):
        """
        Receive a request from a specific and established connection.
        :param conn The connection to receive the request from
        :return The request, or none if there is no request
        """
        
        request_length = conn.recv(self.HEADER).decode(self.FORMAT)
        request_length = int(request_length)

        if request_length:
            request = str(conn.recv(request_length).decode(self.FORMAT))
            return eval(request)
        
        return None

    def send(self, conn, request_name, request_content):
        """
        Send a request to a specific and established connection.
        :param conn The connection to send the request on
        :param request The request to send
        """
        
        request = str({'name': request_name, 'content': request_content})
        
        message = request.encode(self.FORMAT)
        msg_length = len(message)
        send_length = str(msg_length).encode(self.FORMAT)
        send_length += b' ' * (self.HEADER - len(send_length))
        conn.send(send_length)
        conn.send(request.encode(self.FORMAT))

    def on_server_startup(self):
        """
        Method called when the server starts.
        """
        
        log(f"Starting on {self.SERVER}...")
    
    def on_server_shutdown(self):
        """
        Method called when the server shutdowns.
        """
        
        log("Server is shutdowning...")
    
    def on_server_command(self, cmd):
        """
        Method called when a server command is emitted.
        :param cmd The server command to execute
        """
        
        pass
    
    def on_client_connection(self, conn, addr):
        """
        Method called when a client is connected to the server.
        :param conn The client's connection
        :param addr The client's address
        """
        
        log(f"[{addr[0]}] is now connected to the server.")
    
    def on_client_request(self, conn, addr, request):
        """
        Process the client's request.
        Need to return true if the client need to be disconnected.
        :param conn The connection established with the client
        :param addr The client's address
        :param request The client's request
        :return True if the client need to be disconnected
        """
        
        if self.debug:
            debug(f"Request received from the client [{addr[0]}] on port {self.PORT}. Request's content: {request} .")
        
        if request == None:
            error(f"An error occurred with the client [{addr[0]}]. The client has not been disconnected properly!")
            return True
    
    def on_client_disconnection(self, conn, addr):
        """
        Method called when a client is disconnected from the server.
        :param conn The client's connection
        :param addr The client's address
        """
        
        log(f"[{addr[0]}] has been disconnected!")
    
    def on_client_exception(self, client_error, addr):
        """
        Method called when a client has triggered an error.
        :param client_error The error that occurred
        :param addr The client's address
        """
        
        if type(client_error) == ConnectionResetError:
            warn(f"[{addr[0]}] has lost the connection.")
            return
        
        error(f"An error occurred with the client [{addr[0]}]! {format_exc()}")
