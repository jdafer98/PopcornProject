import urllib.request
import json
from ast import literal_eval
from flask import Flask
from flask_testing import LiveServerTestCase



class MyTest(LiveServerTestCase):


	def create_app(self):
		app = Flask(__name__)
		app.config['TESTING'] = True
		app.config['LIVESERVER_PORT'] = 31416
		app.config['LIVESERVER_TIMEOUT'] = 10
		return app

	def test_raiz_api(self):
		response = urllib.request.urlopen(self.get_server_url())
		self.assertEqual(response.code, 200)

	def test_status_api(self):
		response = urllib.request.urlopen(self.get_server_url() + "/status")
		self.assertEqual(response.code, 200)

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

	def test_votar_api(self):
		values = {'name':'xyz'}
		data = urllib.parse.urlencode(values)

		req = urllib.request.Request(self.get_server_url() + "/crear_encuesta",str.encode(data),method='POST')
		response = urllib.request.urlopen(req)
		data = response.read().decode('utf-8')
		data_dict = json.loads(data)
		temp_hashcode = data_dict['hashcode']




		values = {'hc': temp_hashcode, 'opcion': 1}
		data = urllib.parse.urlencode(values)

		req = urllib.request.Request(self.get_server_url() + "/votar",str.encode(data),method='PUT')
		response = urllib.request.urlopen(req)
		data = response.read().decode('utf-8')
		data_dict = literal_eval(json.loads(data))


		self.assertEqual(response.code, 200)

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
		data_dict = json.loads(data)


		self.assertEqual(response.code, 200)

