# bidastar
BIDAd* algorythm implementation on Python

El algoritmo está en bida.py, para el que se crea un objeto de la clase BIDA con un grafo y una distancia de perímetro (d) como parámetros. El grafo se crea con cuadgraf.py, creando un objeto de clase GrafoConPesos, al que se le introducen los parámetros nodos (lista de nodos del grafo), aristas (lista de pares [tuplas] de nodos), pesos (lista de pesos: a la arista i le corresponde el peso i), distancias (función que a partir de dos nodos devuelve su distancia aérea) y completar (true si sólo se han introducido aristas en una dirección y se quiere completar con la otra dirección, false por defecto).

pruebas.py devuelve gráficamente el camino que se ha calculado entre dos puntos de una cuadrícula configurable y su coste:

usage: pruebas.py [-h] [-d NUM] [-D] [-i INI INI] [-f FIN FIN]
                    [-o OBSTS [OBSTS ...]]
                    [NUM] [NUM]

Programa de pruebas del algoritmo BIDA* sobre cuadrículas

positional arguments:
  NUM                   Nº de columnas
  NUM                   Nº de filas

optional arguments:
  -h, --help            show this help message and exit
  -d NUM                Distancia de perímetro
  -D, --diagonal        También en diagonal
  -i INI INI, -0 INI INI, --ini INI INI
                        Nodo inicial
  -f FIN FIN, -1 FIN FIN, --fin FIN FIN
                        Nodo final
  -o OBSTS [OBSTS ...], --obsts OBSTS [OBSTS ...]
                        Nodos obstáculo

Ejemplos:

$ ./pruebas.py 15 15 -i 0 7 -f 14 2

 # # # # # # # # # # # # # # # # #
 #             +                 #
 #           +                   #
 # · · · · +                 o Y #
 # · · · · · +             o o   #
 # · · · · · · +         o o     #
 # · · · · · · · +     o o       #
 # · · · · · · · · + o o         #
 # X o o o o o o o o o           #
 # · · · ·             +         #
 #                       +       #
 #                         +     #
 #                           +   #
 #                             + #
 #                               #
 #                               #
 # # # # # # # # # # # # # # # # #

Coste del camino:      19.000000 casillas
Coste del algoritmo:    0.009994 s


$ ./pruebas.py 11 11 -d 2 -o 1 1 1 2 2 1 1 3 1 4 1 5 1 6 1 7 1 8 1 9 3 1 4 1 5 1 6 1 7 1 8 1 9 1 9 2 9 3 9 4 9 5 9 6 9 7 2 9 3 9 4 9 5 9 6 9 7 9 5 2 5 3 5 4 5 5 5 6 5 7 4 7 3 7 2 5 3 5 4 3 3 3 9 8 9 9 7 8 7 7 7 6 7 5 7 4 7 3 -D -f 4 2

 # # # # # # # # # # # # #
 # X · · · · · · · · · · #
 # o # # # # # # # # # · #
 # o #   o Y # · o · # · #
 # o # o # # # o # o # · #
 # o #   o   # o # o # · #
 # o # # # o # o # o # · #
 # o # · o   # o # o # · #
 # o # o # # # o # o # · #
 # o # · o o o · # o # · #
 # o # # # # # # # o # · #
 # · o o o o o o o · · · #
 # # # # # # # # # # # # #

Coste del camino:      43.556349 casillas
Coste del algoritmo:    0.015336 s

