"""
Ejemplo 1:
Queremos sumar los elementos de un arreglo
"""

import time
# Lista con los elementos 1 al 16
elementos = [i for i in range(1, 17)]

contador = 0

for i in range(16):
    print(f"Leyendo indice elementos[{i}] = {elementos[i]}")
    contador = contador + elementos[i]
    time.sleep(0.01)

print(contador)

"""
Notar que la cantidad de pasos depende de la lista elementos
"""