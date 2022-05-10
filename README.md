* Para acceder a la [instancia](https://siagro.conabio.gob.mx/listado_agrobiodiversidad): https://siagro.conabio.gob.mx/listado_agrobiodiversidad

# Scripts de validación

Para mantener al día la base de datos del Listado de agrobiodiversidad, se cuenta con una serie de scripts desarrollados en Python que realizan la detección de cambios tanto en el SNIB como en la misma base de datos. 

## Comparación del listado contra el SNIB
El script [compareZacatuche.sh](https://github.com/CONABIO/catalogo-agrobiodiversidad/blob/main/scripts/compareZacatuche.sh) se ejecuta todos los días a las 20:15 horas. Descarga la información que hay en el Listado en un archivo .csv y realiza la comparación de lo que hay en la base de datos del Listado contra lo que hay en el SNIB con ayuda del script [estatus.py](https://github.com/CONABIO/catalogo-agrobiodiversidad/blob/main/scripts/estatus.py).
* Si encuentra cambios entre las dos bases realiza los respectivos cambios directamente en la base del listado.
* Si por alguna razón se cuenta con un ID que no se encuentre en el SNIB manda un correo a Alicia Mastretta, Vivian Bass e Irene Ramos para dar seguimiento.
* Los logs del script se encuentran en [logEstatus.txt](https://github.com/CONABIO/catalogo-agrobiodiversidad/blob/main/scripts/logEstatus.txt).

## Histórico de cambios en la base de datos del Listado
El script [actualizaciones_agro.sh](https://github.com/CONABIO/catalogo-agrobiodiversidad/blob/main/scripts/actualizaciones_agro.sh) se ejecuta todos los días a las 20:00 y 20:30 horas. Primero descarga lo que hay al día de hoy en la base de datos del Listado y posteriormente realiza una comparación de dos archivos .csv con ayuda del script [compare.py](https://github.com/CONABIO/catalogo-agrobiodiversidad/blob/main/scripts/compare.py) y [functions.py](https://github.com/CONABIO/catalogo-agrobiodiversidad/blob/main/scripts/functions.py):
* El primero es la información que había en el listado al día de ayer
* El segundo es la información que hay en el listado al día de hoy

El script identifica los registros borrados, agregados y editados y guarda un registro de los cambios en dos archivos:
* **[history.md](https://github.com/CONABIO/catalogo-agrobiodiversidad/blob/main/history.md):**
  Contiene el histórico a detalle de todos los cambios que se realizan en la instancia: agregar, editar o eliminar registros.
* **[changelog.csv](https://github.com/CONABIO/catalogo-agrobiodiversidad/blob/main/changelog.md):**
  Contiene el resumen de los cambios.

En ambos scripts se detecta quién realizó los respectivos cambios a los registros.
Los logs del script se encuentran en [logfile.txt](https://github.com/CONABIO/catalogo-agrobiodiversidad/blob/main/scripts/logfile.txt).


