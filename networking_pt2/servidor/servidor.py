"""
El servidor se encargará de manejar usuarios, y en base a su información,
poder manejar archivos de cada uno.
Debemos:
    - Manejar el login de usuarios
    - Solicitar archivos al directorio
    - Enviar archivos
"""

import socket
import os 
import json

# Definimos funciones utiles para el manejo de archivos

def guardar_datos_json(contenido):
    with open("usuarios.json", "w") as archivo:
        json.dump(contenido, archivo, indent=4)

def cargar_datos_json():
    with open("usuarios.json", "r") as archivo:
        return json.load(archivo)

def validar_login(nombre, contrasena):
    """
    Si es válido el usuario y la contraseña, se retorna True
    Si es que es falso, se retorna -1
    """
    data = cargar_datos_json()
    for usuario in data["usuarios"]:
        if usuario["nombre"] == nombre and usuario["contrasena"] == contrasena:
            return True 
    return False

def obtener_archivos(nombre_usuario):
    data = cargar_datos_json()
    for usuario in data["usuarios"]:
        if usuario["nombre"] == nombre_usuario:
            return True, usuario["archivos"]
    return False, []

def agregar_archivo(nombre_usuario, nombre_archivo):
    data = cargar_datos_json()
    for usuario in data["usuarios"]:
        if usuario["nombre"] == nombre_usuario:
            usuario["archivos"].append(nombre_archivo)
            guardar_datos_json(data)
            return True 
    return False

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

# insetanciamos el socket TCP
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.bind(("localhost", 5000))
sock.listen()
actual_user = None
sock_cliente, _  = sock.accept()

while True:
    # Se revisa el login si no hay ningun usuario autenticado
    if actual_user is None:
        try:
            print("Servidor leyendo login")
            # Se lee lo enviado por el cliente
            contenido = leer_json(sock_cliente)
            # Se revisa si el login es correcto
            respuesta = validar_login(contenido["nombre"], contenido["contrasena"])
            # Si la respuesta es valida, se fija como actual usuario
            if respuesta:
                actual_user = contenido["nombre"]
            # Se envia la respuesta al cliente
            enviar_json(sock_cliente, respuesta)
            print("login exitoso")
        except Exception as e:
            print(e)
            print("Error al realizar la operacion")
            enviar_json(sock_cliente, False)
            continue
    else:
        try:
            print("Servidor leyendo operacion")
            operacion = leer_json(sock_cliente)
            # Operacion guardar: Cliente quiere guardar un archivo en el servidor
            if operacion["tipo"] == "guardar":
                print("Servidor leyendo operacion: guardar")
                nombre_archivo = operacion["archivo"]
                largo = operacion["largo"]
                datos = bytearray()
                bytes_leidos = 0

                # Se reciben los bytes del archivo
                while len(datos) < largo:
                    por_leer = min(4096, largo-bytes_leidos)
                    datos_recibidos = sock_cliente.recv(por_leer)
                    bytes_leidos += len(datos_recibidos)
                    datos.extend(datos_recibidos)
                
                # Se escribe el archivo y se asocia al usuario
                with open(os.path.join("files", nombre_archivo), "wb") as archivo:
                    archivo.write(bytes(datos))

                agregar_archivo(actual_user, nombre_archivo)
            
            elif operacion["tipo"] == "cargar":
                print("Servidor leyendo operacion: cargar")
                nombre_archivo = operacion["archivo"]
                # Se verifica si es que el archivo pertenece al usuario
                resultado, archivos = obtener_archivos(actual_user)
                if not resultado or nombre_archivo not in archivos:
                    print("No existe el archivo")
                    enviar_json(sock_cliente, resultado)
                    continue

                enviar_json(sock_cliente, respuesta)
                ruta = os.path.join("files", nombre_archivo)
                largo = os.path.getsize(ruta)
                enviar_json(sock_cliente, largo)
                bytes_enviados = 0
                with open(ruta, "rb") as archivo:
                    datos = archivo.read()
                # Se envian los datos del archivo al cliente
                while bytes_enviados < largo:
                    bytes_enviados += sock_cliente.send(datos[bytes_enviados:])
            elif operacion["tipo"] == "salir":
                print("Servidor leyendo operacion: salir")
                actual_user = None
                # Terminaremos la conexion con el servidor por simplicidad
                break
            else:
                enviar_json(sock_cliente, False)
                continue
        except:
            enviar_json(sock_cliente, False)
            continue
sock_cliente.close()
sock.close()


"""
Comentarios:
- ¿Como se podria almacenar a contraseña de forma mas segura?
- ¿Como se podria solucionar el problema de tener dos archivos con el mismo nombre  ?
- Carga y Guardar archivo (entre lineas 73 hasta 109) sacado y adaptado de
  la semana 11 del curso, en el código de envio de muchos datos:
  https://github.com/IIC2233/contenidos/blob/main/semana-11-serializacion_y_networking_2/4-networking-ejemplos.ipynb
"""