# Configuración-CI

##Breve resumen

Se han implementado dos sistemas de integración continua en el proyecto con el propósito de garantizar una correcta integración de nuevos recursos sin corromper la consistencia del proyecto. 

Travis-ci testea la aplicación en python 3.6, y Circle lo hará en python 3.7. La explicación de los archivos se encuentra a continuación.

## Travis-ci

```yaml
language: python #Especificamos el lenguaje
sudo: required #Necesario para editar y mover archivos de configuración
python:
  - 3.6 #Versiones de Python

install:
 #PARTE DE INSTALACIÓN DE REQUISITOS
  - pip install --upgrade pip
  - pip install -r requirements.txt
  - sudo apt-get install supervisor
 #COLOCAMOS LOS ARCHIVOS NECESARIOS EN SU SITIO
  - sudo mv ./controv3rsial.conf /etc/supervisor/conf.d
  - sudo mv ./supervisor_script.sh /home/travis
  - sudo cp ./restapi.py /home/travis
  - sudo cp ./encuestas.py /home/travis
  - pip install --upgrade pytest
 #LEEMOS EL ARCHIVO DE CONFIGURACIÓN Y ARRANCAMOS EL SERVICIO
  - sudo supervisorctl reread
  - sudo supervisorctl reload
 #HACEMOS SLEEP PARA QUE CARGUE POR COMPLETO EL STATUS
  - sleep 3
  - sudo supervisorctl status
  - sleep 3
 #HACEMOS UN CAT DE LOS LOGS PARA FACILITAR LA DEPURACIÓN
  - sudo find / -name gunicorn
  - sudo cat /home/travis/supervisor_out.log
  - sudo cat /home/travis/supervisor_err.log

 #SE PASAN TODOS LOS TEST CON EL SERCICIO ACTIVO
script: pytest
```

## Circle-ci

```yaml
version: 2 #Especificamos la versión de Circle
jobs: #Nos basta con una tarea. En realidad no necesitamos concurrencia de momento...
  build:
    docker:
      - image: circleci/python:3.7 #Levantaremos un contenedor Docker con python 3.7

    working_directory: ~/repo #Importante especificar un wd para que no se lie buscando cosas

    steps: # Abrimos una rama
      - checkout
      - run: #Instalamos pip y pytest en su última versión
          name: Instalar dependencias
          command: |
            python3 -m venv venv
            pip install --user pytest
            . venv/bin/activate

      # Step 3: Correr test #Corremos nuestros maravitupendos test
      - run:
          name: run tests
          command: |
            . venv/bin/activate
            pytest 
```

**NOTA IMPORTANTE** Circle-CI No se usa para testear la API REST.

