# Despliegue de contenedor Docker

En este apartado se pretende explicar como se ha llevado a cabo el despliegue de un contenedor Docker que aisla la aplicación y la prepara de forma automática para su despliegue. En este caso hemos elegido dos plataformas para su despliegue: Heroku y Azure.

## Preparación del contenedor

lo primero que tendremos que hacer será preparar una imagen de Docker donde se ejecutará nuestra aplicación. Como imagen base, se usará **python:alpine-3.7**. La elección deriva de la recomendación del profesor de la asignatura como imagen extremadamente ligera, sobria y sin sobrecarga de aplicaciones inecesarias. Al principio encontré [esta](https://hub.docker.com/_/alpine?tab=description). Pero no traía python instalado. Antes de instalarlo, buscando por internet veia que la gente que usaba alpine para correr una aplicación con python, utilizaban la imagen [python](https://hub.docker.com/_/python) con el tag alpine. Al final cambié, aunque tuve que instalar bastantes cosas porque apenas trae cosas de serie (ni siquiera gcc).


Lo primero, como no podria ser de otra forma, es crear un **Dockerfile** y un **.dockerignore** para establecer las reglas de construcción, y para no levantar un contenedor con archivos que no queremos que estén. En concreto el **Dockerfile** tendrá la siguente forma (basado en el Dockerfile de [python](https://hub.docker.com/_/python) , principalmente):

```yaml

#Imagen elegida
FROM python:3.7-alpine

#Exponemos un puerto del contenedor al exterior
EXPOSE $CV3_PORT

#Añadimos un directorio de trabajo:
WORKDIR /usr/src/app

#Copiamos el requirements.txt de nuestro pc al contenedor.
COPY requirements.txt ./

#Acutalizamos apk
RUN apk update
RUN apk upgrade

#Instalamos dependencias (La mayoria son dependencias de fabric. Por ejemplo, paramiko necesita gcc y algunas otras librerias como limits.h)
RUN apk add musl-dev libffi-dev openssl-dev python3-dev make gcc
RUN apk add bash
RUN pip install -r requirements.txt

#Copiamos el resto de archivos
COPY . .

#Ejecutamos un nuevo task de fabric llamado buildocker
CMD fab builddocker

```



## Heroku



## Azure Webapps

Horrible. Totalmente nefasto. Mi experiencia no podría haber sido peor. Me fio más de hacer _port forwarding_ en mi casa que dejar que Microsoft tenga posesión de mi aplicación. Lo único que bueno, regalan 100$ a estudiantes si ingresas tu correo de la universidad así que decidí darle una oportunidad.

1. De nuevo, lo primero es disponer de una cuenta. Aquí es un poco más difícil (como el resto de cosas). Tienes primero que solicitar el plan de estudiantes poniendo el correo de la universidad, como se dijo antes (y de paso, todos tus datos personales, donde vives y casi hasta como se llama tu mascota, pero bueno...). Cuando tienes tu cuenta y un sku (en mi caso el Github Student Developer Pack), podemos empezar.

2. Lo siguiente será descargar el cli SI NO FUESE EL PEOR CLI DE LA HISTORIA DE LOS CLIs. La instalación es prácticamente automática, eso sí. **curl -sL https://aka.ms/InstallAzureCLIDeb | sudo bash**. Una vez instalado, no lo vuelvas a usar, porque prácticamente, a dia de hoy, todas las órdenes a parte de **az login** fracasan. 

3. Ahora como un humilde usuario común, accedemos al interfaz web. Nos logueamos en Azure y nos vamos a nuestro portal. Desde allí, creamos un **app service**. Nos pedirá algunos datos. Por ejemplo el grupo de recursos, el nombre de la aplicación, el lenguaje, la región, el sku... Una vez hecho esto le damos a _Aceptar_ y continuamos.

4. Ahora tenemos una webapp creada pero vacia de contentido. Para sincronizarla con github:

    4.1 Seleccionamos _Deployment center_ y clickeamos en github (otrorgando los permisos necesarios).
	![azure2](https://github.com/jdafer98/Controv3rsial/blob/master/.doc/despliegue_imagenes/azure2.png)

    4.2 Elegimos el sistema de buildeo. Se recomienda el motor kudu.
	![azure4](https://github.com/jdafer98/Controv3rsial/blob/master/.doc/despliegue_imagenes/azure4.png)

    4.3 En la configuración, seleccionamos nuestro usuario, el repo y la rama.
 	![azure5](https://github.com/jdafer98/Controv3rsial/blob/master/.doc/despliegue_imagenes/azure5.png)
    4.4 Le damos a aceptar. Si todo va bien, podemos acceder a la url que se nos proporciona y observamos atónitos que no ocurre **absolutamente nada**.
	![azure3](https://github.com/jdafer98/Controv3rsial/blob/master/.doc/despliegue_imagenes/azure3.png)


Si nuestra aplicación se llama app.py o application.py y la aplicación flask se llama app, azure debería colocarnos nuestra aplicación en un puerto. En mi caso, lo he intentado y no lo ha hecho. 

Como de todas formas no quería que sucediese automáticamente, he optado por incluir un _startup command_ en el apartado _Configuration/General Settings_. Tampoco funciona.

Si Azure no quiere arrancar mi aplicación, yo no le voy a obligar. Así que corramos un tupido velo. He querido dejar constancia de que, a pesar de no haber funcionado, si que he invertido tiempo y esfuerzo en leer documentación y probar cosas.


## OpenShift

Bastante mejor que Azure. No hay tanta documentación como con heroku o Azure, pero si la suficiente para desplegar la aplicación.
Aquí las infraestructuras proporcionadas se llaman _pods_. No está al nivel de _dyno_ pero sigue siendo un nombre guay.

El unico problema es que nuestro plan solo dura 60 dias pero supongo que será suficiente para mi propósito.


1. De nuevo, tenemos que registrarnos con nuestra cuenta de redhat y se nos proporcionará un plan de 60 dias.

2. Podemos descargar el cli. Está un poco escondido. Es un ELF sencillo que puedes colocar en algún sitio especificado en la variable de entorno $PATH. Así siempre lo tienes a mano. 

![openshift1](https://github.com/jdafer98/Controv3rsial/blob/master/.doc/despliegue_imagenes/openshift1.png)

3. Este cli funciona genial. Los comandos a ejecutar vendrían a ser:
```bash
	oc login /url/
```

url es una url que se puede encontrar haciendo click en nuestro nombre de usuario, en la sección "Copy login command".

```bash
oc new-project controv3rsial

oc new-app python~https://github.com/jdafer98/Controv3rsial.git --name controv3rsial
```

con estos dos comandos, hemos creado un proyecto y una aplicación dentro de él. Notese que aunque hayamos introducido el repo de github, este será de donde se extraigan los archivos pero no estará sincronizado con el (aún).

```bash
oc expose svc/controv3rsial
```
Este último comando solo sirve para exponer la url al exterior.

```bash
oc start-build controv3rsial

oc describe bc controv3rsial
```

Por último estos dos comandos nos serán útiles. El primero sirve para arrancar una build en openshift y el segundo nos dará información, entre la que se puede encontrar el uri de los **webhooks** de github, que usaremos más adelante.

4. Siendo python, si tu fichero aplicación se llama "wsgi.py", y el nombre de tu aplicación flask "application", muy amablemente Openshift levantará la aplicación por tí. Si no deseas esto, puedes seguir [este enlace](https://docs.openshift.com/container-platform/3.3/dev_guide/deployments/basic_deployment_operations.html#executing-commands-inside-a-container-deployments) en el apartado "Executing Commands Inside a Container". Básicamente lo que tenemos que hacer es irnos al apartado "Workload"/"Deploy config" y modificar el YAML de nuestra app. 

Hay que añadir un apartado _command_ debajo de spec, tal y como dice el enlace.
![openshift2](https://github.com/jdafer98/Controv3rsial/blob/master/.doc/despliegue_imagenes/openshift2.png)

5. Por úlitmo, para sincronizar con github, he seguido [este enlace](https://docs.openshift.com/container-platform/3.5/dev_guide/builds/triggering_builds.html) junto con [este video](https://www.youtube.com/watch?v=1HR0l1b9YNU).

Tenemos que usar el comando que anteriormente comenté (oc describe bc controv3rsial) y copiar el enlace de _github webhook_.

![openshift3](https://github.com/jdafer98/Controv3rsial/blob/master/.doc/despliegue_imagenes/openshift3.png)

Veremos que tiene un parametro "secret" en medio de la url. Este tenemos que sustituirlo por nuestro secret que se encuentra en el apartado Build/Build Configs. Tendremos que mirar en YAML y encontrar el _github webhook secret_.

Para terminar, Nos vamos a git, settings, webhooks. Creamos un nuevo webhook poniendo en el _payload_ la uri anterior con el secret sustituido y content-type: Application/json.

Cuando terminemos, cada push a nuestro repo rebuildeará nuestro despliegue en Openshift.

![openshift4](https://github.com/jdafer98/Controv3rsial/blob/master/.doc/despliegue_imagenes/openshift4.png)


