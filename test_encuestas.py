#Test para la clase "Encuestas"

import json
import encuestas

#se intentan crear 10 encuestas. Cada posición de la lista 'l' es un par clave->valor.
def test_crear_encuesta():
	fields = ["titulo","hashcode","O1","O2","O3","O4"]
	test_pass = True
	l = []
	enc = encuestas.Encuestas()
	
	# Creamos 10 encuestas. Por cada encuesta que se crea, se comprueba:
	for i in range(0,10):
		l.append(enc.crear_encuesta( "titulo" + str(i) ))


		#Que todos los campos se hayan creado
		for j in range(0,len(fields)):
			if fields[j] not in l[i]:
				test_pass = False

		#Que el titulo sea el dado como argumento
		if  "titulo" + str(i) != l[i]["titulo"]:
			test_pass = False

		#Que las opciones se inicialicen a 0
		if l[i]["O1"] != 0 or l[i]["O2"] != 0 or l[i]["O3"] != 0 or l[i]["O4"] != 0:
			test_pass = False

		#Que el valor del 'hashcode' sea único en todas las encuestas creadas

		for k in range(0,len(l)):
			if l[i]["hashcode"] == l[k]["hashcode"] and i != k:
				test_pass = False

	assert test_pass

def test_votar():
	#Creamos una sola instancia de Encuestas
	enc = encuestas.Encuestas()

	#Creamos una sola encuesta esta vez
	mi_encuesta = enc.crear_encuesta( "titulo1" )
	
	#Guardo el antiguo voto
	antiguo_voto = mi_encuesta["O1"]
	
	#Voto la opción 1
	enc.votar(mi_encuesta,"O1")

	#Compruebo que la opción es un voto superior a la antigua
	assert mi_encuesta["O1"] == antiguo_voto + 1 
	
	

def test_encuesta2json():
    #Creamos una encuesta
    enc = encuestas.Encuestas()
    una_encuesta = enc.crear_encuesta("a")

    #preparamos una encuesta para ser enviada al cliente
    encuesta_preparada = enc.encuesta2json(una_encuesta)

    #comprobamos si al invertir el json, los campos coinciden
    assert una_encuesta == json.loads(encuesta_preparada)


