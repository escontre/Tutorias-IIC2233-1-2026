"""
Usaremos el metodo montecarlo para estimar el número pi.
Usaremos un cuadrado de lado 1 con 1/4 de circunferencia dentro de radio 1.
Mediremos N puntos aleatorios.

Comparemos el coste operacional de usar funciones numpy y built-in de python
"""
import numpy as np
import time
import random

N = 10000000

def verificar_area(x, y):
    """
    Se verifica si es que x, y están dentro del area del circulo o no
    """
    ver = x ** 2 + y ** 2
    # Si es que el número es menor que 1, entonces está dentro del circulo
    if ver <= 1:
        return True
    return False


# Primero, usando solo python
t0 = time.time()
contador_circulo = 0
for i in range(N):
    x, y = random.random(), random.random()
    val = verificar_area(x, y)
    if val:
        contador_circulo += 1

pi = 4 * (contador_circulo / N)
t1 = time.time()
print(f"Prueba 1: Valor de pi = {pi}")
print(f"Prueba 1: Tiempo total = {t1 - t0}")


# Usando funciones numpy
t0 = time.time()
# Obtenemos dos arreglos de tamaño N con números aleatorios

x_array = np.random.rand(N)
y_array = np.random.rand(N)

# ver es un array de tamaño N que contiene, para una pos i, x_array[i] ** 2 + y_array[i] ** 2
ver = x_array ** 2 + y_array ** 2

# Generamos un array de largo N con valores 1 o 0 dependiendo si el punto está o no el el circulo. 
puntos_circulo = np.where(ver <= 1, 1, 0)

# Calculamos la media y la multiplicamos por 4.
pi = 4 * np.mean(puntos_circulo)
t1 = time.time()
print(f"Prueba 2: Valor de pi = {pi}")
print(f"Prueba 2: Tiempo total = {t1 - t0}")
