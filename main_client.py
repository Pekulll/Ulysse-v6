from system.object.package import install_package, verify_package
import os

def start():
    """
    Start the Ulysse client after checking for packages to install.
    """
    
    missing_packages = verify_package(["PyAudio", "SpeechRecognition", "pyttsx3", "PyQt5"])

    if len(missing_packages) > 0:
        succeed = install_package(missing_packages)
        
        if not succeed:
            os.system("pause")
            return

    from system.object.server.client import UlysseClient
    client = UlysseClient("192.168.1.24", 1509, True)

    if client.connect():
        client.run()


if __name__ == '__main__':
    os.system("")
    start()