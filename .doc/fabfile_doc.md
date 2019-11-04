# Fabfile

## ¡Hay un sucio fichero fabfile en mi proyecto!

¡Así es, pequeño individuo! Pero no se apure. Está aquí para ayudarle. Fab es una herramenta de ejecución de tareas remota (normalmente, sobre ssh). En este caso, se utilizará fab a modo de herramienta de construcción del proyecto en la máquina de un usuario que desee utilizarla.
Fab se desarrolla por encima de invoke (para ejecución de comandos) y paramiko (para establecer conexiones). 
Podemos por tanto importar paquetes de ambos si lo deseamos.

Reitero: **Este código funciona si la versión 2 de fabric está instalada.** No quiero ver caras raras, muecas de espanto ni gestos de desprecio porque la herramienta no es capaz de instalarse. A llorar se va a la llorería.


El esquema es el que sigue:

```python

from fabric import task #Task para hacer tareas que se dispararán con el uso de la herramienta (fab <task>).
from invoke import run #Ejecución de comandos

@task #Un task o tarea que queremos que se ejecute con la herramienta. Un decorador.
def build(name): #Una pequeña función que se ejecuta cuando se dispara el task
	run("pip install -r requirements.txt") # Y la acción que se requiere

@task
def userbuild(name):
	run("pip install --user -r requirements.txt")

@task
def test(name):
	run("pytest")


@task
def start(name): #Comienza el servicio
	print("Recuerda especificar un puerto en la variable de entorno mediante 'export CV3_PORT=<num_puerto>'")
	run("sudo supervisorctl reread && sudo supervisorctl reload")
@task
def stop(name): #detiene el servicio
	run("sudo supervisorctl stop cv3")
@task
def status(name): #Estado del servicio
	run("sudo supervisorctl status")
```

   **build** es la construcción estándar. Otra versión de esta **userbuid** , la cual instala el proyecto en el espacio del usuario que ejecuta pip. Suele resolver problemas relacionados con permisos. Por último, **test** corre los test que vienen de serie con la herramienta para comprobar que todo anda bien. Es opcional.


