import sys
from PyQt5.QtCore import QCoreApplication
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QGridLayout, QPushButton, QLabel, QLineEdit, QComboBox


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Une première fenêtre")  # Titre de la fenêtre

        # Créer un widget central et définir sa mise en page
        widget = QWidget()
        self.setCentralWidget(widget)
        grid = QGridLayout()
        widget.setLayout(grid)

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
        temperature = float(self.degre.text())
        if self.choose.currentText() == "°C → K":
            if temperature < -273.15:
                raise ValueError("La température ne peut pas être inférieure à -273.15 °C.")
            converted = temperature + 273.15
        else:
            if temperature < 0:
                raise ValueError("La température ne peut pas être inférieure à 0 K.")
            converted = temperature - 273.15
        self.kelvin.setText(f"{converted:.2f}")

    def update(self):
        if self.choose.currentText() == "°C → K":
            self.txtdegre.setText("°C")
            self.txtkelvin.setText("K")
        else:
            self.txtdegre.setText("K")
            self.txtkelvin.setText("°C")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
