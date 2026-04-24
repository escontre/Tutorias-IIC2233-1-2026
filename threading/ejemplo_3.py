"""
Ejemplo 1:
Queremos sumar los elementos de un arreglo CON TRHEADS.
En esta ocasión vamos a distribuir la carga de la suma de
los elementos en dos threads (olvidemos que existe GIL).
Esta vez, lo vamos a realizar como si fueran clases
"""

import threading
import time

elementos = [i for i in range(1, 17)]

class Sumador(threading.Thread):
    def __init__(self, indice):
        super().__init__()  # IMPORTANTE. Thread tiene su propia inicialización interna

        # Atributos de indice y resultado
        self.indice = indice
        self.resultado = 0

    def run(self):
        mitad = len(elementos) // 2     # Se calcula la mitad del arrelgo
        contador = 0
        # Se recorre el arreglo elementos dado el indice
        for i in range(mitad * self.indice, mitad * (self.indice + 1)):
            print(f"Leyendo indice elementos[{i}] = {elementos[i]}")
            contador = contador + elementos[i]
            time.sleep(0.01)    # Se dormirá para poder ver los efectos de la concurrencia

        # Almacenamos el resultado
        self.resultado = contador

# Se crean dos instancias Sumador con sus indices
thread_1 = Sumador(0)
thread_2 = Sumador(1)

# Se comienza la ejecución de los threads
thread_1.start()
thread_2.start()

# El programa principal espera a que terminen ambos threads
thread_1.join()
thread_2.join()

# Se suman los resultados
print(thread_1.resultado + thread_2.resultado)

