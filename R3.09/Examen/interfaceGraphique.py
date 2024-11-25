#lien GitHub: https://github.com/loanbltr/R3.09-SAE3.02/tree/main/R3.09/Examen

import sys, socket, threading
from PyQt5.QtCore import QCoreApplication
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QGridLayout, QPushButton, QLabel, QLineEdit, QTextEdit


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Le serveur de tchat")

        widget = QWidget()
        self.setCentralWidget(widget)
        grid = QGridLayout()
        widget.setLayout(grid)

        self.boutonStart = QPushButton("Démarrage du serveur")
        self.boutonQuit = QPushButton("Quitter")
        self.ipServeur = QLineEdit()
        self.txtServer = QLabel("Serveur")
        self.port = QLineEdit()
        self.txtPort = QLabel("Port")
        self.nbClients = QLineEdit()
        self.txtNbClients = QLabel("Nombre de clients maximum")
        self.tchat = QTextEdit()
        self.tchat.setReadOnly(True)

        self.boutonStart.clicked.connect(self.actionStart)
        self.boutonQuit.clicked.connect(self.actionQuit)

        grid.addWidget(self.txtServer, 0, 0)
        grid.addWidget(self.ipServeur, 0, 2)
        grid.addWidget(self.txtPort, 1, 0)
        grid.addWidget(self.port, 1, 2)
        grid.addWidget(self.txtNbClients, 2, 0)
        grid.addWidget(self.nbClients, 2, 2)
        grid.addWidget(self.boutonStart, 3, 0, 1, 3)
        grid.addWidget(self.tchat, 4, 0, 1, 3)
        grid.addWidget(self.boutonQuit, 5, 0, 1, 3)

        self.resize(500, 600)

    def actionStart(self):
        if self.boutonStart.text() == "Démarrage du serveur":
            self.boutonStart.setText("Arret du serveur")
            self.demarrage()
        else:
            self.boutonStart.setText("Démarrage du serveur")
            self.ipServeur.setText("")
            self.port.setText("")
            self.nbClients.setText("")
            self.tchat.clear()
            socket.socket.close()


    def actionQuit(self):
        QCoreApplication.exit(0)

    def accept(self):
        global message
        server_socket = socket.socket()
        print("Socket crée")
        server_socket.bind((self.ipServeur.text(), int(self.port.text())))
        server_socket.listen(int(self.nbClients.text()))
        print("Socket en cours d'écoute")
        conn, address = server_socket.accept()
        print("Connexion reçue de", address)
        self.receiveMessage(server_socket, conn)

    def receiveMessage(self, s, conn):
        global message
        while True:
            message = conn.recv(1024).decode()
            if not message:
                print("Client déconnecté")
                break
            elif message == "deco-server":
                print("Arret de la communication")
                break
            print(f"MESSAGE DU CLIENT: {message}")
            self.tchat.append("\n Client: " +  message)
        clientAccept.stop()
        conn.close()
        s.close()
        print("Socket fermée")

    def demarrage(self):
        global clientAccept
        if self.ipServeur.text() == "":
            self.ipServeur.setText("localhost")
        print(int(self.port.text()))
        #if not 1 <= int(self.port.text()) <= 65535:
        if self.port.text() == "":
            self.port.setText("4200")
            #else:
                #raise ValueError("Un port est obligatoirement ue valeur numérique entre 1 et 65535")
        if self.nbClients.text() == "":
            self.nbClients.setText("5")
        clientAccept = threading.Thread(target=self.accept)
        clientAccept.start()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())


#Q1: Il faudra ajouter sur le client une déconexion du socket qu'il aura rejoint.
#Q2: Afin de connecter plusieurs clients, il faudra les ajouter à une liste afin de pouvoir traiter l'ensemble des clients à l'aide d'une boucle.
