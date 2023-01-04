#!/bin/bash
exec >logEstatus.txt 2>&1

TODAY=`date`
echo $TODAY

echo "Empieza comparación con Zacatuche\n"

echo "Descargando csv de la instancia..." 
source vars.sh
docker exec $listadobd psql -U postgres -d $db -c "COPY agrobiodiversidads TO STDOUT WITH CSV HEADER" > ../comparaZacatuche.csv

/usr/bin/python3 estatus.py

git add logEstatus.txt
git commit -m "comparación diaria de registros"
git push 
