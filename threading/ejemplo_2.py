"""
Ejemplo 1:
Queremos sumar los elementos de un arreglo CON TRHEADS.
En esta ocasión vamos a distribuir la carga de la suma de
los elementos en dos threads (olvidemos que existe GIL)
"""

import threading
import time

elementos = [i for i in range(1, 17)]
resultado = [0, 0]  # Se almacenan los resultados de ambos threads

def sumar(indice):

    mitad = len(elementos) // 2     # Se calcula la mitad del arrelgo
    contador = 0

    # Se recorre el arreglo elementos dado el indice
    for i in range(mitad * indice, mitad * (indice + 1)):
        print(f"Leyendo indice elementos[{i}] = {elementos[i]}")
        contador = contador + elementos[i]
        time.sleep(0.01)    # Se dormirá para poder ver los efectos de la concurrencia

    resultado[indice] = contador    # Almacenamos la suma en la lista "resultado"

# Se instancian los threads
thread_1 = threading.Thread(target=sumar, args=(0,))
thread_2 = threading.Thread(target=sumar, args=(1,))

# Se comienza la ejecución de los threads
thread_1.start()
thread_2.start()

# El programa principal espera a que terminen ambos threads
thread_1.join()
thread_2.join()

# Se suman los resultados
print(resultado[0] + resultado[1])

"""
Comentarios:
- Recordar que por GIL no existe un paralelismo real.
- Notar que no podemos agregar un return a nuestra función en target.
    Para eso usamos la lista resultados y nos aseguramos de que los indices
    de acceso sean unicos por thread. ¿Qué pasaria si tuviesemos solo una
    variable contadora?

"""