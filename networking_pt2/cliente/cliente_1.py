"""
Cliente 1:
- Se autenticara como usuario_1
- Enviara un nuevo archivo
- Cargara un archivo ya presente en el servidor
"""

import socket
import os
import json 

def enviar_json(sock, data):
    mensaje = json.dumps(data).encode("utf-8")
    sock.sendall(len(mensaje).to_bytes(4, "big"))
    sock.sendall(mensaje)

def leer_json(sock):
    bytes_largo = bytearray()
    while len(bytes_largo) < 4:
        por_leer = 4 - len(bytes_largo)
        datos_recibidos = sock.recv(por_leer)
        bytes_largo.extend(datos_recibidos)
    largo = int.from_bytes(bytes_largo, "big")
    data = bytearray()
    while len(data) < largo:
        por_leer = min(4096, largo - len(data))
        datos_recibidos = sock.recv(por_leer)
        data.extend(datos_recibidos)
    return json.loads(bytes(data).decode("utf-8"))


sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect(("localhost", 5000))

# Se inicia sesión
login = {
    "nombre" : "usuario_1",
    "contrasena" : "contrasena_segura"
}
enviar_json(sock, login)

respuesta = leer_json(sock)
print("Resultado del login")

# Se envia un archivo al servidor 
nombre_archivo = "gato_1.png"
ruta = os.path.join("files", "cliente_1", nombre_archivo)
largo = os.path.getsize(ruta)


contenido = {
    "tipo" : "guardar",
    "archivo" : nombre_archivo,
    "largo" : largo
}
enviar_json(sock, contenido)

bytes_enviados = 0
with open(ruta, "rb") as archivo:
    datos = archivo.read()

while bytes_enviados < largo:
    bytes_enviados += sock.send(datos[bytes_enviados:])

# Se carga un archivo desde el servidor
nombre_archivo = "cat_server_1.png"
contenido = {
    "tipo" : "cargar",
    "archivo" : nombre_archivo
}
enviar_json(sock, contenido)
respuesta = leer_json(sock)
largo = leer_json(sock)
datos = bytearray()
bytes_leidos = 0

while len(datos) < largo:
    por_leer = min(4096, largo-bytes_leidos)
    datos_recibidos = sock.recv(por_leer)
    bytes_leidos += len(datos_recibidos)
    datos.extend(datos_recibidos)

with open(os.path.join("files", "cliente_1", nombre_archivo), "wb") as archivo:
    archivo.write(bytes(datos))

# Se termina la conexion

contenido = {
    "tipo" : "salir"
}

enviar_json(sock, contenido)
sock.close()