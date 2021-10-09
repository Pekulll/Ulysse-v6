from os import system

class Console():
    """
    Create a Console object to send os command
    """
    
    def __init__(self):
        import platform
        self.platform = platform.system()
        
        self.commands = {
            "Linux": {
                'clear': 'clear'
            },
            "Windows": {
                'clear': 'cls'
            }
        }
    
    def execute_cmd(self, cmd):
        """
        Execute a command in the console, depending on the OS
        - clear: clear the console output
        """
        
        system(self.commands[self.platform].get(cmd))