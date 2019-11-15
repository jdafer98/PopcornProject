from flask import Flask, jsonify, request, Response
from encuestas import *
import os


appliaction = Flask(__name__)
enc = Encuestas()

@appliaction.route('/')
def raiz():
	return jsonify(status='OK')

@appliaction.route('/status')
def status():
	return jsonify(status='OK')

@appliaction.route('/crear_encuesta',methods=['POST'])
def ruta_crear_encuesta():
	nueva_encuesta = enc.crear_encuesta(request.form['name'])
	enc.add(nueva_encuesta)
	return jsonify(enc.encuesta2json(nueva_encuesta))

@appliaction.route('/votar', methods=['PUT'])
def ruta_votar():
	a = enc.extraer_por_hashcode(request.form['hc'])
	if a != -1:
		if int(request.form['opcion']) == 1:
			enc.votar(a,'O1')
			return jsonify(status='OK')
		elif int(request.form['opcion']) == 2:
			enc.votar(a,'O2')
			return jsonify(status='OK')
		elif int(request.form['opcion']) == 3:
			enc.votar(a,'O3')
			return jsonify(status='OK')
		elif int(request.form['opcion']) == 4:
			enc.votar(a,'O4')
			return jsonify(status='OK')
		else:
			return jsonify(error='400 INVALID OPTION'), 400
	else:
		return jsonify(error='404 NOT FOUND'), 404

@appliaction.route('/get_encuesta',methods=['GET'])
def get_encuesta():
	a = enc.extraer_por_hashcode(request.args.get('hc'))
	if a != -1:
		return jsonify(enc.encuesta2json(a))
	else:
		return jsonify(error='404 NOT FOUND'), 404

@appliaction.route('/eliminar_encuesta',methods=['DELETE'])
def eliminar_encuesta():
	a = enc.eliminar_por_hashcode(request.form['hc'])
	if a == 0:
		return jsonify(status='OK')
	else:
		return jsonify(error='404 NOT FOUND'), 404


#app.run(port=int(os.environ.get('CV3_PORT')))


