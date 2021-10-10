from system.object.debug import log, warn, error, debug
from system.command.command import Command

class AssistantCommand(Command):
    """
    The 'repeat' command.
    The assistant will simply repeat what the user says.
    """
    
    def __init__(self, client):
        super().__init__(client)
    
    def execute(self, content):
        if self.client.debug:
            debug(content)
        
        self.client.write(content)