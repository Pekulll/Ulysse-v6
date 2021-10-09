from system.object.debug import log, warn, error, debug

class Command():
    def __init__(self, client):
        self.client = client
    
    def execute(self, content):
        if self.client.debug:
            debug(content)
        
        self.client.write(content)