*Log de actualizaciones a la lista de taxones de agrobiodiversidad, mantenida por SIAgro.*

* Para acceder a la [instancia](https://siagro.conabio.gob.mx/listado_agrobiodiversidad): https://siagro.conabio.gob.mx/listado_agrobiodiversidad

# Archivos que se pueden encontrar en el repositorio:
* **history.md:**
  Histórico de cambios de la instancia de agrobiodiversidad
* **changelog.md:**
  Resumen de cambios de la instancia de agrobiodiversidad
* **scripts/:**
  En esta carpeta se encuentran 3 archivos: 
  * **actualizaciones_agro.sh:**
    Script que corre en automático todos los días a las 20:00 horas para revisar si hay modificaciones en los datos con ayuda de compare.py y sube esas modificaciones al repositorio.
  * **compare.py:**
    Realiza la comparación del último csv generado contra el csv anterior
  * **logfile.txt:**
    Logs del script actualizaciones_agro.sh

