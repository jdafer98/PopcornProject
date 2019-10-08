
from fabric import task
from invoke import run

@task
def build(name):
	run("pip install -r requirements.txt")

@task
def test(name):
	run("pytest")



	
