# Supervisor

Supervisor es la herramienta elegida en este proyecto para llevar a cabo el arranque y parada del servicio. A continuación se describe su configuración

## Configuración

El archivo de configuración de supervisor (acabado en .conf) contiene lo necesario para preparar el servicio con la sintaxis de supervisor, pero la verdadera funcionalidad para arrancar el servicio la posee un script adicional:

**Archivo de Configuración**
```bash
[program:cv3] #Así se declara un proceso

command=/bin/bash /home/travis/supervisor_script.sh #Llamada al script
enviroment=CV3_PORT=31416,PATH="/home/Desktop/cv3:%(ENV_PATH)s" #Ajuste de variables de entorno
file=/var/run/supervisor.sock #Un socket TCP que se utilizará como vía de comunicación con el servicio
chmod=0777
stdout_logfile = /home/travis/supervisor_out.log #Archivos de logs.
stderr_logfile = /home/travis/supervisor_err.log
```

**Script**

La funcionalidad del script es en realidad muy sencilla. Es necesario el path de gunicorn ya que la macro de gunicorn no funciona para esta órden.

```bash
export CV3_PORT=31416
sudo /home/travis/virtualenv/python3.6.7/bin/gunicorn --chdir /home/travis --bind 0.0.0.0:$CV3_PORT restapi:app
```
