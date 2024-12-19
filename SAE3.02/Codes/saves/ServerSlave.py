import sys, psutil, time, socket, subprocess, threading
from io import StringIO

class ServerSlave:
    def __init__(self, ip, port):
        self.ip = ip
        self.port = port

    def start(self):
        threadSocket = threading.Thread(target=self.startSocket)
        threadSocket.start()
        threadSocketCpu = threading.Thread(target=self.startSocketCpu)
        threadSocketCpu.start()

    def startSocket(self):
        self.slaveSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.slaveSocket.bind((self.ip, self.port))
        self.slaveSocket.listen(1)
        print(f"Serveur esclave démarré sur {self.ip}:{self.port}")
        threadAcceptMaster = threading.Thread(target=self.acceptMaster, args=([self.slaveSocket]))
        threadAcceptMaster.start()

    def acceptMaster(self, socketMaster):
        while True:
            try:
                conn, address = socketMaster.accept()
                print(f"Connection established with {address}")
                threadReceive = threading.Thread(target=self.receiveMaster, args=(conn, address))
                threadReceive.start()
            except Exception as e:
                print(f"Error accepting connection: {e}")

    def receiveMaster(self, conn, address):
        try:
            while True:
                data = conn.recv(1024)
                if not data:
                    print(f"Connection terminated by master {address}.")
                    break
                while data is None:
                   data = conn.recv(1024)
                print(f"Data received from {address}: {data}")
                code = self.traitementCode(data)
                conn.send(code.encode())
        except Exception as e:
            print(f"Error receiving data: {e}")
                
    def startSocketCpu(self):
        self.slaveSocketCpu = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.slaveSocketCpu.bind((self.ip, 11111))
        self.slaveSocketCpu.listen(1)
        print(f"Serveur esclave démarré sur {self.ip}:11111")
        while True:
            try:
                conn, address = self.slaveSocketCpu.accept()
                print(f"Connexion établie avec {address}")
                threadSendCpu = threading.Thread(target=self.sendCpu, args=(conn, address))
                threadSendCpu.start()
            except Exception as e:
                print(f"Erreur avec {address}: {e}")

    def sendCpu(self, conn, address):
        while True:
            try:
                conn.send(str(psutil.cpu_percent()).encode())
                time.sleep(5)
            except Exception as e:
                print(f"Erreur avec {address}: {e}")

    def traitementCode(self, data):
        try:
            # Préparer un espace pour exécuter le code
            local_vars = {}
            
            # Rediriger la sortie standard pour capturer les impressions
            old_stdout = sys.stdout
            sys.stdout = StringIO()

            # Exécuter le code dans le contexte local
            exec(data, {}, local_vars)

            # Récupérer les impressions (si présentes)
            output = sys.stdout.getvalue()
            
            # Récupérer les variables locales après exécution
            sys.stdout = old_stdout  # Restaurer stdout

            # S'il y a une sortie via `print`, on la retourne
            if output:
                return output.strip()
            
            # Sinon, retourner les variables locales si elles existent
            if local_vars:
                return str(local_vars)
            
            return "Code executed successfully without output."
        except Exception as e:
            sys.stdout = old_stdout  # Restaurer stdout en cas d'erreur
            return f"Erreur d'exécution du code: {e}"

    def stop(self):
        self.running = False
        if self.slaveSocket:
            self.slaveSocket.close()
        print("Serveur arrêté.")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Utilisation : python ServerSlave.py <port>")
        sys.exit(1)

    ip = str(socket.gethostbyname(socket.gethostname()))
    port = int(sys.argv[1])

    serverSlave = ServerSlave(ip, port)
    serverSlave.start()
