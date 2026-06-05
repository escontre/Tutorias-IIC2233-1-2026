"""
Servidor creado para manejar los a partir de la palabra del dia
"""

from flask import Flask, request, jsonify
import json
import random

def guardar_datos(contenido):
    with open("data.json", "w") as archivo:
        json.dump(contenido, archivo, indent=4)

def cargar_datos():
    with open("data.json", "r") as archivo:
        return json.load(archivo)
    
palabras = ["AYUDA", "PERRO", "JUGOS", "SIETE", "CORTA", "ZUMBA", "LECHE"]
PALABRA = random.choice(palabras)
app = Flask("wordle IIC2233 - Server")

# Endpoint encargado de retornar las respuestas correctas e incorrectas
@app.route("/try", methods = ["GET"])
def responder_intento():
    try:
        # Se espera que el body tenga la llave try
        body = request.get_json(force=True)
        if "try" not in body or type(body["try"]) != str or len(body["try"]) != 5:
            return jsonify({"error": "invalid format"}), 401
        if not body["try"].isalpha():
            return jsonify({"error": "use alpha characters"}), 401
        
        body["try"] = body["try"].upper()

        # Hacemos dos pasadas
        # La primera: ubicamos todas las letras bien ubicadas
        intento = dict()
        letras_restantes = list(PALABRA)
        for i in range(5):
            letra = body["try"][i]
            if PALABRA[i] == letra:
                intento[i] = {
                    "letter" : letra,
                    "color" : "green"
                }

                letras_restantes[i] = None

        # La segunda: ubicamos todas las letras mal ubicadas o que no estan
        for i in range(5):
            if i in intento:
                continue

            letra = body["try"][i]

            if letra in letras_restantes:
                intento[i] = {
                    "letter" : letra,
                    "color" : "yellow"
                }

                letras_restantes[letras_restantes.index(letra)] = None

            else:
                intento[i] = {
                    "letter" : letra,
                    "color" : "grey"
                }
        # Retorna la palabra y el resultado del intento
        return jsonify({
            "state" : "solved" if PALABRA == body["try"] else "unsolved",
            "try": body["try"],
            "check": intento
        })
    except: 
        return jsonify({"error": "server error"}), 500

# Endpoint encargado de ertornar la palabra correcta
# SIMPLIFICACION: Como ya se descubrio la palabra, entonces se cambia a nivel
# de servidor
@app.route("/result", methods = ["GET"])
def responder_respuesta():
    global PALABRA
    try:
        respuesta = jsonify({"word": PALABRA})
        PALABRA = random.choice(palabras)
        return respuesta
    except:
        return jsonify({"error": "server error"}), 500


if __name__ == "__main__":
    app.run(host="localhost", port=4444)


"""
Comentarios:
    - Falta agregar lógica de cambiar la palabra cada dia :)
    - Se podría agregar la lógica de usuario para almacenar los intentos
"""