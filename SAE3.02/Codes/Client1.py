import sys, socket, os, threading
from PyQt5.QtCore import Qt, QMetaObject, Q_ARG
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QFileDialog, QTextEdit, QCheckBox
)

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Client Interface")
        self.resize(600, 400)

        layout = QVBoxLayout()

        localLayout = QHBoxLayout()
        localLabel = QLabel("Localhost:")
        self.localLayout = QCheckBox()
        self.localLayout.setChecked(False)
        localLayout.addWidget(localLabel)
        localLayout.addWidget(self.localLayout)
        layout.addLayout(localLayout)

        self.localLayout.stateChanged.connect(self.updateLabel)

        ipLayout = QHBoxLayout()
        ipLabel = QLabel("Server IP:")
        self.ipInput = QLineEdit()
        self.ipInput.setPlaceholderText("127.0.0.1")
        self.ipInput.setText("192.168.0.20")

        ipLayout.addWidget(ipLabel)
        ipLayout.addWidget(self.ipInput)
        layout.addLayout(ipLayout)

        portLayout = QHBoxLayout()
        portLabel = QLabel("Port:")
        self.portInput = QLineEdit()
        self.portInput.setPlaceholderText("11111")
        self.portInput.setText("11111")
        portLayout.addWidget(portLabel)
        portLayout.addWidget(self.portInput)
        layout.addLayout(portLayout)

        self.connectButton = QPushButton("Connect")
        layout.addWidget(self.connectButton)
        self.connectButton.clicked.connect(self.connectMaster)

        fileLayout = QHBoxLayout()
        self.fileInput = QLineEdit()
        self.fileInput.setPlaceholderText("No file selected")
        self.fileInput.setReadOnly(True)
        fileButton = QPushButton("Select File")
        fileButton.clicked.connect(self.selectFile)
        fileLayout.addWidget(self.fileInput)
        fileLayout.addWidget(fileButton)
        layout.addLayout(fileLayout)

        fileDisplayLabel = QLabel("File Content:")
        self.fileDisplay = QTextEdit()
        self.fileDisplay.setReadOnly(False)
        layout.addWidget(fileDisplayLabel)
        layout.addWidget(self.fileDisplay)

        self.send_button = QPushButton("Send File")
        layout.addWidget(self.send_button)
        self.send_button.clicked.connect(self.sendMaster)

        messagesLabel = QLabel("Messages Received:")
        self.messagesDisplay = QTextEdit()
        self.messagesDisplay.setReadOnly(True)
        layout.addWidget(messagesLabel)
        layout.addWidget(self.messagesDisplay)

        self.setLayout(layout)

    def updateLabel(self):
        if self.localLayout.isChecked():
            self.ipInput.setText("127.0.0.1")
            self.portInput.setText("11111")
        else:
            self.ipInput.setText("")
            self.portInput.setText("")

    def selectFile(self):
        options = QFileDialog.Options()
        filePath, _ = QFileDialog.getOpenFileName(None, "Select file(s)", "", "Source Files (*.py *.c *java);;All Files (*)")
        if filePath:
            self.fileInput.setText(filePath)
            with open(filePath, 'r') as file:
                self.fileDisplay.setText(file.read())

    def connectMaster(self):
        global socketConnMaster, socketConnMasterConnected
        if self.connectButton.text() == "Connect":
            try:
                ip = self.ipInput.text()
                port = int(self.portInput.text())
                socketConnMaster = socket.socket()
                socketConnMaster.connect((ip, port))
                socketConnMasterConnected = True
                print(f"Connecting to {ip}:{port}")
                threading.Thread(target=self.receiveMaster, args=(socketConnMaster,), daemon=True).start()
                self.connectButton.setText("Disconnect")
            except Exception as e:
                print(f"Error connecting to server master: {e}")
        else:
            self.disconnectMaster()

    def receiveMaster(self, socket):
        while True:
            try:
                data = socketConnMaster.recv(1024).decode()
                if not data:
                    break
                print(f"Received message from server master: {data}")

                # Utiliser QMetaObject.invokeMethod pour mettre à jour l'interface utilisateur
                QMetaObject.invokeMethod(
                    self.messagesDisplay,
                    "append",
                    Qt.QueuedConnection,
                    Q_ARG(str, data)
                )
            except Exception as e:
                print(f"Error receiving message from server master: {e}")
                break

    def sendMaster(self):
        if not socketConnMasterConnected:
            print("Not connected to server master.")
            return
        try:
            file_content = self.fileDisplay.toPlainText()
            message = f"code|{self.fileInput.text().split('/')[-1]}|{file_content}"
            socketConnMaster.send(message.encode())
            print(f"Message sent to server master: {message}")
            self.messagesDisplay.clear()
        except Exception as e:
            print(f"Error sending command to server master: {e}")

    def disconnectMaster(self):
        global socketConnMaster, socketConnMasterConnected
        try:
            socketConnMaster.close()
            socketConnMasterConnected = False
            print("Disconnected from server master.")
            self.connectButton.setText("Connect")
        except Exception as e:
            print(f"Error disconnecting from server master: {e}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
