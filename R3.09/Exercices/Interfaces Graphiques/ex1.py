import sys
from PyQt5.QtCore import QCoreApplication
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QGridLayout, QPushButton, QLabel, QLineEdit


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Une première fenêtre")  # Titre de la fenêtre

        # Créer un widget central et définir sa mise en page
        widget = QWidget()
        self.setCentralWidget(widget)
        grid = QGridLayout()
        widget.setLayout(grid)

        self.ok = QPushButton("Ok")
        self.quit = QPushButton("Quitter")
        self.entrer = QLineEdit()
        self.phrase = QLabel("Saisir votre nom")
        self.bienvenue = QLabel()

        self.ok.clicked.connect(self.actionOk)
        self.quit.clicked.connect(self.actionQuitter)

        # Ajouter les widgets à la disposition
        grid.addWidget(self.phrase, 0, 0)
        grid.addWidget(self.entrer, 1, 0)
        grid.addWidget(self.ok, 2, 0)
        grid.addWidget(self.bienvenue, 3, 0)
        grid.addWidget(self.quit, 4, 0)

        self.resize(500, 250)

    def actionOk(self):
        self.bienvenue.setText(f"Bienvenue {self.entrer.text()} !")

    def actionQuitter(self):
        QCoreApplication.exit(0)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
