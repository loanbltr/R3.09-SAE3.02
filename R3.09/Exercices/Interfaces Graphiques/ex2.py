import sys
from PyQt5.QtCore import QCoreApplication
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QGridLayout, QPushButton, QLabel, QLineEdit, QComboBox, QAction, QMessageBox


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Une première fenêtre")  # Titre de la fenêtre

        # Créer un widget central et définir sa mise en page
        widget = QWidget()
        self.setCentralWidget(widget)
        grid = QGridLayout()
        widget.setLayout(grid)

        menu_bar = self.menuBar()
        window_menu = menu_bar.addMenu("Choisir la fenêtre")

        # Ajouter les actions de menu pour afficher les fenêtres
        ex1_action = QAction("Fenêtre EX1", self)
        ex1_action.triggered.connect(self.show_ex1_window)
        window_menu.addAction(ex1_action)

        my_window_action = QAction("Fenêtre MyWindow", self)
        my_window_action.triggered.connect(self.show_my_window)
        window_menu.addAction(my_window_action)

        self.txttempdegre = QLabel("Température")
        self.degre = QLineEdit()
        self.txtdegre = QLabel("°C")
        self.boutonConvert = QPushButton("Convertir")
        self.choose = QComboBox()
        self.choose.addItems(["°C → K", "K → °C"])
        self.choose.currentIndexChanged.connect(self.update)
        self.txttempkelvin = QLabel("Conversion")
        self.kelvin = QLineEdit()
        self.kelvin.setReadOnly(True)
        self.txtkelvin = QLabel("K")

        self.boutonConvert.clicked.connect(self.actionBoutonConvert)

        # Ajouter les widgets à la disposition
        grid.addWidget(self.txttempdegre, 0, 0)
        grid.addWidget(self.degre, 0, 1)
        grid.addWidget(self.txtdegre, 0, 2)
        grid.addWidget(self.boutonConvert, 1, 1)
        grid.addWidget(self.choose, 1, 2)
        grid.addWidget(self.txttempkelvin, 2, 0)
        grid.addWidget(self.kelvin, 2, 1)
        grid.addWidget(self.txtkelvin, 2, 2)

        self.resize(500, 250)

    def actionBoutonConvert(self):
        try:
            temperature = float(self.degre.text())
        except ValueError:
            QMessageBox.warning(self, "Erreur", "Veuillez entrer une valeur numérique valide.")
            return

        if self.choose.currentText() == "°C → K":
            if temperature < -273.15:
                QMessageBox.warning(self, "Erreur", "La température ne peut pas être inférieure à -273.15 °C.")
                return
            converted = temperature + 273.15
        else:
            if temperature < 0:
                QMessageBox.warning(self, "Erreur", "La température ne peut pas être inférieure à 0 K.")
                return
            converted = temperature - 273.15

        self.kelvin.setText(f"{converted:.2f}")

    def update(self):
        if self.choose.currentText() == "°C → K":
            self.txtdegre.setText("°C")
            self.txtkelvin.setText("K")
        else:
            self.txtdegre.setText("K")
            self.txtkelvin.setText("°C")

    def show_ex1_window(self):
        QMessageBox.information(self, "Info", "Fenêtre EX1 - À implémenter")

    def show_my_window(self):
        QMessageBox.information(self, "Info", "Fenêtre MyWindow - À implémenter")


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
