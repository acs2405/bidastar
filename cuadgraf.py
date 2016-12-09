#! /usr/bin/env python3
# -*- coding: utf-8 -*-

import bida
import math

class GrafoConPesos:
	def __init__(self, nodos, aristas, pesos, distancias, completar=False):
		self.ns = nodos
		self.arws = dict([(n, [(*ar, w) for ar, w in zip(aristas, pesos) if ar[0] == n]) for n in nodos])
		self.ws = pesos
		self.ds = distancias
		if completar:
			invs = [ar[::-1] for ar in aristas]
			self.ars.extend(invs)
			self.ws *= 2
	def h(self, nodo1, nodo2):
		if callable(self.ds):
			return self.ds(nodo1, nodo2)
		else:
			return self.ds[nodo1][nodo2]
	def aristas(self, origen): # Con pesos
		return self.arws[origen]
	def arista(self, origen, destino): # Con peso
		arws = [(*ar, w) for *ar, w in self.arws[origen] if ar[1] == destino]
		return arws[0] if arws else None
	def peso(self, origen, destino):
		ws = [w for *ar, w in self.arws[origen] if ar[1] == destino]
		return ws[0] if ws else None
	def adyacentes(self, nodo):
		return set(arw[1] for arw in self.arws[nodo])
def crear_grafo_cuadricula(M, N, fdistancia, diag=False, obsts=None):
	rM, rN = range(M), range(N)
	if not obsts:
		obsts = {}
	# Nodos:
	nodos = [(a, b) for a in rM for b in rN if (a, b) not in obsts]
	# Verticales y horizontales:
	aristas = [(n, m) for n in nodos for m in nodos if abs(n[0] - m[0]) + abs(n[1] - m[1]) == 1]
	pesos = [1 for n in nodos for m in nodos if abs(n[0] - m[0]) + abs(n[1] - m[1]) == 1]
	# Diagonales:
	if diag:
		aristas += [(n, m) for n in nodos for m in nodos if abs(n[0] - m[0]) == 1 and abs(n[1] - m[1]) == 1]
		pesos += [math.sqrt(2) for n in nodos for m in nodos if abs(n[0] - m[0]) == 1 and abs(n[1] - m[1]) == 1]
	return GrafoConPesos(nodos, aristas, pesos, fdistancia)
