"""
Frontend de la aplicacion Wordle
"""


from PyQt6.QtCore import QObject, pyqtSignal
import requests

class Procesador(QObject):
    senal_actualizar_fila = pyqtSignal(dict)
    senal_actualizar_status = pyqtSignal(str)
    senal_limpiar = pyqtSignal()
    contador = 0

    def verificar_intento(self, palabra):
        if Procesador.contador >= 6:
            self.limpiar()
            Procesador.contador = 0
            return
        try:
            base = "http://localhost:4444/"
            respuesta = requests.get(base + "try", json={"try": palabra})
            if respuesta.status_code != 200:
                 self.senal_actualizar_status.emit(respuesta.json()["error"])
                 return
            # Se envia la informacion para que pueda ser cambiada por la fila
            respuesta_intento = {
                "contador": Procesador.contador,
                "data": respuesta.json()
            }
            self.senal_actualizar_fila.emit(respuesta_intento)
            Procesador.contador += 1
            print(respuesta.json())
            if respuesta.json()["state"] == "solved":
                self.senal_actualizar_status.emit("Ganaste!")
                requests.get(base + "result")
                Procesador.contador = 6
            elif Procesador.contador == 6:
                self.obtener_palabra()
            
            
        except Exception as e:
            print(e)
            self.senal_actualizar_status.emit("Error. Intentalo más tarde.") 

    def obtener_palabra(self):
        try:
            base = "http://localhost:4444/"
            respuesta = requests.get(base + "result")
            if respuesta.status_code != 200:
                self.senal_actualizar_status.emit(respuesta.json()["error"])
            self.senal_actualizar_status.emit("Fallaste. Respuesta: " + respuesta.json()["word"])
        except:
            self.senal_actualizar_status.emit("Error. Intentalo más tarde")

    def limpiar(self):
        self.senal_limpiar.emit()