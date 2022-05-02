import socket
import threading
import json
from client import Client

class ChatterServer:
    """A class to run the Chatter server"""

    def __init__(self):
        self.socket = socket.socket()
        self.host = '127.0.0.1'
        self.port = 10000
        self.clients = {}


    def run(self):
        # Start socket and bind
        try:
            self.socket.bind((self.host, self.port))
            print('Chatter server is listening...')
            self.socket.listen(5)

            # Process client connections
            while True:
                client, address = self.socket.accept()
                print('Connected to: ' + address[0] + ':' + str(address[1]))
                threading.Thread(target=self.on_client_connect, args=(client,), daemon=True).start()

        except socket.error as e:
            print(str(e))
        
    def on_client_connect(self, connection):
        
            while True:
                # Decode
                message = connection.recv(2048).decode('utf-8')
                decoded_message = json.loads(message)

                # Keep track of clients
                if decoded_message["type"] == "connect":
                    self.clients[decoded_message["client_id"]] = Client(decoded_message["client_id"], decoded_message["display_name"], connection)
                    # Send updated friend list to all OTHER clients
                    friend_list = {client_id: client.display_name for client_id, client in self.clients.items()}
                    friend_message = {"type": "friends", "friends": friend_list}
                    encoded_message = json.dumps(friend_message, ensure_ascii=False)
                    self.send_all_clients(decoded_message.get("client_id"), encoded_message, True)
                
                if decoded_message["type"] == "room":
                    # Send to all OTHER clients
                    self.send_all_clients(decoded_message.get("client_id"), message)

    def send_all_clients(self, from_client_id, message, send_self = False):
        for client in self.clients.values():
            if send_self or client.id != from_client_id:
                client.connection.sendall(message.encode('utf-8'))


if __name__ == '__main__':
    chatter = ChatterServer()
    chatter.run()
    