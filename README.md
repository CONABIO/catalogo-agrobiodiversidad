*Log de actualizaciones a la lista de taxones de agrobiodiversidad, mantenida por SIAgro.*

* Para acceder a la [instancia](https://siagro.conabio.gob.mx/listado_agrobiodiversidad): https://siagro.conabio.gob.mx/listado_agrobiodiversidad

# Archivos que se pueden encontrar en el repositorio:
* **history.md:**
  Histórico de cambios de la instancia de agrobiodiversidad
* **changelog.md:**
  Resumen de cambios de la instancia de agrobiodiversidad
* **scripts/:**
  En esta carpeta se encuentran distintos archivos para realizar la comparación entre registros de ayer y hoy en la base de datos de catalogo-agrobiodiversidad, así como los scripts necesarios para realizar la validación de campos entre Zacatuche y nuestra base de datos: 
  * **compareZacatuche.sh:**
    Script que corre en automático todos los días a las 20:00 horas para revisar si hay modificaciones entre nuestra base de datos y Zacatuche. 
  * **estatus.py:**  
    Realiza la comparación entre zacatuche y catalogo-agrobiodiversidad. Si detecta cambios se realizan las modificaciones directamente a la base de datos de catalogo-agrobiodiversidad.
  * **actualizaciones_agro.sh:**
    Script que corre en automático todos los días a las 20:30 horas para revisar si hay modificaciones en los datos con ayuda de compare.py y sube esas modificaciones al repositorio.
  * **compare.py:**
    Realiza la comparación del último csv generado contra el csv anterior
  * **functions.py**
    Contiene las funciones necesarias para los scripts en python.
  * **logfile.txt:**
    Logs del script actualizaciones_agro.sh
  * **logEstatus.txt:**
    Logs del script compareZacatuche.sh
