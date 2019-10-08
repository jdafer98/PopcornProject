#Autor: Javier de Ángeles Fernández 2019
#Ordenes: 
#	fab build --> Instala todos los requisitos para que la aplicación pueda funcionar.
#	fab test --> Pasa los test correspondientes para comprobar la integridad del código.

#NOTA: Es posible que sea necesario cambiar la orden "pip install -r requirements.txt" y añadir
# "pip install --user -r requirements.txt" en caso de tener algún problema relacionado con
# permisos.

from fabric import task
from invoke import run

@task
def build(name):
	run("pip install -r requirements.txt")

@task
def test(name):
	run("pytest")



	
