import sys, psutil, time, socket, subprocess, threading, random
from io import StringIO

class ServerSlave:
    def __init__(self, ipMaster):
        self.ipMaster = ipMaster
        self.socketMaster = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socketMaster.connect((self.ipMaster, 22222))
        self.disponible = True

    def start(self):
        threading.Thread(target=self.receiveMaster).start()
        threading.Thread(target=self.stateCpu).start()
        #threading.Thread(target=self.sendMaster).start()

    def receiveMaster(self):
        while True:
            try:
                data = self.socketMaster.recv(1024).decode("utf-8")
                print(f"Received data from master: {data}")
                result = self.traitementMessage(data)
                result += f"code|{result}"
                print(result)
                self.sendMaster(result)
            except Exception as e:
                print(f"Error receiving data from master: {e}")
                break

    def sendMaster(self, data):
        while True:
            if data == 'stateSlave':
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
                    info = f'code|{data}'
                    self.socketMaster.send(info.encode("utf-8"))
                    print(f"Message sent to master: {data}")
                except Exception as e:
                    print(f"Error sending data to master: {e}")
                    break
            
    def stateCpu(self):
        while True:
            try:
                if psutil.cpu_percent() > 80.0:
                    self.disponible = False
                else:
                    self.disponible = True
                self.sendMaster('stateSlave')
            except Exception as e:
                print(f"Error sending CPU usage to master: {e}")

    def traitementMessage(self, data):
        try:
            if data.split("|")[1].split(".")[1] == "py":
                nameTmp = data.split("|")[1].split(".")[0] + str(random.randint(0, 1000)) + ".py"
                try:
                    with open(f'fileTemp/{nameTmp}', "w", encoding='utf-8') as f:
                        f.write(data.split("|")[1])
                except:
                    print("Erreur lors de l'écriture du fichier")
                result = subprocess.run(['python', f'fileTemp/{nameTmp}'], capture_output=True, text=True)
                return result.stdout.strip() if result.returncode == 0 else result.stderr.strip()
        except Exception as e:
            print(f"Error processing message: {e}")

    def stop(self):
        self.socketMaster.close()
        self.socketMasterCpu.close()
        print("Server slave stopped.")

if __name__ == "__main__":
    #if len(sys.argv) != 2:
        #print("Utilisation : python ServerSlave.py <ipMaster>")
        #sys.exit(1)

    #ipMaster = str(sys.argv[1])

    serverSlave = ServerSlave("192.168.0.20")
    serverSlave.start()
