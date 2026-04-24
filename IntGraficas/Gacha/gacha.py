"""
Vamos a crear una maquina gacha.
La idea es que al momento de presionar un boton
se pueda visualizar tras un cierto tiempo una nueva ventana
con el premio.

"""

import sys
import os
import random
from PyQt6.QtWidgets import QApplication, QWidget, QPushButton, QLabel, QHBoxLayout, QVBoxLayout
from PyQt6.QtCore import pyqtSignal
from PyQt6.QtGui import QPixmap


class Ventana(QWidget):
    # Señal para manejar las imagenes en la pestaña de premio
    senal_premio = pyqtSignal(str)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.init_gui()

    def init_gui(self):
        # Se fija el titulo de la pestaña, las dimensiones y el color del fondo
        self.setWindowTitle("Ejemplo - Gacha!")
        self.setGeometry(0, 0, 600, 600)
        self.setStyleSheet("background-color: lightblue;")

        # Se fija una imagen para la maquina de gachas
        self.label_gacha = QLabel(self)
        self.label_gacha.resize(180, 200)
        ruta_imagen = os.path.join("images", "ball_machine.png")
        pixeles = QPixmap(ruta_imagen)
        self.label_gacha.setPixmap(pixeles)
        self.label_gacha.setScaledContents(True)

        # Se fija un boton para poder hacer gacha
        self.boton_gacha = QPushButton("Hacer gacha", self)
        self.boton_gacha.sizeHint()         # Se redimenciona a un tamaño recomendado
        self.boton_gacha.clicked.connect(self.agregar_imagen)   # Se conecta a su handler

        # Se genera un layout vertical para guardar la imagen y el boton
        vbox = QVBoxLayout()
        vbox.addStretch(1)
        vbox.addWidget(self.label_gacha)
        vbox.addWidget(self.boton_gacha)
        vbox.addStretch(1)

        hbox = QHBoxLayout()
        hbox.addStretch(3)
        hbox.addLayout(vbox)    # Agregamos el layout vertical al horizontal
        hbox.addStretch(3)
        self.setLayout(hbox)

    def agregar_imagen(self):
        # Revisamos las imagenes en el directorio images
        lista_imagenes = os.listdir(os.path.join("images", "prizes"))
        # Se toma un premio aleatorio
        premio = random.choice(lista_imagenes)
        print(premio)
        # Se emite la ruta por la señal
        self.senal_premio.emit(os.path.join("images", "prizes", premio))

class VentanaPremio(QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.init_gui_premio()

    def init_gui_premio(self):
        # Se fija el titulo de la pestaña, las dimensiones y el color del fondo
        self.setWindowTitle("Ejemplo - Premio!")
        self.setGeometry(0, 0, 300, 300)
        self.setStyleSheet("background-color: pink;")
        
        # Se fija la el label para el premio
        self.label_premio = QLabel(self)
        self.label_premio.setFixedSize(200, 200)
        # Se genera un layout vertical para guardar la imagen y el boton
        vbox = QVBoxLayout()
        vbox.addStretch(1)
        vbox.addWidget(self.label_premio)
        vbox.addStretch(1)

        hbox = QHBoxLayout()
        hbox.addStretch(1)
        hbox.addLayout(vbox)    # Agregamos el layout vertical al horizontal
        hbox.addStretch(1)
        self.setLayout(hbox)

    # Se ejecuta cuando se emite una señal! (despues de conectarla más abajo)
    def set_imagen(self, ruta_premio):
        # Se muestra la pestaña
        # Se fija la imagen
        pixeles_premio = QPixmap(ruta_premio)
        self.label_premio.setPixmap(pixeles_premio)
        self.label_premio.setScaledContents(True)
        self.show()

if __name__ == "__main__":
    def hook(type, value, traceback) -> None:
        print(type)
        print(traceback)
    sys.__excepthook__ = hook

    app = QApplication([])
    ventana = Ventana()
    ventana_premio = VentanaPremio()
    ventana.senal_premio.connect(ventana_premio.set_imagen)
    ventana.show()
    sys.exit(app.exec())

