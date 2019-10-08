# Troubleshooting

Si por algún casual no ha conseguido instalar Controv3rsial satisfactoriamente, puede comprobar si se siente identificado con algunos de los problemas que se describen a continuación.

## Problema relacionado con permisos en su sistema

A veces el usuario de su sistema no dispone de los permisos necesarios para instalar las dependencias de la herramienta. Para ello Controv3rsial dispone de  una solución especial para estos casos. Simplemente ejecute:

```bash
	fab userbuild
```

Compruebe si ahora la herramienta se instala correctamente.

## "No module named fabric" / "cannot import task"

Para poder construir Controv3rsial correctamente, es necesario disponer de fabric 2. Asegurese de que dispone de la última versión de fabric 2. Si es usuario de Linux, Ejecute:

```bash
	fab --version
```
y compruebe que realmente aparece fabric 2.X como salida. En caso contrario, puede ejecutar 

```bash
	sudo apt update && sudo apt upgrade
```
y posteriormente

```bash
	sudo apt install fabric
```

además recuerde que no solo es necesario tener la herramienta **fabric2** instalada, sino también las bibliotecas de python correspondientes.
Visite [este enlace](http://www.fabfile.org/) para más información.

## Otras soluciones

Si todo esto no ha resuelto su problema, existe una última solución consistente en instalar la herramienta en un entorno virtual de python preparado para este propósito. Utilizaremos para ello un entorno virtual de [pipenv](https://pipenv-es.readthedocs.io/es/latest/). Como prerequisito, se supone que python3 y pipenv se encuentran ya instalados. Ejecute:

```bash
	pip install pipenv
``` 
o

```bash
	pip install --user pipenv
``` 
En caso de fallo relacionado con permisos.

Una vez instalado, descargue los archivos pipenv y pipenv.lock que se encuentran [en el siguiente enlace](https://github.com/jdafer98/Controv3rsial/.pipenv_files).

Una vez hecho esto, arraste los archivos a la carpeta donde ha descargado previamente Controv3rsial. Dentro de esa carpeta, ejecute:

```bash
	$> pipenv sync
    (2) $> pipenv shell
	$> fab build
``` 
La herramienta debe haberse instalado satisfactoriamente. **Nota:** Si opta por esta solución, nótese que antes de volver a ejecutar la herramienta, debe volver a ejecutar "pipenv shell". Una vez en el entorno virtual, ejecutar la herramienta.





