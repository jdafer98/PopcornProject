# Provisionamiento

En este apartado se pretende explicar el proceso seguido para realizar el provisionamiento de una máquina virtual, donde partiendo de una máquina recién creada somos capaces de proveerla con todo lo necesario para poder correr nuestra aplicación (incluyendo los propios archivos de la apliación).

## Elección del SO

Una práctica interesante antes de meternos de cabeza en el provisionamiento de una máquina virtual, será elegir que máquina virtual queremos provisionar. 

Buscando en internet recomendaciónes y _benchmarks_ de rendimiento, me he topado con [esto](https://www.phoronix.com/scan.php?page=article&item=8way-amd-rome&num=5)

En el enlace podemos ver varios test pasados a las distribuciones más populares de Linux. No había un test específico para servicio web, pero observando los resultados más relevantes (entre los que se encuentra el _average_), mis mejores opciones serían pues Ubuntu 19 o Debian 10. En concreto Debian parece que da un rendimiento ligeramente mejor así que me he decantado por ella.

## Alojamiento

Otra duda que se me plantea es si voy a provisionar mi máquina en local o en la nube. Quizás en local hubiese sido lo más sencillo ya que utilizar virtualbox para conectarlo con el host no es muy conplejo y es rápido. Sin embargo soy consciente de que posteriormente tendré que provisionar una máquina en la nube y convenía ir practicando ya.

Mi licencia de OpenShift caducará dentro de poco, no he conseguido que el cli de Azure funcione correctamente y Heroku no parece que sea una plataforma muy usada para máquinas virtuales en concreto. He tenido que elegir entre la plataforma de Amazon o Google Cloud. Esta última me ha sido recomendada así que le he dado una oportunidad.

## Provisionamiento

En este caso, usaremos como herramienta **ansible**. No necesariamente por ser la mejor, pero es fácil encontrar recursos para ella y hemos visto algo sobre ella en otra asignatura así que servirá para mi propósito. 

Me he apoyado en general con [este enlace](https://cloud.google.com/compute/docs/quickstart-linux)
Partiendo de una cuenta en Google Cloud, procedemos de la siguente forma:

1. Vamos al apartado de Compute Engine y creamos una Máquina Virtual.

![gce1](https://github.com/jdafer98/Controv3rsial/blob/master/.doc/despliegue_imagenes/gce-1.png)

2. Seleccionamos el sistema operativo que nos convenga (Debian 10, en mi caso). 

![gce2](https://github.com/jdafer98/Controv3rsial/blob/master/.doc/despliegue_imagenes/gce-2.png)

3. Cuando creemos la máquina, será importante para el provisionamiento intercambiar un par de claves con ella. En mi caso, he seguido [Este video](https://www.youtube.com/watch?v=S2MocgFZMPU).

	en resumen, utilizamos ssh-keygen para generar un par de claves y copiamos la pública en la sección correspondiente de nuestra máquina.

![gce3](https://github.com/jdafer98/Controv3rsial/blob/master/.doc/despliegue_imagenes/gce-3.png)

Teóricamente, podemos conectarnos a la máquina por _raw ssh_ así:

```bash

ssh -i .ssh/cv3gce -o UserKnownHostsFile=/dev/null -o CheckHostIp=no -o StrictHostKeyChecking=no <usuario>@<ip>

```

Una vez hecho esto tenemos una máquina operativa, pero sin nada dentro. Vamos a usar **ansible** con la siguiente configuración (siguiendo los propios apuntes de la asignatura)

 - ansible.cnf lo hemos dejado por defecto

 - Hemos añadido:
	```
		#Infraestructuras virtuales - Controv3rsial
		[Controv3rsial]
		104.155.126.134
	```
   al archivo de hosts.

 - Como playbook, nos hemos inspirado en diversas fuentes como [esta](https://www.tutorialspoint.com/ansible/ansible_playbooks.htm) o [esta otra](https://docs.ansible.com/ansible/latest/network/getting_started/first_playbook.html) u otras varias de internet tratando de hacer un collage que se ajuste a nuestras necesidades.

Cada task es bastante autodescriptivo:

```yaml

- hosts: all #solo tenemos un grupo creado. Solo se invoca a ese
  remote_user: user1 #así se llama mi usuario de la máquina

  tasks: #Tareas en orden

  - name: Actualizar apt
    become: true #para ejecutar el task con privilegios
    command: sudo apt-get update

  - name: Instalar Python
    become: true
    apt: pkg=python3.7 state=present

  - name: Instalar pip3
    become: true
    command: sudo apt-get -y install python3-pip

  - name: Instalar Git
    become: true
    command: sudo apt-get install -y git

  - name: Instalar Fabric #Importante para ejecutar posteriormente el gestor de tareas
    become: true
    command: pip3 install fabric

  - name: Instalar Supervisor
    become: true
    command: pip3 install supervisor

  - name: Clonar repo
    git: repo=https://github.com/jdafer98/Controv3rsial.git dest=controv3rsial/

  - name: Buildeo
    command: pip3 install -r controv3rsial/requirements.txt

```

Se ha añadido un nuevo task:

```python

@task
def provide(name):
	run("ansible-playbook playbook_cv3.yml")

```

al gestor de tareas para recoger de forma centralizada el proceso.

Al correr el task, resulta así:

![ansible](https://github.com/jdafer98/Controv3rsial/blob/master/.doc/despliegue_imagenes/ansible.png)


