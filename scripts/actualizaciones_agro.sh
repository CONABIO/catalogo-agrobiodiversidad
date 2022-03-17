#!/bin/sh
exec >scripts/logfile.txt 2>&1

TODAY=`date`
echo $TODAY

echo "Empieza validación de actualizaciones diarias\n"
echo "Cambiando nombre de archivos..."
mv agro_actual.csv agro_anterior.csv 
echo "Descargando archivo nuevo..." 
#SE LE TIENE QUE QUITAR EL -it
docker exec etiqueta-postgres psql -U postgres -d zendro_development -c "COPY agrobiodiversidads TO STDOUT WITH CSV HEADER" > agro_actual.csv
#echo "Comparando archivos..."
/usr/bin/python3 compare.py
cp /home/vbass/etiquetas/etiquetas/graphql-server/history.txt ./history.md
cp /home/vbass/etiquetas/etiquetas/graphql-server/changelog.txt ./changelog.md
echo "git add history.md changelog.md"
/usr/bin/git add history.md changelog.md
echo "git commit"
/usr/bin/git commit -m "validacion diaria de registros"
echo "git push"
/usr/bin/git push 
echo "Proceso terminado!"
/usr/bin/git add scripts/logfile.txt
echo "git commit"
/usr/bin/git commit -m "validacion diaria de registros"
echo "git push"
/usr/bin/git push 
