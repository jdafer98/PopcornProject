from fabric import task
from invoke import run

@task
def build(name):
	run("export CV3_PORT=31416")
	run("pip install -r requirements.txt")
	run("sudo mv ./controv3rsial.conf /etc/supervisor/conf.d")
@task
def buildheroku(name):
	run("gunicorn --bind 0.0.0.0:$PORT restapi:app")

@task
def builddocker(name):
	run("gunicorn --bind 0.0.0.0:$CV3_PORT restapi:app")

@task
def test(name):
	run("pytest")
@task
def start(name):
	print("Recuerda especificar un puerto en la variable de entorno mediante 'export CV3_PORT=<num_puerto>'")
	run("sudo supervisorctl reread && sudo supervisorctl reload && sudo supervisorctl start cv3")
@task
def stop(name):
	run("sudo supervisorctl stop cv3")
@task
def status(name):
	run("sudo supervisorctl status")
