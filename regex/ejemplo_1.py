"""
Veremos como funcionan las funciones de re
"""

import re

string = "abc123"

patron_1 = r"abc"
patron_2 = r"\d*"
patron_3 = r"\w*\d*"



# Uso de match
print("########\nre.match()\n########")

print(re.match(patron_1, string))
print(re.match(patron_2, string))
print(re.match(patron_3, string))

# Uso de fullmatch
print("\n########\nre.fullmatch()\n########")

print(re.fullmatch(patron_1, string))
print(re.fullmatch(patron_2, string))
print(re.fullmatch(patron_3, string))

# Uso de search
print("\n########\nre.search()\n########")

print(re.search(patron_1, string))
print(re.search(patron_2, string))
print(re.search(patron_3, string))

# Uso de findall
print("\n########\nre.findall()\n########")

print(re.findall(patron_1, string))
print(re.findall(patron_2, string))
print(re.findall(patron_3, string))

"""
Comentarios:
- Para el patrón 2, search y findall retornan cadenas vacias
"""