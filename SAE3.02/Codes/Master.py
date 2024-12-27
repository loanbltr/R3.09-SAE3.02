import threading
import socket
import sys

class ServerMaster:
    def __init__(self, ip):
        self.ip = ip

        self.socketClient = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socketClient.bind((self.ip, 11111))
        self.socketClient.listen()

        self.socketSlave = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socketSlave.bind((self.ip, 22222))
        self.socketSlave.listen()

        self.socketSlaveCpu = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socketSlaveCpu.bind((self.ip, 33333))
        self.socketSlaveCpu.listen()

        self.listSlave = []
        self.listClient = []

        self.slaveId = []
        self.cpuId = []
        self.SlaveCpu = []

    def startMaster(self):
        threading.Thread(target=self.acceptClient).start()
        threading.Thread(target=self.acceptSlaveCpu).start()
        threading.Thread(target=self.acceptSlave).start()

    def acceptClient(self):
        while True:
            try:
                conn, address = self.socketClient.accept()
                print(f"Connection setup with client : {address}")
                self.listClient.append({"connexion": conn, "address": address})
                threading.Thread(target=self.keepClient, args=(conn, address), daemon=True).start()
            except Exception as e:
                print(f"Error of connection with client : {e}")

    def keepClient(self, conn, address):
        while True:
            try:
                data = conn.recv(1024).decode("utf-8")
                if not data:
                    print(f"Client {address} disconnected.")
                    conn.close()
                    break

                print(f"Received from client {address}: {data}")
                data = f"{address[1]}�{data}"
                langageCode = data.split("�")[1].split("|")[1]
                slave = self.getAvailableSlave(langageCode)

                if slave:
                    slave_conn = slave["connexion"]
                    slave_conn.send(data.encode("utf-8"))
                    print(f"Message sent to slave: {data}")
                else:
                    print("No slave available.")
                    conn.send("No slave available".encode("utf-8"))

            except Exception as e:
                print(f"Error keep client {address}: {e}")
                conn.close()
                break

    def acceptSlave(self):
        while True:
            try:
                conn, address = self.socketSlave.accept()
                print(f"Connection setup with slave: {address}")
                data = conn.recv(1024).decode("utf-8")
                self.slaveId.append({"connexion": conn, "address": address, "id": data.split("�")[0], "langages": data.split("�")[1]})
                #self.listSlave.append({"connexion": conn, "address": address, "state": "True"})
                threading.Thread(target=self.keepSlave, args=(conn, address)).start()
            except Exception as e:
                print(f"Error of connection with slave: {e}")

    def acceptSlaveCpu(self):
        while True:
            try:
                conn, address = self.socketSlaveCpu.accept()
                print(f"Connection setup with slave: {address}")
                threading.Thread(target=self.keepSlaveCpu, args=(conn, address)).start()
            except Exception as e:
                print(f"Error of connection with slave: {e}")

    def keepSlaveCpu(self, conn, address):
        while True:
            try:
                data = conn.recv(1024).decode("utf-8")
                if not data:
                    print(f"Slave {address} disconnected.")
                    conn.close()
                    self.removeSlave(conn)
                    break
                else:
                    data = data.split("�")
                    if len(self.cpuId) != 0:
                        for slave in self.cpuId:
                            if slave["id"] == data[0]:
                                slave["state"] = data[1]
                                slave["cpu"] = data[2]
                            else:
                                self.cpuId.append({"id": data[0], "state": data[1], "cpu": data[2]})
                    else:
                        self.cpuId.append({"id": data[0], "state": data[1], "cpu": data[2]})
                    self.updateListSlaveCpu()
                #print(f"Received from slave {address}: {data}")
            except Exception as e:
                print(f"Error keep slave {address}: {e}")
                conn.close()
                break

    def keepSlave(self, conn, address):
        while True:
            try:
                data = conn.recv(1024).decode("utf-8")
                if not data:
                    print(f"Slave {address} disconnected.")
                    conn.close()
                    self.removeSlave(conn)
                    break
                else:
                    print(f"Received from slave {address}: {data}")
                    port, data = data.split("�")
                    client = [client for client in self.listClient if client["address"][1] == int(port)][0]
                    client_conn = client["connexion"]
                    result, data = data.split("|")
                    client_conn.send(data.encode("utf-8"))
            except Exception as e:
                print(f"Error keep slave {address}: {e}")
                conn.close()
                self.removeSlave(conn)
                break

    def updateListSlaveCpu(self):
        for conn in self.slaveId:
            for cpu in self.cpuId:
                if conn["id"] == cpu["id"]:
                    if len(self.SlaveCpu) != 0:
                        for final in self.SlaveCpu:
                            if final["connexion"] == conn["connexion"]:
                                final["state"] = cpu["state"]
                                final["cpu"] = cpu["cpu"]
                                break
                            else:
                                self.SlaveCpu.append({"connexion": conn["connexion"], "state": cpu["state"], "cpu": cpu["cpu"], "langages": conn["langages"]})
                    else:
                        self.SlaveCpu.append({"connexion": conn["connexion"], "state": cpu["state"], "cpu": cpu["cpu"], "langages": conn["langages"]})

    def getAvailableSlave(self, langage):
        langage = str(langage)
        if langage.split(".")[1] == "py":
            langageName = "python"
        elif langage.split(".")[1] == "java":
            langageName = "java"
        elif langage.split(".")[1] == "c":
            langageName = "c"
        else:
            langageName = None
        for slave in self.SlaveCpu:
            print(slave["langages"])
            code = slave["langages"].split("/")
            for langageCpu in code:
                if slave["state"] == "True" and langageName == langageCpu:
                    return slave
        return None

    def removeSlave(self, conn):
        #self.listSlave = [slave for slave in self.listSlave if slave["connexion"] != conn]
        for slave in self.slaveId:
            if slave["connexion"] == conn:
                for cpu in self.cpuId:
                    if slave["id"] == cpu["id"]:
                        self.cpuId.remove(cpu)
                self.slaveId.remove(slave)
        for slave in self.SlaveCpu:
            if slave["connexion"] == conn:
                self.SlaveCpu.remove(slave)
        self.slaveId = []
        self.cpuId = []
        self.SlaveCpu = []

    def stop(self):
        self.socketClient.close()
        self.socketSlave.close()
        print("Server stopped.")

if __name__ == '__main__':
    if len(sys.argv) != 1:
        print("Usage: python ServerMaster.py")
        sys.exit(1)

    ip = str(socket.gethostbyname(socket.gethostname()))

    server = ServerMaster(ip)

    try:
        server.startMaster()
        print("Server running... Press Ctrl+C to stop.")
        while True:
            pass
    except KeyboardInterrupt:
        print("\nShutting down server.")
        server.stop()
        sys.exit(0)