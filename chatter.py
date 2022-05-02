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
        self.window = sg.Window(f"Chatter - {self.settings.display_name}", self.layout)
        self.clientSocket = socket.socket()

        # Friend list
        self.friends = {}

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
            connect_message = json.dumps({"type": "connect", "client_id": self.settings.client_id, "display_name": self.settings.display_name}, ensure_ascii=False).encode("utf8")
            self.clientSocket.send(connect_message)
            read_from_socket = True
            while read_from_socket:
                res = self.clientSocket.recv(2048)
                if len(res) > 0:
                     # Decode
                    decoded_message = json.loads(res.decode('utf-8'))

                    if decoded_message["type"] == "room":
                        window.write_event_value('##CLIENT_HANDLER##', decoded_message)
                    elif decoded_message["type"] == "friends":
                        self.friends = decoded_message["friends"]
                else:
                    read_from_socket = False
            self.clientSocket.close()
        except OSError as e:
            print(str(e))
            self.clientSocket.close()


    def send(self, values):
        message = values['##MESSAGE##']
        if message:
            # Encode
            encoded_message = json.dumps({"type": "room", "client_id": self.settings.client_id, "room_id": self.settings.room_id, "text": message}, ensure_ascii=False).encode("utf8")
            # Send message
            self.clientSocket.send(encoded_message)
            # Update chat box
            self.window["##CHATBOX##"].print(f'(self): {message}')
    
    def receive(self, values):
        message = values['##CLIENT_HANDLER##']
        if message:
            self.window["##CHATBOX##"].print(f'({self.friends[message["client_id"]]}): {message["text"]}')

if __name__ == '__main__':
    chatter = Chatter()
    chatter.run()