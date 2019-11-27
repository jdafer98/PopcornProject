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

Podemos testear nuestro contenedor buildeando la imagen con **docker build -t <nombre:etiqueta>**
Y después correrla, o bien haciendo otro yml para docker-compose, o bien simplemente haciendo docker run dando valor a la variable de entorno (-e) y conectando el puerto del contenedor con la máquina (-p). Es posible que una vez ejecutado no queremos que se quede parado y guardado. Ponemos entonces el flag --rm.

En nuestro caso, el puerto 31416 del contenedor se conecta al puerto 31416 del host. 

```bash
sudo docker run -e CV3_PORT=31416 -p 31416:$CV3_PORT --rm controv3rsial
```
Si comprobamos que todo es correcto y que el contenedor tiene el comportamiento esperado, toca desplegarlo.

## DockerHub

Es interesante subir nuestra imagen a dockerhub con la intención de desplegar automáticamente desde aquí, a la plataforma que hallamos elegido. Siguiendo principalmente [la documentación oficial](https://docs.docker.com/docker-hub/repos/) se procede como sigue:

1. Creamos una cuenta de DockerHub si no tenemos ya una.

2. Accedemos al portal web (solo la primera vez, para crear el recurso). Nos encontramos algo como esto:

![Docker-1](https://github.com/jdafer98/Controv3rsial/blob/master/.doc/despliegue_imagenes/Docker-1.png)

    2.1 Le damos a **Create Repository**.
    2.2 Creamos un repositorio público normal y corriente.
![Docker-2](https://github.com/jdafer98/Controv3rsial/blob/master/.doc/despliegue_imagenes/Docker-2.png)

    2.3 Sería interesante conectarlo con git en la opción de build. Seguimos [este enlace](https://docs.docker.com/docker-hub/builds/)
![Docker-3](https://github.com/jdafer98/Controv3rsial/blob/master/.doc/despliegue_imagenes/Docker-3.png)

    2.4 Autorizamos DockerHub a acceder a nuestro repo.

![Docker-4](https://github.com/jdafer98/Controv3rsial/blob/master/.doc/despliegue_imagenes/Docker-4.png)

    2.5 Y nuestro recurso quedaría así.

![Docker-5](https://github.com/jdafer98/Controv3rsial/blob/master/.doc/despliegue_imagenes/Docker-5.png)

    2.6 En la configuración, enlazamos a nuestro repo

![Docker-6](https://github.com/jdafer98/Controv3rsial/blob/master/.doc/despliegue_imagenes/Docker-6.png)

    2.7 A partir de aquí, con cada push de github, la imagen se buildea como contenedor
![Docker-7](https://github.com/jdafer98/Controv3rsial/blob/master/.doc/despliegue_imagenes/Docker-7.png)




## Heroku

Mi intención para desplegar en Heroku, era hacerlo a través de DockerHub, sin embargo me ha sido casi imposible encontrar documentación acerca de como conectar esos dos recursos. Siguiendo [este enlace](https://devcenter.heroku.com/categories/deploying-with-docker), he conseguido hacerlo desde github a heroku.

Lo primero, sería crear un fichero heroku.yml que bastaría con que contenga lo siguiente:

```yaml
build:
  docker:
    web: Dockerfile
```
En realidad, es el mismo heroku.yml que se encuentra en el enlace anterior, pero sin la sección "run". Eso es debido a que si no se pone esa sección, se ejecuta el CMD del Dockerfile, que es precisamente lo que queremos.

a partir de aquí, tabajaremos con el CLI de Heroku.

hacemos **heroku login** como hicimos para desplegar la aplicación en el PaaS y hacemos **heroku create <nuevo_nombre>** para crear otro recurso. **NOTA:** he tenido problemas para logearme por un error hacerca de un "secret_service" o algo así. Encontré en una discusión de git que el error se solucionaba renombrando un archivo con otro nombre para que heroku lo creara de nuevo. Algo así como:

```bash
sudo mv docker-credential-secretservice docker-credential-secretservice_SAVE
```



Una vez creado, tenemos que cambiar la fuente remota a la del nuevo recurso. Sino todas las operaciones las realizaremos sobre la aplicación que desplegamos anteriormente y no sobre este nuevo recurso. Para ello:

```bash
heroku git:remote -a <nuevo_nombre>
```

A continuación cambiamos el "stack" de heroku-18 (Default) a container con:

```bash
heroku stack:set container
```

Luego debemos usar un comando especial para subir los cambios a heroku que parece no ser necesario para la corrección así que no voy a comentarlo.

Todavía nos queda sincronizar la aplicación con git. Tendríamos que hacer exactamente lo que hicimos para la aplicación en el PaaS. Dejo captura:

![Docker-8](https://github.com/jdafer98/Controv3rsial/blob/master/.doc/despliegue_imagenes/Docker-8.png)



## Azure Webapps

La razón de escoger esta vez Azure, en lugar de otra plataforma, es precisamente que he leido que está bastante acondicionado para desplegar contenedores, y que se puede hacer de forma muy sencilla para desplegar desde dockerhub. Me hubiese gustado posteriormente desplegar en OpenShift pero ya si que no me daba tiempo. Tengo mucha carga externa a la asignatura.


Dicho esto, la forma de desplegar en Azure desde DockerHub, es muy similar a desplegar una aplicación normal.

1. Creamos un _App service_, pero esta vez decimos que nuestro despliegue es un contenedor, no código:

![adocker-1](https://github.com/jdafer98/Controv3rsial/blob/master/.doc/despliegue_imagenes/adocker-1.png)

2. En las opciones del contenedor, Cambiamos a DockerHub, y ponemos nuestra ruta. Hay una errata que corregí posteriormente. La etiqueta es latest y no lastest (porque viene de late, no de last. Fallo mio).

![adocker-2](https://github.com/jdafer98/Controv3rsial/blob/master/.doc/despliegue_imagenes/adocker-2.png)

3. Cuando aceptamos, realmente se buildea y se levanta el contenedor. Sorprende que sea tan sencillo pero es así. 




