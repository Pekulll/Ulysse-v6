from system.object.debug import debug

class Command():
    """
    A basic command
    """
    
    def __init__(self, client):
        self.client = client
        
    def execute(self, content):
        """
        Execute the command according to the command's content
        """
        
        debug("Command had been executed!")