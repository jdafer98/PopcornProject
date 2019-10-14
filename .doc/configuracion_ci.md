# Configuración-CI

##Breve resumen

Se han implementado dos sistemas de integración continua en el proyecto con el propósito de garantizar una correcta integración de nuevos recursos sin corromper la consistencia del proyecto.

Travis-ci testea la aplicación en python 3.6, y Circle lo hará en python 3.7. La explicación de los archivos se encuentra a continuación.

## Travis-ci

```yaml
language: python #Especificamos el lenguaje
python:  #y la versión
  - 3.6

before_install: #Antes de la instalación nos aseguramos de que esté instalado pip en su última versión
  - pip install --upgrade pip
install: #Instalamos pytest en su última versión
  - pip install --upgrade pytest

script: pytest #ejecutamos pytest en la raiz pytest
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
