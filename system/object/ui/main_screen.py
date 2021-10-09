from PyQt5.QtWidgets import *
from PyQt5 import uic
from time import sleep

class MainScreen(QMainWindow):
    """
    The main window of the Ulysse (v6) GUI.
    """
    
    def __init__(self, placeholder, on_send, on_close):
        super(MainScreen, self).__init__()
        uic.loadUi("./system/ui/main.ui", self)
        self.on_close = on_close
        
        self.interactions.ensureCursorVisible()
        self.user_input.setPlaceholderText(placeholder) 
    
        self.show()
        
        self.user_input.returnPressed.connect(on_send)
    
    def get_user_input(self) -> str:
        """
        Return the user input in the input line.
        :return the user input
        """
        
        user_input = self.user_input.text()
        self.user_input.setText("")
        self.user_input.setFocus()
        return str(user_input)
    
    def append(self, text):
        """
        Append text to the text edit.
        :param text the new text
        """
        
        self.interactions.append(text)
        sleep(0.001)
        self.interactions.verticalScrollBar().setValue(self.interactions.verticalScrollBar().maximum())
    
    def closeEvent(self, event):
        self.on_close()
        event.accept()