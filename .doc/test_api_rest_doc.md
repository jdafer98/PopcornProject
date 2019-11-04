# Test API REST
A continuación se describen los test usados para testear la API REST. Usaremos el **Test Case** que nos proporciona Flask y para hacer las peticiones urllib. 
## Test:


```python

class MyTest(LiveServerTestCase):

	#Esta función no es un rest pero es necesario para comenzar a testear. Construye una aplicación de prueba para testeo.
	def create_app(self):
		app = Flask(__name__)
		app.config['TESTING'] = True
		app.config['LIVESERVER_PORT'] = 31416
		app.config['LIVESERVER_TIMEOUT'] = 10
		return app

	#Se lanza una peticción GET a la API rest y comprobamos el código de error.
	def test_raiz_api(self):
		response = urllib.request.urlopen(self.get_server_url())
		self.assertEqual(response.code, 200)

	#Se crea una string JSON y se parsea a datos que incluiremos en el cuerpo del paquete HTTP.
	#Luego se concatena la ruta deseada y se envia la petición. De nuevo se comprueba
	#Que la respuesta es la esperada y el código de error correcto.
 
	def test_crear_encuesta_api(self):
		values = {'name':'abc'}
		data = urllib.parse.urlencode(values)

		req = urllib.request.Request(self.get_server_url() + "/crear_encuesta",str.encode(data),method='POST')
		response = urllib.request.urlopen(req)
		data = response.read().decode('utf-8')
		data_dict = literal_eval(json.loads(data))
		temp_hashcode = data_dict['hashcode']

		#f= open("jaja","w+")		
		#f.write(data_dict['hashcode'])
		#f.close()
		self.assertEqual(response.code, 200)
	
	#Este test vuelve a ser una petición GET, pero se ve obligado primero a crear una encuesta y luego a consultarla.
	def test_get_encuesta_api(self):
		values = {'name':'xyz'}
		data = urllib.parse.urlencode(values)

		req = urllib.request.Request(self.get_server_url() + "/crear_encuesta",str.encode(data),method='POST')
		response = urllib.request.urlopen(req)
		data = response.read().decode('utf-8')
		data_dict = literal_eval(json.loads(data))
		temp_hashcode = data_dict['hashcode']




		req = urllib.request.Request(self.get_server_url() + "/get_encuesta?hc=" + temp_hashcode)
		response = urllib.request.urlopen(req)
		data = response.read().decode('utf-8')

		#f= open("jaja","w+")		
		#f.write(data)
		#f.write(temp_hashcode)
		#f.close()
		self.assertEqual(response.code, 200)

	#De nuevo, se crea una encuesta y se intenta votar una opción. Se comprueba el resultado. 
	def test_votar_api(self):
		values = {'name':'xyz'}
		data = urllib.parse.urlencode(values)

		req = urllib.request.Request(self.get_server_url() + "/crear_encuesta",str.encode(data),method='POST')
		response = urllib.request.urlopen(req)
		data = response.read().decode('utf-8')
		data_dict = literal_eval(json.loads(data))
		temp_hashcode = data_dict['hashcode']




		values = {'hc': temp_hashcode, 'opcion': 1}
		data = urllib.parse.urlencode(values)

		req = urllib.request.Request(self.get_server_url() + "/votar",str.encode(data),method='PUT')
		response = urllib.request.urlopen(req)
		data = response.read().decode('utf-8')
		data_dict = literal_eval(json.loads(data))


		self.assertEqual(response.code, 200)

	# Se crea una encuesta, se elimina y se trata de encontrar.
	def test_eliminar_encuesta(self):
		values = {'name':'xyz'}
		data = urllib.parse.urlencode(values)

		req = urllib.request.Request(self.get_server_url() + "/crear_encuesta",str.encode(data),method='POST')
		response = urllib.request.urlopen(req)
		data = response.read().decode('utf-8')
		data_dict = literal_eval(json.loads(data))
		temp_hashcode = data_dict['hashcode']


		values = {'hc': temp_hashcode}
		data = urllib.parse.urlencode(values)

		req = urllib.request.Request(self.get_server_url() + "/eliminar_encuesta",str.encode(data),method='DELETE')
		response = urllib.request.urlopen(req)
		data = response.read().decode('utf-8')
		data_dict = literal_eval(json.loads(data))


		self.assertEqual(response.code, 200)

```




