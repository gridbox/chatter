import socket
import threading
import json

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
        try:
            while True:
                message = connection.recv(2048).decode('utf-8')
                # Decode
                decoded = json.loads(message)

                # Keep track of clients
                if decoded["type"] == "connect":
                    self.clients[decoded["client_id"]] = connection
                
                print(message)
                connection.sendall(message)
        except:
            connection.close()

if __name__ == '__main__':
    chatter = ChatterServer()
    chatter.run()
    