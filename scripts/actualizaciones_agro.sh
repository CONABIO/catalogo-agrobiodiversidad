#!/bin/bash
exec >logfile.txt 2>&1

TODAY=`date`
echo $TODAY

echo "Empieza validación de actualizaciones diarias\n"
echo "Cambiando nombre de archivos..."
mv ../agro_actual.csv ../agro_anterior.csv 
echo "Descargando archivo nuevo..." 
source vars.sh
docker exec $listadobd psql -U instancia_listado -d $db -c "COPY agrobiodiversidads TO STDOUT WITH CSV HEADER" > ../agro_actual.csv
/usr/bin/python3 compare.py
echo "git add history.md changelog.md"
echo "git commit"
echo "git push"
echo "Proceso terminado!"
/usr/bin/git add ../history.md ../changelog.csv logfile.txt
/usr/bin/git commit -m "validacion diaria de registros"
/usr/bin/git push 


