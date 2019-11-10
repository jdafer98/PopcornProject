from fabric import task
from invoke import run

@task
def build(name):
	run("export CV3_PORT=31416")
	run("pip install -r requirements.txt")
	run("sudo mv ./controv3rsial.conf /etc/supervisor/conf.d")
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
