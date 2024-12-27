import sys, psutil, time, socket, subprocess, threading, random, os, argparse
from io import StringIO

class ServerSlave:
    def __init__(self, ipMaster, langages, maxCpu=100, nbCodesMax=999):
        self.ipMaster = ipMaster
        self.maxCpu = maxCpu
        self.nbCodesMax = nbCodesMax
        self.nbCodesNow = 0
        self.langages = langages

        self.socketMaster = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socketMaster.connect((self.ipMaster, 22222))

        self.socketMasterCpu = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socketMasterCpu.connect((self.ipMaster, 33333))

        self.disponible = True
        self.id = str(random.randint(0, 10000))
        try:
            data = f"{self.id}�{self.langages}"
            self.socketMaster.send(data.encode("utf-8"))
        except Exception as e:
            print(f"Error sending ID to master: {e}")

    def start(self):
        threading.Thread(target=self.receiveMaster).start()
        threading.Thread(target=self.stateCpu).start()
        #threading.Thread(target=self.sendMaster).start()

    def receiveMaster(self):
        while True:
            try:
                data = self.socketMaster.recv(1024).decode("utf-8")
                print(f"Received data from master: {data}")
                if data == None:
                    break
                else:
                    threading.Thread(target=self.traitementMessage, args=(data,)).start()
            except Exception as e:
                print(f"Error receiving data from master: {e}")
                break

    def sendMaster(self, data):
        if data == 'stateSlave':
            while True:
                try:
                    info = f'stateSlave|{self.disponible}'
                    self.socketMaster.send(info.encode("utf-8"))
                    print(f"Message sent to master: {info}")
                    time.sleep(5)
                except Exception as e:
                    print(f"Error sending data to master: {e}")
                    break
        else:
            try:
                self.socketMaster.send(data.encode("utf-8"))
                print(f"Message sent to master: {data}")
            except Exception as e:
                print(f"Error sending data to master: {e}")
            
    def stateCpu(self):
        psutil.cpu_percent(interval=None)
        while True:
            try:
                cpu_usage = psutil.cpu_percent(interval=1)
                if cpu_usage > self.maxCpu or self.nbCodesNow > self.nbCodesMax:
                    self.disponible = False
                else:
                    self.disponible = True
                self.socketMasterCpu.send(f"{self.id}�{self.disponible}�{str(cpu_usage)}".encode("utf-8"))
                time.sleep(5)
            except Exception as e:
                print(f"Error sending CPU usage to master: {e}")

    def traitementMessage(self, data):
        try:
            if data.split("|")[1].split(".")[1] == "py":
                self.traitementPython(data)
            if data.split("|")[1].split(".")[1] == "java":
                self.traitementJava(data)
        except Exception as e:
            print(f"Error processing message: {e}")

    def traitementJava(self, data):
        nameTmp = data.split("|")[1].split(".")[0] + str(random.randint(0, 10000)) + ".java"
        try:
            with open(f'fileTemp/{nameTmp}', "w", encoding='utf-8') as f:
                f.write(data.split("|")[2])
            with open(f"fileTemp/{nameTmp}", "r") as fichier:
                lignes = fichier.readlines()

            for i in range(len(lignes)):
                if lignes[i].startswith("public class"):
                    mots = lignes[i].split(" ")
                    mots[2] = nameTmp.split(".")[0]
                    lignes[i] = " ".join(mots) + "\n"

            with open(f"fileTemp/{nameTmp}", "w") as fichier:
                fichier.writelines(lignes)
        except:
            print("Error during writing file")
        #compile_result = subprocess.run(["java", f'fileTemp/{nameTmp}'], capture_output=True, text=True)
        #if compile_result.returncode != 0:
        result = subprocess.run(["java", f'fileTemp/{nameTmp}'], capture_output=True, text=True)
        if result.returncode == 0:
            self.sendMaster(f"{data.split("�")[0]}�result|{result.stdout}")
        else:
            self.sendMaster(f"{data.split("�")[0]}�result|{result.stderr}")
        os.remove(f'fileTemp/{nameTmp}')
        

    def traitementPython(self, data):
        nameTmp = data.split("|")[1].split(".")[0] + str(random.randint(0, 1000)) + ".py"
        try:
            with open(f'fileTemp/{nameTmp}', "w", encoding='utf-8') as f:
                f.write(data.split("|")[2])
        except:
            print("Error during writing file")
        try:
            result = subprocess.run(['python', f'fileTemp/{nameTmp}'], capture_output=True, text=False)
        except Exception as e:
            self.sendMaster(e)
        else:
            if result.returncode == 0:
                self.sendMaster(f"{data.split("�")[0]}�result|{result.stdout.decode('utf-8')}")
            else:
                self.sendMaster(f"{data.split("�")[0]}�result|{result.stderr.decode('utf-8')}")
        os.remove(f'fileTemp/{nameTmp}')

    def stop(self):
        self.socketMaster.close()
        #self.socketMasterCpu.close()
        print("Server slave stopped.")

if __name__ == "__main__":
    """parser = argparse.ArgumentParser(description="Permet de définir les caractéristiques du serveur esclave")
    parser.add_argument("-local", "--localhost", help="Si cette option est activée le serveur sera en localhost", type=str)
    parser.add_argument("-pm", "--portMaster", help="Permet de définir le port sur lequel se connectera le serveur slave (par défaut: 22222)", type=int)

    args = parser.parse_args()
    resultats = []

    if args.localhost:
        ip = "127.0.0.1"
    else:
        ip = str(socket.gethostbyname(socket.gethostname()))

    if args.portMaster:
        portMaster = int(args.portMaster)
    else:
        portMaster = 22222"""
                                  
    serverSlave = ServerSlave("192.168.0.20", "python/java/c", 80, 3)
    serverSlave.start()
    
    