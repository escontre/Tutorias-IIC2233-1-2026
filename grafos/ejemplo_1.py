"""
Modelaremos un automata que acepte las palabras
cuya cantidad de a`s sea un multiplo de 3
    - Las palabras son compuestas por letras "a" y "b"
    - Se acepta "", "aab", "aabaabbb"
    - Se rechaza "a", "bbbbab"
"""

strings = [
    "",
    "aab",
    "aabaabbb",
    "a",
    "bbbbab"
]

# Ver dibujo en pizarra

# Simularemos el automata por medio de una lista de adyacencia
# En vez de almacenar solamente el nombre del nodo como llave, almacenaremos también lo que se lea

automata = {
    (0, "a"): 1,
    (0, "b"): 0,
    (1, "a"): 0,
    (1, "b"): 1
}

# Simulamos el Automata con los strings entregados
# Si estamos en el estado 0, la palabra cumple lo requerido. En el caso contrario no lo cumple. 

for palabra in strings:
    print(f"\n###################\nPALABRA: {palabra}\n###################\n")
    estado = 0
    for letra in palabra:
        print(f"Estoy en el estado {estado}. Estoy leyendo {letra} y me moveré a {automata[(estado, letra)]}")
        estado = automata[(estado, letra)]
    
    print("RESULTADO:", "ACEPTADO" if estado == 0 else "RECHAZADO")

"""
Comentarios:
    - ¿Tiene alguna relación con las expresiones regulares?
"""
