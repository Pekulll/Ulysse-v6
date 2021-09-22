from PyQt5.QtWidgets import *
from PyQt5 import uic

class LoadingScreen(QMainWindow):
    def __init__(self):
        super(LoadingScreen, self).__init__()
        uic.loadUi("./system/ui/loading.ui", self)
        self.show()
    
    def change_sys(self, sys):
        """
        Change the system text
        :param sys The modified text
        """
        
        self.loading_system.setText(sys)
    
    def change_lang(self, lang):
        """
        Change the langage text
        :param lang The modified text
        """
        
        self.loading_langages.setText(lang)
        
    def change_serv(self, serv):
        """
        Change the server statut text
        :param serv The modified text
        """
        
        self.connecting.setText(serv)
        
    def change_auth(self, auth):
        """
        Change the authentification text
        :param auth The modified text
        """
        
        self.authentification.setText(auth)