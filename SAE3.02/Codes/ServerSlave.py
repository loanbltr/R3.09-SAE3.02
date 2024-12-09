import sys
import socket
import os

class ServerSlave:
    def __init__(self, ip="localhost", port=None):
        self.ip = ip
        self.port = port
        self.export = False
        self.serverSlave_socket = None

    def start(self):
        server_socket = socket.socket()
        server_socket.bind((self.ip, self.port))
        server_socket.listen(1)
        self.export = True
        print(f"Serveur démarré sur {self.ip}:{self.port}. En attente de connexions...")
        while True:
            conn, address = server_socket.accept()
            print(f"Connexion établie avec {address}")
            data = conn.recv(1024).decode()
            exec(data)

    def stop(self):
        self.running = False
        if self.serverSlaveSocket:
            self.serverSlaveSocket.close()
            self.serverSlaveSocket = None
            self.export = True
        print("Serveur arrêté.")

if __name__ == "__main__":
    serverSlave = ServerSlave(sys.argv[1], int(sys.argv[2]))
    serverSlave.start()
