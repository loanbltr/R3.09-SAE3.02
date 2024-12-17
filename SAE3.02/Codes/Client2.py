import sys, socket, os
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QFileDialog, QTextEdit
)

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Socket Client Interface")
        self.resize(600, 400)

        layout = QVBoxLayout()

        ipLayout = QHBoxLayout()
        ipLabel = QLabel("Server IP:")
        self.ipInput = QLineEdit()
        ipLayout.addWidget(ipLabel)
        ipLayout.addWidget(self.ipInput)
        layout.addLayout(ipLayout)

        portLayout = QHBoxLayout()
        portLabel = QLabel("Port:")
        self.portInput = QLineEdit()
        portLayout.addWidget(portLabel)
        portLayout.addWidget(self.portInput)
        layout.addLayout(portLayout)

        self.connectButton = QPushButton("Connect")
        layout.addWidget(self.connectButton)
        self.connectButton.clicked.connect(connectMaster)

        # File Input and Select Button
        fileLayout = QHBoxLayout()
        self.fileInput = QLineEdit()
        self.fileInput.setPlaceholderText("No file selected")
        self.fileInput.setReadOnly(True)
        fileButton = QPushButton("Select File")
        fileButton.clicked.connect(lambda: selectFile())
        fileLayout.addWidget(self.fileInput)
        fileLayout.addWidget(fileButton)
        layout.addLayout(fileLayout)

        fileDisplayLabel = QLabel("File Content:")
        self.fileDisplay = QTextEdit()
        self.fileDisplay.setReadOnly(True)
        layout.addWidget(fileDisplayLabel)
        layout.addWidget(self.fileDisplay)

        self.send_button = QPushButton("Send File")
        layout.addWidget(self.send_button)
        self.send_button.clicked.connect(sendMaster)

        messagesLabel = QLabel("Messages Received:")
        self.messagesDisplay = QTextEdit()
        self.messagesDisplay.setReadOnly(True)
        layout.addWidget(messagesLabel)
        layout.addWidget(self.messagesDisplay)

        self.setLayout(layout)

def selectFile():
    options = QFileDialog.Options()
    filePath, _ = QFileDialog.getOpenFileName(None, "Select file(s)", "", "Files (*.py)", options=options)
    if filePath:
        window.fileInput.setText(filePath)
        with open(filePath, 'r') as file:
            window.fileDisplay.setText(file.read())

def connectMaster():
    global socketConnMaster, socketConnMasterConnected
    try:
        ip = window.ipInput.text()
        port = int(window.portInput.text())
        socketConnMaster = socket.socket()
        socketConnMaster.connect((ip, port))
        socketConnMasterConnected = True
        print(f"Connecting to {ip}:{port}")
    except Exception as e:
        print(f"Error connecting to server master: {e}")

def sendMaster():
    if not socketConnMasterConnected:
        print("Not connected to server master.")
        return
    try:
        message = window.fileInput.text()
        socketConnMaster.send(fileToMsg(message).encode())
        print(f"Message sent to server master: {message}")
    except Exception as e:
        print(f"Error sending command to server master: {e}")

def fileToMsg(file_path):
    if os.path.exists(file_path):
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()
        return content
    else:
        return f"Le fichier '{file_path}' n'existe pas."


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
