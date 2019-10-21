#Módulo con la clase encuestas
import time
import json
from hashlib import md5

class Encuestas:

	lista_encuestas = []
			
	def crear_encuesta(self, titulo):
		res = {}
		
		ticks = time.time()
		hashcode = md5( str(ticks).encode('utf-8')).hexdigest()

		res["titulo"] = titulo
		res["hashcode"] = hashcode
		res["O1"] = 0
		res["O2"] = 0
		res["O3"] = 0
		res["O4"] = 0

		return res
		
	def votar(self, encuesta, opcion): 
		encuesta[opcion] += 1
		return encuesta

	def encuesta2json(self, encuesta):
		return json.dumps(encuesta)

	def add(self,e):
		self.lista_encuestas.append(e)

	def extraer_por_hashcode(self,h):
		for e in self.lista_encuestas:
			if e['hashcode'] == h:
				return e
			
		return -1

	def eliminar_por_hashcode(self,h):
		for e in self.lista_encuestas:
			if e['hashcode'] == h:
				self.lista_encuestas.remove(e)
				return 0
			
		return -1

	



