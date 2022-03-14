#!/bin/sh
exec >logfile.txt 2>&1
echo "Empieza validación de actualizaciones diarias\n"
echo "Cambiando nombre de archivos..."
mv agro_actual.csv agro_anterior.csv 
echo "Descargando archivo nuevo..." 
#SE LE TIENE QUE QUITAR EL -it
docker exec etiqueta-postgres psql -U postgres -d zendro_development -c "COPY agrobiodiversidads TO STDOUT WITH CSV HEADER" > agro_actual.csv
echo "Comparando archivos..."
/usr/bin/python3 compare.py
echo "git add history.txt"
/usr/bin/git add history.txt
echo "git commit"
/usr/bin/git commit -m "validacion diaria de registros"
echo "git push"
/usr/bin/git push 
echo "Proceso terminado!"