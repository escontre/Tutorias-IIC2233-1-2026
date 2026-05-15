"""
Backend de la aplicacion wordle
"""

import sys
from PyQt6.QtCore import pyqtSignal, Qt
from PyQt6.QtWidgets import (QApplication, QWidget, QLabel, QPushButton,
                             QLineEdit, QGridLayout, QVBoxLayout, QHBoxLayout)
from backend import Procesador

class VentanaJuego(QWidget):
    senal_enviar_palabra = pyqtSignal(str)
    def __init__(self):
        super().__init__()
        self.inicializar_gui()
        

    def inicializar_gui(self):
        # Fijamos atributos de la ventana
        self.setGeometry(0, 0, 200, 350)
        self.setWindowTitle("Wordle IIC2233")
        # Se instancian los labels dentro de self.labels y se instancian dentro de la grilla
        grilla = QGridLayout()
        self.labels = []
        for i in range(6):
            fila = []
            for j in range(5):
                # Se crea el label y se fijan caracteristicas
                label = QLabel(self)
                label.setFixedSize(40, 40)
                label.setStyleSheet("background-color: black")
                fila.append(label)
                grilla.addWidget(label, i, j)
            self.labels.append(fila)

        vbox =  QVBoxLayout()
        vbox.addLayout(grilla)

        # Agregar el form con el boton y un texto de status
        self.input_respuesta = QLineEdit()
        self.boton = QPushButton("Verificar")
        self.status = QLabel("", self)
        
        vbox.addWidget(self.status)
        vbox.addWidget(self.input_respuesta)
        vbox.addWidget(self.boton)
        # Se fija un layout horizontal para estetica de lo anterior
        hbox = QHBoxLayout()
        hbox.addLayout(vbox)
        self.setLayout(hbox)

        # El boton lo vinculamos al metodo enviar_palabra
        self.boton.clicked.connect(self.enviar_palabra)
        # Similar a lo anterior pero con enter
        self.input_respuesta.returnPressed.connect(self.enviar_palabra)

    # Metodo encargado de comunicarse con el backend para 
    # enviar el intento
    def enviar_palabra(self):
        # Se toma lo escrito en input
        intento = self.input_respuesta.text()
        # Limpiamos el input y el status
        self.input_respuesta.clear()
        self.status.setText("")
        # Enviamos por medio de una senal
        self.senal_enviar_palabra.emit(intento)
        
    # Metodo encargado de cambiar una fila a partir de la respuesta
    def cambiar_colores(self, respuesta):
        # Separamos el diccionario
        fila = respuesta["contador"]
        data = respuesta["data"]["check"]

        # A partir de fila, cambiamos cada valor
        for j in range(5):
            self.labels[fila][j].setStyleSheet(f"background-color: {data[str(j)]['color']}")
            self.labels[fila][j].setText(data[str(j)]["letter"])
    
    # Metodo encargado de cambiar el status (wow!)
    def cambiar_status(self, respuesta):
        # Fijamos el texto respuesta en el status
        self.status.setText(respuesta)

    # Metodo encargado de limpiar todas las entradas para volver a jugar
    def limpiar_entradas(self):
        # Limpiamos todas las celdas
        for i in range(6):
            for j in range(5):
                self.labels[i][j].setText("")
                self.labels[i][j].setStyleSheet("background-color: black")

        # Limpiamos el status y el input
        self.status.setText("")
        self.input_respuesta.clear()



if __name__ == '__main__':
    def hook(type, value, traceback) -> None:
        print(type)
        print(traceback)

    sys.__excepthook__ = hook

    app = QApplication([])
    procesador = Procesador()
    ventana = VentanaJuego()

    # Se agregan la vinculacion de senales entre backend y frontend
    ventana.senal_enviar_palabra.connect(procesador.verificar_intento)
    procesador.senal_actualizar_fila.connect(ventana.cambiar_colores)
    procesador.senal_actualizar_status.connect(ventana.cambiar_status)
    procesador.senal_limpiar.connect(ventana.limpiar_entradas)
    ventana.show()

    sys.exit(app.exec())