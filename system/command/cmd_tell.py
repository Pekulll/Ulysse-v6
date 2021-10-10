from system.object.debug import log, warn, error, debug
from system.command.command import Command

class AssistantCommand(Command):
    """
    The 'tell' command
    """
    
    def __init__(self, client):
        super().__init__(client)
    
    def execute(self, content):
        if self.client.debug:
            debug(content)
    
        contact_name = content.split(' ')[0]
        house_name = None
        room_name = None
        
        for contact in self.client.contacts:
            if contact['contact_name'].lower() == contact_name.lower():
                house_name = contact['house_name']
                room_name = contact['room_name']
                break
        
        if house_name == None or room_name == None:
            self.client.write("Contact not found!")
            return
        
        server_request = {
            'from': {'house_name': self.client.HOUSE, 'room_name': self.client.ROOM},
            'to': {'house_name': house_name, 'room_name': room_name},
            'message': " ".join(content.split(' ')[1:])
        }
        
        self.client.send("tell", str(server_request))