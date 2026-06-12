# Comentarios Grafos y algoritmos
## Grafos
- Grafos no dirigidos permiten unir dos nodos de forma bidireccional, mientras que los no dirigidos tienen uniones unidireccionales
- Representaciones: 
    * Lista de adyacencia: diccionario que asocia como llave el nodo y como valor una lista de todos los nodos vecinos
    * Matriz de adyacencia: matriz A (lista de listas) de 0's y 1's de dimensión N x N (con N la cantidad de nodos). Si A[i][j] = 1, entonces hay una arista del nodo i al nodo j. 

## BFS Y DFS
- Busqueda por amplitud y busqueda en profundidad
- DFS se puede implementar con colas FIFO (stack) Y BFS se puede implementar con colas FILO (deque)