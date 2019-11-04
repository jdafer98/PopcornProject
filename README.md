# Controv3rsial.
Proyecto para la asignatura de Infraestructuras Virtuales.

Bajo Licencia: [![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)

Travis Build: [![Build Status](https://travis-ci.org/jdafer98/Controv3rsial.svg?branch=master)](https://travis-ci.org/jdafer98/Controv3rsial)

Circle-ci Build: [![CircleCI](https://circleci.com/gh/jdafer98/Controv3rsial.svg?style=svg)](https://circleci.com/gh/jdafer98/Controv3rsial)

Lenguaje: [![Powered by: Python](https://img.shields.io/badge/powered%20by-python-yellow)](https://www.python.org/)


## Planteamiento

El proyecto se plantea como un servicio web para realizar encuestas. Un usuario anónimo podrá comenzar una encuesta y obtener un enlace (o un token en formato de "hashcode"). Ese enlace puede ser publicado donde se desee y permite una votación anónima en la encuesta a donde dicho enlace pertenezca. Ese enlace tambíen servirá para consultar el estado de la encuesta.

En principio el cliente REST opera con la API REST anteriormente mencionada y mediante un método de HTTP, interactua con una instancia de la clase "Encuestas". Esta clase contiene toda la fucnionalidad que se espera de la aplicación, en su mayoria operaciones de inserción, consulta y borrado de la base de datos.

El lenguaje de programación elegido será **python**

## Instalación

**Nota:** La aplicación ha sido testeada en Python 3.6 y 3.7

**Prerequisitos:** Instalación del intérprete de python3, y [fabric (versión 2)](http://www.fabfile.org/).

**Instalación:**
 1. Clonar este repositorio con ```git clone``` o descargar como zip.

 2. instalar la aplicación con 

```bash
     fab build
```
 3. probar que la aplicación pasa correctamente los test con

```bash
     fab test
```

**Nota:** _fab build_ pone por defecto la variable de entorno CV3_PORT=31416. Se puede cambiar manualmente si se desea.
## Uso

Para su uso, la aplicación cuenta también con tres tareas para iniciar, parar y comprobar el estado del servicio. Estas son respectivamente:

```bash
     fab start
```

```bash
     fab stop
```

```bash
     fab status
```
Todas estas tareas funcionan como un wrapper de supervisor, el cual será instalado junto a todas las demás dependencias.

## Información totalmente irrelevante para alguien que desee usar la herramienta

**¿Quieres saber como funciona el archivo fabfile?:** [fabfile](https://github.com/jdafer98/Controv3rsial/blob/master/.doc/fabfile_doc.md)

**¿Quieres saber más acerca de la configuración de los sistemas de integración?:** [configuración_ci](https://github.com/jdafer98/Controv3rsial/blob/master/.doc/configuracion_ci.md)

**¿Quieres saber más acerca de mi API REST?:** [API REST]

**¿Quieres saber cómo ha sido testeada mi API REST?:** [test API REST]

**¿Quieres saber como ha sido configurado supervisor?** [Supervisor]



## Troubleshooting

Si encuentra algún problema con la instalación de la aplicación, puede dirigirse [aquí](https://github.com/jdafer98/Controv3rsial/blob/master/.doc/troubleshooting.md).
