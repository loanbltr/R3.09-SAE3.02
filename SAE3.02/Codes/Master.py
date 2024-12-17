import threading, socket, sys

class ServerMaster:
    def __init__(self, ip, portClient, configSlave):
        self.ip = ip
        self.portClient = portClient
        self.configSlave = configSlave
        self.listSlave = []
        self.listSlaveCpu = []

    def startMaster(self):
        socketMaster = socket.socket()
        socketMaster.bind((self.ip, self.portClient))
        socketMaster.listen()
        print(f"Master server started on {self.ip}:{self.portClient}")
        threadAcceptClient = threading.Thread(target=self.acceptClient, args=([socketMaster]))
        threadAcceptClient.start()
        threadConnectConfig = threading.Thread(target=self.connectConfig)
        threadConnectConfig.start()

    def acceptClient(self, socketMaster):
        while True:
            try:
                conn, address = socketMaster.accept()
                print(f"Connection established with {address}")
                threadReceive = threading.Thread(target=self.receiveSlave, args=(conn, address))
                threadReceive.start()
            except Exception as e:
                print(f"Error accepting connection: {e}")
            
    def receiveSlave(self, conn, address):
        try:
            while True:
                data = conn.recv(1024)
                if not data:
                    print(f"Connection terminated by client {address}.")
                    break
                while data is None:
                   data = conn.recv(1024)
                print(f"Data received from {address}: {data}")

        except Exception as e:
            print(f"Error receiving data: {e}")
        
    def connectConfig(self):
        try:
            self.listSlave.clear()
            with open(self.configSlave, 'r') as file:
                serv = 1
                for line in file:
                    line = line.strip()
                    if not line:
                        continue
                    print(f"Lecture de la ligne : {line}")
                    try:
                        line = line.split(':')
                        socketMaster = socket.socket()
                        socketMaster.connect((line[0], int(line[1])))
                        self.listSlave.append({"socket": socketMaster, "ip":line[0], "port": line[1]})
                        print(f"Connection established with slave {line[0]}:{line[1]}")
                        threadReceive = threading.Thread(target=self.receive, args=(socketMaster,))
                        threadReceive.start()
                    except Exception as e:
                        print(f"Error connecting to slave {line[0]}:{line[1]}: {e}")
                    try:
                        socketMastercpu = socket.socket()
                        socketMastercpu.connect((line[0], 11111 * serv))
                        self.listSlaveCpu.append({"socket": socketMastercpu, "ip":line[0], "port": 11111 * serv})
                        print(f"Connection established with slave {line[0]}:{11111 * serv}")
                        threadReceive = threading.Thread(target=self.receive, args=(socketMastercpu,))
                        threadReceive.start()
                        serv += 1
                    except Exception as e:
                        print(f"Error connecting to slave {line[0]}:{11111 * serv}: {e}")
                    
        except Exception as e:
            print(f"An error occurred while reading the configuration file: {e}")

    def receive(self, socket):
        while True:
            try:
                data = socket.recv(1024)
                print(data.decode())
            except Exception as e:
                print(f"Error receiving data: {e}")
                return None

    def stop(self):
        self.running = False
        self.slaveSocket.close()
        print("Slave server stopped.")

if __name__ == '__main__':
    if len(sys.argv) != 3:
        print("Use : python ServerMaster.py <fichier.txt> <port>")
        sys.exit(1)

    ip = str(socket.gethostbyname(socket.gethostname()))
    configSlave = sys.argv[1]
    portClient = int(sys.argv[2])

    server = ServerMaster(ip, portClient, configSlave)
    try:
        server.startMaster()
    except KeyboardInterrupt:
        print("\nServer stopped.")
        server.stop()
        sys.exit(0)