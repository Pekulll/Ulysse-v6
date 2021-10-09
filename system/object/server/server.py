from system.object.server.server_core import Server
from system.object.debug import log, warn, error, debug

from system.object.ai.recognizer import Recognizer
from system.object.ai.trainer import create_model

from system.object.console import Console

class UlysseServer(Server):
    def __init__(self, port=5050, debug=False):
        super().__init__(port, debug)
        #create_model(epochs=30000)
        self.recognizer = Recognizer()
        self.console = Console()
        
        self.console.execute_cmd("clear")
    
    def on_client_request(self, conn, addr, request) -> bool:
        """
        Process the client's request.
        Need to return true if the client need to be disconnected.
        :param conn The connection established with the client
        :param addr The client's address
        :param request The client's request
        :return True if the client need to be disconnected
        """

        if super().on_client_request(conn, addr, request):
            return True

        if request['name'] == "disconnect":
            return True
        
        MIN_PROBABILITY = 0.8
        
        if request['name'] == "speech":
            tag, result, probability = self.recognizer.get_response(request['content'], True)
            
            if not tag == None and 'cmd_' in tag:
                result = result[1:] if result.startswith(" ") else result
                self.send(conn, tag, result)
                return False
            
            tag, result, probability = self.recognizer.get_response(request['content'])
            
            if probability < MIN_PROBABILITY:
                if self.debug: self.send(conn, 'speech', f"Probability too low: {probability}.")
                return False
            
            self.send(conn, 'speech', f"[{probability}] {result}")
            return False
