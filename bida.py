#! /usr/bin/env python3
# -*- coding: utf-8 -*-

import math
from collections import OrderedDict
#import argparse

class ListaNodos:
	def __init__(self, n_attrs, order=None, listas=None):
		self.nodos = [] # Números de nodos
		#self.attrs = [] if listas == None else listas[1] # Tuplas de cosas
		self.data = dict()
		self.order = order
		self.n_attrs = n_attrs
	def get(self, n):
		try:
			return self.data[n]
		except KeyError:
			return None
	def put(self, x):
		if not self.push(x):
			self.replace(x)
	def put_ordered(self, x):
		i = self.index_of(x[0])
		if i != -1:
			del self.nodos[i]
			del self.data[x[0]]
		self.insert_ordered(x)
	def insert_ordered(self, x):
		assert(len(x) == self.n_attrs + 1)
		if self.has(x[0]):
			return False
		else:
			self.data[x[0]] = x
			i = 0
			f = self.order
			for nodo in self:
				if f(x, nodo) < 0:
					self.nodos.insert(i, x[0])
					break
				i += 1
			if i == len(self.nodos):
				self.nodos.append(x[0])
			return True
	def push(self, x):
		assert(len(x) == self.n_attrs + 1)
		if self.has(x[0]):
			return False
		else:
			self.data[x[0]] = x
			self.nodos.append(x[0])
			return True
	def pop(self):
		n = self.nodos.pop()
		return self.data.pop(n)
	def unshift(self, x):
		assert(len(x) == self.n_attrs + 1)
		if self.has(x[0]):
			return False
		else:
			self.data[x[0]] = x
			self.nodos.insert(0, x[0])
			return True
	def shift(self):
		n = self.nodos.pop(0)
		return self.data.pop(n)
	def replace(self, x):
		assert(len(x) == self.n_attrs + 1)
		self.data[x[0]] = x
	def first(self):
		return self.data[self.nodos[len(self.nodos) - 1]]
	def last(self):
		return self.data[self.nodos[0]]
	def push_all(self, l2):
		anadidos = 0
		for n, attr in zip(l2.nodos, l2.attrs):
			x = attr
			if self.push(x):
				anadidos += 1
			else:
				self.replace(x)
		return anadidos
	def copy(self):
		l2 = ListaNodos(self.n_attrs)
		l2.nodos = self.nodos.copy()
		l2.data = self.data.copy()
		return l2
	def is_empty(self):
		return len(self.nodos) <= 0
	def index_of(self, n):
		try:
			return self.nodos.index(n)
		except ValueError:
			return -1
	def has(self, n):
		return n in self.data
	def clear(self):
		self.nodos.clear()
		self.data.clear()
	def __iter__(self):
		return self.__next__()
	def __next__(self):
		for n in self.nodos:
			yield self.data[n]
class BIDA:
	def __init__(self, G=None, d=2):
		self.d = d # Profundidad del perímetro
		self.G = G # GrafoConPesos
	def set_G(self, G):
		self.G = G
	def set_d(self, d):
		self.d = d
	def generar_perimetro(self, fin):
		# Perímetro: lista de nodos (n, camino, coste, h(m, fin))
		order_per = lambda nodo1, nodo2: nodo1[3] - nodo2[3]
		A = ListaNodos(3, order=order_per) # Ad
		A.push((fin, [], 0, 0))
		P = A.copy()
		ants = []
		for i in range(self.d):
			P_ = ListaNodos(3, order=order_per)
			for n1, cam1, cost1, hfin in P:
				arws = self.G.aristas(n1)
				for arw in arws:
					n2, w = arw[1:]
					if n2 in ants:
						continue
					new2 = (n2, [n1] + cam1, cost1 + w, self.G.h(fin, n2))
					nodo2 = A.get(n2)
					if nodo2:
						if cost1 + w < nodo2[2] or cost1 + w == nodo2[2] and nodo2[3] < nodo2[3]:
							A.replace(new2)
							P_.replace(new2)
					else:
						A.put_ordered(new2)
						P_.put_ordered(new2)
			ants = P.nodos
			P = P_
		self.P = P
		return A, P
	def hd(n1, G, P):
		#h_hs = [(self.G.h(n1, n2) + h2, self.G.h(n1, n2) + cost) for n2, cam, cost, h2 in P]
		h_min, hs_min = [], []
		for n2, cam, cost, h2 in P:
			h12 = G.h(n1, n2)
			h_min.append(h12 + h2)
			hs_min.append(h12 + cost)
		#for i in range(len(h_hs)):
		#	
		return min(h_min), min(hs_min)
	def buscar_camino(self, ini, fin):
		A, P = self.generar_perimetro(fin) #(n, camino, coste, h)
		hs = dict()
		for n in self.G.ns:
			hs[n] = BIDA.hd(n, self.G, P)
		nodoini = A.get(ini)
		if nodoini:
			return [ini] + nodoini[1], nodoini[2], []
		order_L = lambda nodo1, nodo2: (nodo1[4]) - (nodo2[4])
		L = ListaNodos(4, order_L) #(n, g, hd, camino, f)
		nodos_fin = ListaNodos(3) #(n, fd, camino, f)
		for np, cam, cost, hfin in P:
			nodos_fin.push((np, float('inf'), None, float('inf')))
		h_hd_ini = hs[ini]
		nodo_ini = (ini, 0, h_hd_ini[1], [], 0 + h_hd_ini[0])
		L.push(nodo_ini)
		H = L.first()[2]
		estudiados = list()
		over = list()
		found = False
		#print("\n"*30)
		#print("Init  (H=%5.2f)" % H)
		while True:
			while not L.is_empty():
				n, g, hd, cam, f = L.shift()
				fd = g + hd
				estudiados.append(n)
				if P.has(n):
					nodo_n = nodos_fin.get(n)
					if fd < nodo_n[1] or fd == nodo_n[1] and f < nodo_n[3]:
						new_fin = (n, g + P.get(n)[2], cam + [n] + P.get(n)[1][:], f)
						nodos_fin.replace(new_fin)
						found = True
						#print(" - Consigo (nodo de perímetro) %s: %s" % (str(n), str(new_fin[1:])))
					#else:
					#	print(" - Descarto (nodo de perímetro) %s: %s" % (str(n), str((g + P.get(n)[2], cam + [n] + cam_fin, f))))
				else:
					ars = self.G.aristas(n)
					#print(ars)
					cam2 = cam + [n]
					if n == (6, 8) and H >= 30:
						pass
					for n, n2, w in ars:
						if n2 not in estudiados:
							g2 = g + w
							h2, hd2 = hs[n2]
							fd2 = g2 + hd2
							f2 = g2 + h2
							if fd2 <= H:
								nodo2 = L.get(n2)
								new2 = (n2, g2, hd2, cam2, f2)
								if nodo2:
									if fd2 < nodo2[1] + nodo2[2]: # or fd2 == nodo2[1] + nodo2[2] and f2 < nodo2[4]:
										L.put_ordered(new2)
										#print(" - Reemplazo %s: %s" % (str(n2), str(new2[1:])))
								else:
									L.insert_ordered(new2)
									#print(" - Añado %s: %s" % (str(n2), str(new2[1:])))
							else:
								over.append(fd2)
								#print(" - Descarto %s: %s" % (str(n2), str((g2, hd2, cam2, f2))))
			# Condicion de salida:
			if not over or found: # Fin
				#print("End   (H=%5.2f)" % H)
				break
			else: # Empezar de nuevo
				H = min(over)
				#print("Again (H=%5.2f)" % H)
				L.clear()
				L.push(nodo_ini)
				over = list()
				estudiados = list()
				continue
		min_f, min_fd = float("inf"), float("inf")
		min_cam = None
		for n, fd, cam, f in nodos_fin:
			if fd < min_fd or fd == min_fd and f < min_f:
				min_cam = cam
				min_f, min_fd = f, fd
		self.estudiados = estudiados
		self.camino = min_cam
		self.coste = min_fd 
		return min_cam, min_fd, estudiados
	def __call__(self, ini, fin):
		return self.buscar_camino(ini, fin)
