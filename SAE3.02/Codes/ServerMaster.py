import sys
import socket
import threading
import os
import subprocess
import random
import time

class ServerMaster:
    def __init__(self, ip="localhost", port=8080, max_clients=5):
        self.ip = ip
        self.port = port
        self.max_clients = max_clients
        self.serverMasterSocket = None
        self.running = False
        self.slave = []
        self.portSlaveInUse = []

    def start(self):
        self.serverMasterThread = threading.Thread(target=self.serverMaster)
        self.serverMasterThread.start()
        self.startServerSlave()

    def serverMaster(self):
        global data
        try:
            self.serverMasterSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.serverMasterSocket.bind((self.ip, self.port))
            self.serverMasterSocket.listen(self.max_clients)
            self.running = True
            print(f"Serveur démarré sur {self.ip}:{self.port}. En attente de connexions...")
            while self.running:
                conn, address = self.serverMasterSocket.accept()
                print(f"Connexion établie avec {address}")
                data = conn.recv(1024).decode()
                self.sendSlave(data)
        except Exception as e:
            print(f"Erreur : {e}")
            self.stop()

    def findSlave(self, portSlave):
        for slave in self.slave:
            if slave["port"] == portSlave:
                return slave
        return None

    def startServerSlave(self):
        portSlave = random.randint(49152, 65535)
        if portSlave not in self.portSlaveInUse:
            self.portSlaveInUse.append(portSlave)
            print(f"Port libre trouvé : {portSlave}")
            self.slave.append({
                "ip": self.ip,
                "port": portSlave
            })
            subprocess.Popen(["start", "cmd", "/k", "python", "ServerSlave.py", self.ip, str(portSlave)], shell=True)
        else:
            time.sleep(1)
            self.startServerSlave()

    def sendSlave(self, data):
        slaveSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        slaveSocket.connect((self.slave[0]["ip"], self.slave[0]["port"]))
        slaveSocket.send(data.encode())

    def stop(self):
        self.running = False
        if self.serverMasterSocket:
            self.serverMasterSocket.close()
            self.serverMasterSocket = None
        print("Serveur arrêté.")

if __name__ == '__main__':
    server = ServerMaster()
    try:
        server.start()
    except KeyboardInterrupt:
        print("\nArrêt du serveur...")
        server.stop()
        sys.exit(0)
