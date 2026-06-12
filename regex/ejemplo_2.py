"""
Uso de expresión regular para verificar un rut:
    - A lo mas dos dígitos. El primero no puede ser 0.
    - Un punto
    - Tres dígitos
    - Un punto 
    - Tres dígitos
    - Un punto
    - Un dígito o una letra k
"""

import re

ruts = [
    "1.234.567-8",
    "9.876.543-k",
    "12.345.678-9",
    "99.999.999-k",
    "10.000.000-1",
    "45.123.456.7",
    "123.456.789.0",
    "100.000.000.k",
    "01.234.567.8",
    "09.876.543.k",
    "12.345678.9",
    "12.345.6789",
    "12345.678.9",
    "1.23.456.7",
    "1.2345.678.7",
    "12.34.567.8",
    "12.345.67.8",
    "12.345.678.a",
    "12.345.678.K",
    "12.345.678.12",
    "12.345.678.@",
    "1.23a.567.8",
    "a2.345.678.9",
    "12.34b.678.k",
    " 12.345.678.9",
    "12.345.678.9 ",
    "12. 345.678.9",
]

patron = r"[123456789]\d?\.\d{3}\.\d{3}-[\dk]"

# Se usará fullmatch. Si es que se hace con match o search se debe de especificar los limites
# correspondientes (^ y $)

for rut in ruts:
    resultado = re.fullmatch(patron, rut)
    print(rut, "valor valido" if resultado else "valor invalido")

"""
Comentarios:
    - La lista ruts fue generada por GPT-5.5 
"""