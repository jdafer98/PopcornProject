# API REST

Se presenta la API REST que hará de interfaz para clientes REST con el resto de la aplicación. En este caso, la API REST hace uso de una estructura interna de la clase que otroga la funcionalidad de encuestas pero puede sin problemas sustituirse por una BD.
A continuación se describen las rutas:

## Rutas

1. Ruta para comprobar si el servicio está online

```python
@app.route('/')
def raiz():
	return jsonify('{ "status": "OK" }')
```

2. Ruta para crear una encuesta. Solo accesible mediante POST

```python
@app.route('/crear_encuesta',methods=['POST'])
def ruta_crear_encuesta():
	nueva_encuesta = enc.crear_encuesta(request.form['name']) #Se extrae la variable name proveniente de un formulario.
	enc.add(nueva_encuesta)
	return jsonify(enc.encuesta2json(nueva_encuesta))
```

3. Votar en una encuesta. Solo accesible mediante PUT.

```python
@app.route('/votar', methods=['PUT'])
def ruta_votar():
	a = enc.extraer_por_hashcode(request.form['hc']) #Se busca la encuesta por el hashcode recivido
	if a != -1: #Si se ha encontrado, se vota la opción correspondiente o se entiende que la opción es inválida.
		if int(request.form['opcion']) == 1:
			enc.votar(a,'O1')
			return jsonify('{ "status": "200 OK" }')
		elif int(request.form['opcion']) == 2:
			enc.votar(a,'O2')
			return jsonify('{ "status": "200 OK" }')
		elif int(request.form['opcion']) == 3:
			enc.votar(a,'O3')
			return jsonify('{ "status": "200 OK" }')
		elif int(request.form['opcion']) == 4:
			enc.votar(a,'O4')
			return jsonify('{ "status": "200 OK" }')
		else:
			return jsonify('{ "error": "400 INVALID OPTION" }'), 400
	else:
		return jsonify('{ "error": "404 NOT FOUND" }'), 404

```

4. Ruta para obtener una encuesta por hashcode.

```python 
@app.route('/get_encuesta',methods=['GET'])
def get_encuesta():
	a = enc.extraer_por_hashcode(request.args.get('hc')) #Se extrae por hashcode y se devuelve
	if a != -1:
		return jsonify(enc.encuesta2json(a))
	else:
		return jsonify('{ "error": "404 NOT FOUND" }'), 404

```

5. Ruta para borrar una encuesta dado un hashcode 

```python
@app.route('/eliminar_encuesta',methods=['DELETE'])
def eliminar_encuesta():
	a = enc.eliminar_por_hashcode(request.form['hc']) #Se intenta borrar una encuesta.
	if a == 0: # Devuelve un código de error en relación a lo ocurrido.
		return jsonify('{ "status": "200 OK" }')
	else:
		return jsonify('{ "error": "404 NOT FOUND" }'), 404

```



