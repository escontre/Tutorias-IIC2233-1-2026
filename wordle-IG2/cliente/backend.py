"""
Backend de la aplicacion Wordle
"""

from time import sleep
from PyQt6.QtCore import QObject, pyqtSignal, QThread
import requests

class ThreadAnimacion(QThread):
    
    def __init__(self, senal_actualizar, contador, data):
        super().__init__()
        self.senal = senal_actualizar   # Señal para emitir el cambio de celda
        self.contador = contador        # El contador interno del back
        self.data = data                # respuesta.json()
        
        
    def run(self):
        # Cada 0.5 segundos enviaremos una senal para actualizar una celda
        data_celda = {
                "fila": self.contador,
            }
        for i in range(5):
            data_celda["info"] = self.data["check"][str(i)]
            data_celda["columna"] = i
            # Al final el diccionario tendrá llaves "info", "columna" y "fila"
            self.senal.emit(data_celda)
            sleep(0.25)
        
            


class Procesador(QObject):
    senal_actualizar_celda = pyqtSignal(dict)
    senal_actualizar_status = pyqtSignal(str)
    senal_limpiar = pyqtSignal()
    contador = 0

    def __init__(self):
        super().__init__()
        self.threads = []

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
            # Se envia la informacion para que pueda ser cambiada
            # En este caso, el thread se encargará de cambia la fila celda por celda tras X tiempo

            thread = ThreadAnimacion(
                self.senal_actualizar_celda,
                Procesador.contador,
                respuesta.json())
            
            # Necesitamos almacenar el thread para que python no lo elimine al terminar el metodo
            self.threads.append(thread)
            # Cuando el thread termine, lo elimino de de la lista
            thread.finished.connect(
                lambda t=thread: self.threads.remove(t)
            )
            thread.start()
            
            # Sigue el flujo

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

    def actualizar_lista_threads(self, thread):
        self.threads.remove(thread)


"""
Comentarios:
    - lambda: self.threads.remove(thread) es distinto a lo implementado.
      En este caso se evalua al ultimo valor de la variable thread, pero si hago
      lambda t=thread: self.threads.remove(t), almaceno en t el valor actual del thread creado.
        * Idea de implementación sacada de:
          https://www.pythonguis.com/faq/elegant-shutdown-of-running-threads/
    - La lógica del thread pudo ser implementada con QTimers  
"""