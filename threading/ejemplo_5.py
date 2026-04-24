"""
Usaremos Daemon para poder terminar el programa.
Simularemos una carrera de threads en la cual si
uno o más threads terminan, entonces el programa
terminará.
"""

import threading
import time
import random

def correr():
    thread = threading.current_thread()
    time.sleep(random.randint(2, 10))
    print(f"{thread.name} terminó")

# Instanciamos una serie de threads en una lista
lista_threads = []
for i in range(5):
    thread = threading.Thread(name=f"{i}", target=correr, daemon=True)
    lista_threads.append(thread)

# Se inician todos los threads
for thread in lista_threads:
    thread.start()

# Se empieza a consultar en la lista de threads si es que uno terminó
carrera = True
while carrera:
    for thread in lista_threads:
        time.sleep(0.01)
        if not thread.is_alive():
            carrera = False
            break

