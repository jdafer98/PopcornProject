#Módulo con la clase encuestas
import time
import json
from hashlib import md5

class Encuestas:
			
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
