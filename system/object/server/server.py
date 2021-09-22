from system.object.server.server_core import Server
from system.object.debug import log, warn, error, debug

from system.object.ai.recognizer import Recognizer
from system.object.ai.trainer import create_model

class UlysseServer(Server):
    def __init__(self, port=5050, debug=False):
        super().__init__(port, debug)
        #create_model(epochs=30000)
        self.recognizer = Recognizer()
    
    def on_client_request(self, conn, addr, request):
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

        if request['name'] == "speech":
            result, probability = self.recognizer.get_response(request['content'])
            
            if probability >= 0.8:
                self.send(conn, 'speech', f"[{probability}] {result}" if self.debug else f"{result}")
            else:
                self.send(conn, 'speech', f"Probability too low: {probability}.")
