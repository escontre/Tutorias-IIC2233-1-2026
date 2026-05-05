"""
Implementaremos un cliente que consuma
mascotAPI.
Se realizaran 7 requests:
    - Se revisaran las mascotas actuales
    - Se agregara una nueva mascota
    - Se revisaran las mascotas actuales
    - Se creará una mascota mal
    - Se buscará una mascota
    - Se borrará una mascota
    - Se revisaran las mascotas actuales
"""

import requests

base = "http://localhost:4444/mascotas"

print("1) Se revisan todas las mascotas")
respuesta = requests.get(base)
print(respuesta.json())

print("2) Se agregara una nueva mascota")
mascota = {
    "nombre": "Lisa",
    "dueno": "Esteban",
    "raza": "Gata bonita",
    "edad": 10
}
respuesta = requests.post(base, json=mascota)
print(respuesta.status_code, respuesta.json())

print("3) Se revisan de nuevo las mascotas actuales")
respuesta = requests.get(base)
print(respuesta.json())

print("4) Se creara una mascota mal")
mascota = {
    "nombre": "Lisa",
    "dueno": "Esteban",
    "raza": "Gata bonita",
    "edad": "Diez"
}
respuesta = requests.post(base, json=mascota)
print(respuesta.status_code, respuesta.json())

print("5) Buscando mascota con id 2")
respuesta = requests.get(base + "/2")
print(respuesta.status_code, respuesta.json())

print("6) Se borrara el registro de mascota con id 2")
respuesta = requests.delete(base + "/2")
print(respuesta.status_code)

print("7) Se revisa por ultima vez todo")
respuesta = requests.get(base)
print(respuesta.json())