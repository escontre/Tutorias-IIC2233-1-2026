"""
Crearemos un generador y veremos como se recorre
"""
# Creamos nuestro generador
def mi_generador():
    valor = 1
    print("GENERADOR - Inicio")
    yield valor 

    valor = 2
    print("GENERADOR - Entrando al loop")
    yield valor
    while valor < 10:
        valor += 1 
        print("GENERADOR - En el loop...")
        yield valor
    print("GENERADOR - Salí del loop!")


# # Creamos un objeto generador a partir de mi_generador
# x = mi_generador()

# #Recorreremos el objeto y veamos que imprime 

# for _ in range(5):
#     valor = next(x)
#     print(f"El valor es {valor}")

# # Se pueden recorrer por medio de un ciclo for! 

y = mi_generador()

for i in y:
    print(i)

# Salta error si es que se intenta sacar otro elemento del iterador
next(y)