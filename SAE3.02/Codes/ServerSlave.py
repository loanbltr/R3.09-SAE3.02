import sys, psutil, time
import socket
import subprocess
import threading

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
        while True:
            try:
                conn, address = self.slaveSocket.accept()
                print(f"Connexion établie avec {address}")
            except Exception as e:
                print(f"Erreur avec {address}: {e}")
                
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
                print(psutil.cpu_percent())
                time.sleep(5)
            except Exception as e:
                print(f"Erreur avec {address}: {e}")

    def traitementCode(self, conn, address):
        try:
            while self.running:
                code = self.receive(conn)
                #if not code:
                    #print(f"Connexion terminée par le client {address}.")
                    #break
                while code is None:
                    code = self.receive(conn)
                print(f"Code reçu de {address}: {code}")
                
                try:
                    # Sauvegarder le code reçu dans un fichier temporaire
                    with open("temp_code.py", "w") as temp_file:
                        temp_file.write(code)    
                    
                    # Exécuter le code en sous-processus
                    result = subprocess.run(
                        ["python3", "temp_code.py"],
                        text=True,
                        capture_output=True
                    )
                    if result.returncode == 0:
                        output = result.stdout
                    else:
                        output = f"Erreur d'exécution:\n{result.stderr}"
                    
                    # Envoyer le résultat au client
                    conn.send(output.encode())
                
                except Exception as exec_error:
                    error_message = f"Erreur d'exécution: {exec_error}"
                    conn.send(error_message.encode())
                
                print(f"Résultat envoyé à {address}: {output}")
        except Exception as e:
            print(f"Erreur avec {address}: {e}")

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
