#! /usr/bin/env python3
# -*- coding: utf-8 -*-

from cuadgraf import crear_grafo_cuadricula
from bida import BIDA
from time import time
import hashlib
import json
import argparse
import math
import sys

parser = argparse.ArgumentParser(description="Programa de pruebas del algoritmo BIDA* sobre cuadrículas", prog="pruebas-bida")
parser.add_argument("M", nargs="?", metavar="NUM", type=int, default=10, help="Nº de columnas")
parser.add_argument("N", nargs="?", metavar="NUM", type=int, default=10, help="Nº de filas")
parser.add_argument("-d", dest="d", metavar="NUM", type=int, default=10, help="Distancia de perímetro")
parser.add_argument("-D", "--diagonal", dest="diag", action="store_true", help="También en diagonal")
#parser.add_argument("-g", "--gen", dest="generar_grafo", action="store_true", help="Generar grafo")
parser.add_argument("-i", "-0", "--ini", nargs=2, dest="ini", type=int, default=None, help="Nodo inicial")
parser.add_argument("-f", "-1", "--fin", nargs=2, dest="fin", type=int, default=None, help="Nodo final")
parser.add_argument("-o", "--obsts", nargs='+', dest="obsts", type=int, default=None, help="Nodos obstáculo")
args = parser.parse_args(sys.argv[1:])

def imprimir_camino(M, N, ini, fin, objres=None, obstaculos=None):
	cuadricula = [[' ' for i in range(M)] for j in range(N)]
	car_obst = '#'
	car_path = 'o'
	car_est  = '·'
	car_per  = '+'
	if obstaculos:
		for i, j in obstaculos:
			cuadricula[j][i] = car_obst
	if objres:
		if objres.estudiados:
			for i, j in objres.estudiados:
				cuadricula[j][i] = car_est
		for i, j in objres.P.nodos:
			cuadricula[j][i] = car_per
		if objres.camino:
			for i, j in objres.camino:
				cuadricula[j][i] = car_path
	cuadricula[ini[1]][ini[0]] = 'X'
	cuadricula[fin[1]][fin[0]] = 'Y'
	print()
	print(' ' + car_obst + ' ' + ' '.join([car_obst for i in range(M)]) + ' ' + car_obst)
	for fila in cuadricula:
		print(' ' + car_obst + ' ' + ' '.join(fila) + ' ' + car_obst)
	print(' ' + car_obst + ' ' + ' '.join([car_obst for i in range(M)]) + ' ' + car_obst)
	print()
if __name__ == "__main__":
	#M, N = 34, 11
	#d = 10
	#diag = True
	ini = tuple(args.ini) if args.ini else (0, 0)
	fin = tuple(args.fin) if args.fin else (args.M - 1, args.N - 1)
	if args.obsts and len(args.obsts) > 1:
		obsts = set((args.obsts[i], args.obsts[i+1]) for i in range(0, len(args.obsts), 2))
	else:
		obsts = {}
	#	obsts = {(9, i) for i in range(0, 9)} | {(4, i) for i in range(2, 11)} | {(i, 2) for i in range(2, 8)} | {(i, 8) for i in range(7, 12)} # Casillas obstáculo
	distancias_G = lambda nodo1, nodo2: math.sqrt((nodo2[0] - nodo1[0])**2 + (nodo2[1] - nodo1[1])**2)
	G = crear_grafo_cuadricula(args.M, args.N, distancias_G, args.diag, obsts)
	bida = BIDA(G, args.d)
	t0 = time()
	path, cost, studied = bida.buscar_camino(ini, fin)
	t1 = time()
	imprimir_camino(args.M, args.N, ini, fin, bida, obsts)
	print("Coste del camino:    %11.6f casillas" % (cost))
	print("Coste del algoritmo: %11.6f s" % ((t1 - t0)))