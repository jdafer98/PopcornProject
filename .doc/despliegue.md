# Despliegue

En este apartado se pretende explicar como se ha llevado a cabo el despliegue de la aplicación, no en uno o en dos, sino en ¡tres! sitios distintos (o al menos intentado). Pretendo de buena fe que el formato de esta documentación esté orientada a ser replicada, describiendo poco a poco y paso por paso todo el proceso detalladamente. Además como para desplegar las aplicaciónes se ha hecho uso del cli povisto por cada plataforma de despliegue, reproducir el escenario es casi tan fácil como ejecutar un script.

## Heroku

Heroku es una maravilla de plataforma. Hace el trabajo suuuuper cómodo. Ejecutar comandos dentro del servidor es tan sencillo como incluirlo dentro de un fichero procfile y la integración con git puede hacerse a través del portal web. El cli funciona super bien y es super intuitivo. Además es genial para estudiantes, ya que podemos desplegar nuestro proyecto en un dyno (hasta el nombre de los servidores es genial) que, aunque con pocas prestaciones, no caduca y nunca será necesario introducir una tarjeta de crédito. 

He seguido más o menos esta parte de la [documentación](https://devcenter.heroku.com/articles/getting-started-with-python) (que también es muy útil y muy detallada): 

1. Lo primero será disponer de una cuenta de Heroku, logicamente. Podemos registrarnos con github.

2. Ahora debemos instalar el cli de Heroku con **sudo snap install heroku --classic**

3. Ahora viene el momento de logearnos. Podemos hacer **heroku login** y se nos abrirá una pestaña en el navegador donde poner nuestro usuario y contraseña. También es posible hacer **heroku login -u <user> -p <pass>** pero ni la propia documentación de heroku lo recomienda, así que seguiremos con el plan A.

4. Ahora agarramos nuestra terminal y nos movemos a nuestro repositorio que contiene la aplicación. Ejecutamos **heroku create**. Si todo va bien, ahora se habrá creado una aplicación y se nos habrá proporcionado un magnífico dyno, pero con un nombre aleatorio. Podemos cambiarlo con **heroku apps:rename my_new_app_name**.

5. Haciendo **git push heroku master** desde el repo clonado, podemos subir los cambios a heroku. Llegados a este punto, podemos hacer **heroku open** para que se nos abra una pestaña del navegador y ver nuestra aplicación. Si nuestra aplicación no cumple los requisitos de nombres que se especifican en la documentación, lo más normal es que llegados a este punto la aplicación no se ejecute.

6. Para levantar la aplicación, debemos crear un archivo **Procfile** en la raiz de nuestro repo. Este contendrá la palabra "web: " y la orden que necesitemos para levantar la app. 
Muy importante: Si heroku no encuentra nada escuchando en el puerto que el propio heroku nos provee ($PORT), la aplicación no se buildeará. Entonces una orden que funcionaría podría ser:  **web: gunicorn --bind 0.0.0.0:$PORT <ficheroapp>:<app>**. En mi caso he agregado una tarea a mi herramienta de build (fabric) para ejecutar esa orden, y el comando en mi caso es **web: fab buildheroku**.

Con esto, sería suficiente para desplegar la aplicación. Pero nosotros queremos seguir manteniendo y actualizando nuestra aplicación, ¿verdad? Como no queremos hacer por cada **git push** a nuestro repo de github, un **git push heroku master**, optamos por sincronizar github con heroku.

Como no podría ser de otra forma, Heroku vuelve a dejar esta tarea extraordinariamente fácil. Tan solo nos movemos al apartado _deploy_, creamos un pipeline y decimos que queremos sincronizarlo con git. Cuando este listo. Quedaría así: 

![heroku1](https://github.com/jdafer98/Controv3rsial/blob/master/.doc/heroku1.png)

A partir de aquí, cada pull request hará trigger al un webhook de github, y se actualizará el repo de heroku también.

## Azure Webapps

Horrible. Totalmente nefasto. Mi experiencia no podría haber sido peor. Me fio más de hacer _port forwarding_ en mi casa que dejar que Microsoft tenga posesión de mi aplicación. Lo único que bueno, regalan 100$ a estudiantes si ingresas tu correo de la universidad así que decidí darle una oportunidad.

1. De nuevo, lo primero es disponer de una cuenta. Aquí es un poco más difícil (como el resto de cosas). Tienes primero que solicitar el plan de estudiantes poniendo el correo de la universidad, como se dijo antes (y de paso, todos tus datos personales, donde vives y casi hasta como se llama tu mascota, pero bueno...). Cuando tienes tu cuenta y un sku (en mi caso el Github Student Developer Pack), podemos empezar.

2. Lo siguiente será descargar el cli SI NO FUESE EL PEOR CLI DE LA HISTORIA DE LOS CLIs. La instalación es prácticamente automática, eso sí. **curl -sL https://aka.ms/InstallAzureCLIDeb | sudo bash**. Una vez instalado, no lo vuelvas a usar, porque prácticamente, a dia de hoy, todas las órdenes a parte de **az login** fracasan. 

3. Ahora como un humilde usuario común, accedemos al interfaz web. Nos logueamos en Azure y nos vamos a nuestro portal. Desde allí, creamos un **app service**. Nos pedirá algunos datos. Por ejemplo el grupo de recursos, el nombre de la aplicación, el lenguaje, la región, el sku... Una vez hecho esto le damos a _Aceptar_ y continuamos.

4. Ahora tenemos una webapp creada pero vacia de contentido. Para sincronizarla con github:

    4.1 Seleccionamos _Deployment center_ y clickeamos en github (otrorgando los permisos necesarios).
	![azure2](https://github.com/jdafer98/Controv3rsial/blob/master/.doc/azure2.png)

    4.2 Elegimos el sistema de buildeo. Se recomienda el motor kudu.
	![azure4](https://github.com/jdafer98/Controv3rsial/blob/master/.doc/azure4.png)

    4.3 En la configuración, seleccionamos nuestro usuario, el repo y la rama.
 	![azure5](https://github.com/jdafer98/Controv3rsial/blob/master/.doc/azure5.png)
    4.4 Le damos a aceptar. Si todo va bien, podemos acceder a la url que se nos proporciona y observamos atónitos que no ocurre **absolutamente nada**.
	![azure3](https://github.com/jdafer98/Controv3rsial/blob/master/.doc/azure3.png)


Si nuestra aplicación se llama app.py o application.py y la aplicación flask se llama app, azure debería colocarnos nuestra aplicación en un puerto. En mi caso, lo he intentado y no lo ha hecho. 

Como de todas formas no quería que sucediese automáticamente, he optado por incluir un _startup command_ en el apartado _Configuration/General Settings_. Tampoco funciona.

Si Azure no quiere arrancar mi aplicación, yo no le voy a obligar. Así que corramos un tupido velo. He querido dejar constancia de que, a pesar de no haber funcionado, si que he invertido tiempo y esfuerzo en leer documentación y probar cosas.


## OpenShift

Bastante mejor que Azure. No hay tantos recursos como heroku o Azure, pero si los suficientes para desplegar la aplicación.
Aquí las infraestructuras proporcionadas se llaman _pods_. No está al nivel de _dyno_ pero sigue siendo un nombre guay.

El unico problema es que nuestro plan solo dura 60 dias pero supongo que será suficiente para mi propósito.


1. De nuevo, tenemos que registrarnos con nuestra cuenta de redhat y se nos proporcionará un plan de 60 dias.

2. Podemos descargar el cli. Está un poco escondido. Es un ELF sencillo que puedes colocar en algún sitio especificado en la variable de entorno $PATH. Así siempre lo tienes a mano. 

![openshift1](https://github.com/jdafer98/Controv3rsial/blob/master/.doc/openshift1.png)

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
![openshift2](https://github.com/jdafer98/Controv3rsial/blob/master/.doc/openshift2.png)

5. Por úlitmo, para sincronizar con github, he seguido [este enlace](https://docs.openshift.com/container-platform/3.5/dev_guide/builds/triggering_builds.html) junto con [este video](https://www.youtube.com/watch?v=1HR0l1b9YNU).

Tenemos que usar el comando que anteriormente comenté (oc describe bc controv3rsial) y copiar el enlace de _github webhook_.

![openshift3](https://github.com/jdafer98/Controv3rsial/blob/master/.doc/openshift3.png)

Veremos que tiene un parametro "secret" en medio de la url. Este tenemos que sustituirlo por nuestro secret que se encuentra en el apartado Build/Build Configs. Tendremos que mirar en YAML y encontrar el _github webhook secret_.

Para terminar, Nos vamos a git, settings, webhooks. Creamos un nuevo webhook poniendo en el _payload_ la uri anterior con el secret sustituido y content-type: Application/json.

Cuando terminemos, cada push a nuestro repo rebuildeará nuestro despliegue en Openshift.

![openshift4](https://github.com/jdafer98/Controv3rsial/blob/master/.doc/openshift4.png)


