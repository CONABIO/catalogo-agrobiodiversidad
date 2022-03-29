#!/bin/sh
exec >scripts/logEstatus.txt 2>&1

TODAY=`date`
echo $TODAY

echo "Empieza comparación con Zacatuche\n"

echo "Descargando csv de la instancia..." 
docker exec -it etiqueta-postgres psql -U postgres -d zendro_development -c "COPY agrobiodiversidads TO STDOUT WITH CSV HEADER" > comparaZacatuche.csv

/usr/bin/python3 estatus.py

git add scripts/logEstatus.txt
git commit -m "comparación diaria de registros"
git push 
