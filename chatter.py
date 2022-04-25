import PySimpleGUI as sg
import socket
import threading
import json
from settings import Settings

class Chatter:
    def __init__(self):
        self.settings = Settings()

        # Define the window's contents
        self.layout = [
            [sg.Multiline(key="##CHATBOX##", size=(100,25), disabled=True),],
            [sg.Input(key='##MESSAGE##', size=100, do_not_clear=False), sg.Button('Send')],
        ]

        # Create the window
        self.window = sg.Window('Chatter', self.layout)
        self.clientSocket = socket.socket()

    def run(self):
        # Connect to server
        threading.Thread(target=self.client_handler, args=(self.window,), daemon=True).start()

        # Display and interact with the Window using an Event Loop
        while True:
            event, values = self.window.read()
            # See if user wants to quit or window was closed
            if event == sg.WINDOW_CLOSED or event == 'Quit':
                break
            elif event == 'Send':
                self.send(values)
            elif event == '##CLIENT_HANDLER##':
                self.receive(values)

        # Finish up by removing from the screen
        self.window.close()

    def client_handler(self, window):
        print('Connecting to server...')

        try:
            self.clientSocket.connect((self.settings.host, self.settings.port))
            connect_message = json.dumps({"type": "connect", "client_id": self.settings.client_id}, ensure_ascii=False).encode("utf8")
            self.clientSocket.send(connect_message)
            while True:
                res = self.clientSocket.recv(1024)
                print(res.decode('utf-8'))
                window.write_event_value('##CLIENT_HANDLER##', res.decode('utf-8'))
        except OSError as e:
            print(str(e))
            self.clientSocket.close()


    def send(self, values):
        message = values['##MESSAGE##']
        if message:
            # Encode
            encoded = json.dumps({"type": "message", "to_client_id": self.settings.client_id, "text": message}, ensure_ascii=False).encode("utf8")
            # Send message
            self.clientSocket.send(encoded)
            # Update chat box
            self.window["##CHATBOX##"].print(message)
    
    def receive(self, values):
        message = values['##CLIENT_HANDLER##']
        if message:
            # Decode
            decoded = json.loads(message)
            print(decoded)
            # Update chat box
            if decoded["type"] == "message":
                self.window["##CHATBOX##"].print(decoded["text"])

if __name__ == '__main__':
    chatter = Chatter()
    chatter.run()