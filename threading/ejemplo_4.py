"""
Ejemplo 1:
Queremos sumar los elementos de un arreglo CON TRHEADS.
En esta ocasión vamos a distribuir la carga de la suma de
los elementos en dos threads (olvidemos que existe GIL).
Además, trabajaremos con locks
"""

import threading
import time

elementos = [i for i in range(1, 65)]
resultado = [0]   # Variable global compartida
lock_resultado = threading.Lock()
def sumar(indice, lock):

    mitad = len(elementos) // 2     # Se calcula la mitad del arrelgo

    # Se recorre el arreglo elementos dado el indice
    for i in range(mitad * indice, mitad * (indice + 1)):
        with lock:
            print(f"Leyendo indice elementos[{i}] = {elementos[i]}")
            resultado[0] += elementos[i]
        time.sleep(0.01)    # Se dormirá para poder ver los efectos de la concurrencia


# Se instancian los threads
thread_1 = threading.Thread(target=sumar, args=(0, lock_resultado))
thread_2 = threading.Thread(target=sumar, args=(1, lock_resultado))

# Se comienza la ejecución de los threads
thread_1.start()
thread_2.start()

# El programa principal espera a que terminen ambos threads
thread_1.join()
thread_2.join()

# Se suman los resultados
print(resultado)

"""
Comentarios:
- Recordar que por GIL no existe un paralelismo real.
- Notar que no podemos agregar un return a nuestra función en target.
    Para eso usamos la lista resultados y nos aseguramos de que los indices
    de acceso sean unicos por thread. ¿Qué pasaria si tuviesemos solo una
    variable contadora?

"""