"""
Crearemos una API la cual maneje datos de mascotas.
Dentro de las funcionalidades tendremos:
    - Obtener, borrar por indice.
    - Obtener todas las mascotas.
    - Crear un registro de mascota.
"""
# Importamos las librerias
from flask import Flask, request, jsonify
import json

# Creamos funciones para guardar y cargar datos
def guardar_datos(contenido):
    with open("data.json", "w") as archivo:
        json.dump(contenido, archivo, indent=4)

def cargar_datos():
    with open("data.json", "r") as archivo:
        return json.load(archivo)
    
# Creamos la instancia
app = Flask("mascotAPI")

# Por medio de este ENDPOINT vamos a obtener todas las mascotas
# o crear una nueva mascota
@app.route("/mascotas", methods = ["GET", "POST"])
def obtener_o_crear_mascotas():
    # Retornaremos todas las mascotas
    if request.method == "GET":
        data = cargar_datos()
        return jsonify(data["mascotas"])

    # Crearemos una entrada a partir de la información en el body
    if request.method == "POST":
        data = cargar_datos()
        body = request.get_json(force=True) 

        # Se verifica si todos los campos están
        campos = ["nombre", "dueno", "raza", "edad"]
        for atributo in campos:
            if atributo not in body:
                return jsonify({"mensaje" : "Campos erroneos"}), 404
        if type(body["edad"]) != int:
            return jsonify({"mensaje": "Los tipos de dato no son correctos"}), 404
        
        # Guardamos y retornamos
        body["id"] = data["meta"]["index_count"] + 1
        data["meta"]["index_count"] += 1
        data["mascotas"].append(body)
        guardar_datos(data)
        return jsonify(body), 201

# Por medio de este ENDPOINT DINAMICO vamos a poder obtener a una
# mascota o poder borrarla por medio de su ID
@app.route("/mascotas/<int:id>", methods = ["GET", "DELETE"])
def buscar_o_borrar_mascota(id):
    # Se obtiene el usuario por medio del id en el endpoint
    if request.method == "GET":
        data = cargar_datos()
        for mascota in data["mascotas"]:
            if mascota["id"] == id:
                return jsonify(mascota)
        return jsonify({"mensaje": "No se encontro la mascota"}), 404
    # Se borra el usuario por medio del id en el endpoint
    if request.method == "DELETE":
        data = cargar_datos()
        indice_lista = 0
        for mascota in data["mascotas"]:
            if mascota["id"] != id:
                indice_lista += 1
                continue
            data["mascotas"].pop(indice_lista)
            guardar_datos(data)
            return "", 204  # Codigo 204 no envia nada. Solo el status_code
        return jsonify({"mensaje": "No se encontro la mascota"}), 404

if __name__ == "__main__":
    app.run(host="localhost", port=4444)

"""
Comentarios:
    - El crear y borrar son operaciones sensibles.
        ¿Que deberiamos hacer para proteger la información?
    - No estan todas las verificaciones
    - data.json fue generado por GPT-5.3 mini.
"""
