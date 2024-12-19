import threading, socket, sys

class ServerMaster:
    def __init__(self, ip):
        self.ip = ip

        self.socketClient = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socketClient.bind((self.ip, 11111))
        self.socketClient.listen()
        
        self.socketSlave = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socketSlave.bind((self.ip, 22222))
        self.socketSlave.listen()

        self.listSlave = []

    def startMaster(self):
        threading.Thread(target=self.acceptClient).start()
        threading.Thread(target=self.acceptSlave).start()

    def acceptClient(self):
        while True:
            try:
                conn, address = self.socketClient.accept()
                print(f"Connection established with {address}")
                threading.Thread(target=self.receiveClient, args=(conn, address)).start()
            except Exception as e:
                print(f"Error accepting connection: {e}")

    def receiveClient(self, conn, address):
        while True:
            try:
                data = conn.recv(1024).decode("utf-8")
                if data == None:
                    break
                else:
                    print(f"Received data from client {address}: {data}")
                    #self.listSlave[0].send(data.encode("utf-8"))
                    #threading.Thread(target=self.loadBalancing, args=(conn, address, data)).start()
                    try:  
                        print(self.listSlave)
                        for slave in self.listSlave:
                            if slave["state"] == 'True':
                                slave["connexion"].send(data.encode("utf-8"))
                                print(f"Message sent to slave {slave['address']}: {data}")
                                threading.Thread(target=self.receiveSlave, args=(slave['connexion'], slave['address'], conn, address, data)).start()
                                break
                            else:
                                print("No slave available")
                    except Exception as e:
                        print(f"Error sending data to slave {slave['address']}: {e}")
            except Exception as e:
                print(f"Error receiving data from client or send to slave {address}: {e}")
                break

    def acceptSlave(self):
        while True:
            try:
                conn, address = self.socketSlave.accept()
                print(f"Connection established with {address}")
                threading.Thread(target=self.receiveSlave, args=(conn, address)).start()
            except Exception as e:
                print(f"Error accepting connection: {e}")

    def receiveSlave(self, connSlave, addressSlave, connClient=None, addressClient=None, code=None):
        try:
            if code == None:
                while True:
                    try:
                        data = connSlave.recv(1024).decode("utf-8")
                        if data == None:
                            break
                        if data.split("|")[0] == "stateSlave":
                            print(f"{connSlave}: {data.split("|")[1]}")
                            if len(self.listSlave) == 0:
                                self.listSlave.append({"connexion": connSlave, "address": addressSlave, "state": data.split("|")[1]})
                            for slave in self.listSlave:
                                if slave["connexion"] == connSlave and slave["address"] == addressSlave:
                                    slave["state"] = data.split("|")[1]
                                    break
                                else:
                                    self.listSlave.append({"connexion": connSlave, "address": addressSlave, "state": data.split("|")[1]})
                                    break
                                    #self.listSlave.append({"connexion": connSlave, "address": addressSlave, "state": data.split("|")[1]})
                    except Exception as e:
                        print(f"Error receiving data from slave {addressSlave}: {e}")
                        break
            else:
                if code.split("|")[0] == "code":
                    print(f"{connClient}: {code.split("|")[0]}")
                    print(code)
                    try:
                        connClient.send(code.encode("utf-8"))
                        #print(f"Message sent to client {addressClient}: {data}")
                    except Exception as e:
                        print(f"Error sending data to client {addressClient}: {e}")
        except Exception as e:
            print(f"Error receiving data from slave {addressSlave}: {e}")
    
    def sendSlave(self, connSlave, data):
        try:
            connSlave.send(data.encode("utf-8"))
            print(f"Message sent to slave: {data}")
        except Exception as e:
            print(f"Error sending data to slave: {e}")

    """def loadBalancing(self, connClient, addressClient, data):
        if len(self.listSlave) == 0:
            print("No slave available.")
        else:
            for slave in self.listSlave:
                if slave["state"] == "True":
                    slave["connexion"].send(data.encode("utf-8"))
                    print(f"Message sent to slave {slave['address']}: {data}")
                    threading.Thread(target=self.receiveSlave, args=(connClient, addressClient, slave['connexion'], slave['address'])).start()
                    break
                else:
                    print("No slave available")"""

    def stop(self):
        self.running = False
        self.slaveSocket.close()
        print("Slave server stopped.")

if __name__ == '__main__':
    if len(sys.argv) != 1:
        print("Use : python ServerMaster.py")
        sys.exit(1)

    ip = str(socket.gethostbyname(socket.gethostname()))

    server = ServerMaster(ip)

    try:
        server.startMaster()
    except KeyboardInterrupt:
        print("\nServer stopped.")
        server.stop()
        sys.exit(0)