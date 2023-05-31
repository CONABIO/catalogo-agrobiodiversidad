#!/bin/sh
SIAGRO_URL="http://maices-siagro.conabio.gob.mx:4600/graphql"

# echo "Uploading cualitative characteristics ..."

# echo "Color de grano"
# curl -XPOST $SIAGRO_URL -H 'Content-Type: multipart/form-data' -F 'query=mutation { bulkAddCaracteristica_cualitativaCsv }' -F csv_file=@color_grain.csv

# echo "Color de olote"
# curl -XPOST $SIAGRO_URL -H 'Content-Type: multipart/form-data' -F 'query=mutation { bulkAddCaracteristica_cualitativaCsv }' -F csv_file=@color_olote.csv

# #echo "Color de tallo"
# #curl -XPOST $SIAGRO_URL -H 'Content-Type: multipart/form-data' -F 'query=mutation { bulkAddCaracteristica_cualitativaCsv }' -F csv_file=@color_tallo.csv

# echo "Dispo hile"
# curl -XPOST $SIAGRO_URL -H 'Content-Type: multipart/form-data' -F 'query=mutation { bulkAddCaracteristica_cualitativaCsv }' -F csv_file=@dispo_hil.csv

# echo "Forma mazorca"
# curl -XPOST $SIAGRO_URL -H 'Content-Type: multipart/form-data' -F 'query=mutation { bulkAddCaracteristica_cualitativaCsv }' -F csv_file=@form_mazorca.csv

# echo "Tipo grano"
# curl -XPOST $SIAGRO_URL -H 'Content-Type: multipart/form-data' -F 'query=mutation { bulkAddCaracteristica_cualitativaCsv }' -F csv_file=@type_grain.csv

# #echo "Tipo hoja"
# #curl -XPOST $SIAGRO_URL -H 'Content-Type: multipart/form-data' -F 'query=mutation { bulkAddCaracteristica_cualitativaCsv }' -F csv_file=@tipo_hoja.csv



echo "Uploading cuantitative characteristics ..."

echo "Altura planta"
curl -XPOST $SIAGRO_URL -H 'Content-Type: multipart/form-data' -F 'query=mutation { bulkAddCaracteristica_cuantitativaCsv }' -F csv_file=@altura_planta.csv--

echo "Anchura grano"
curl -XPOST $SIAGRO_URL -H 'Content-Type: multipart/form-data' -F 'query=mutation { bulkAddCaracteristica_cuantitativaCsv }' -F csv_file=@anchura_grano.csv--

echo "Diametro mazorca"
curl -XPOST $SIAGRO_URL -H 'Content-Type: multipart/form-data' -F 'query=mutation { bulkAddCaracteristica_cuantitativaCsv }' -F csv_file=@diametro_mazorca.csv--

echo "Diametro olote"
curl -XPOST $SIAGRO_URL -H 'Content-Type: multipart/form-data' -F 'query=mutation { bulkAddCaracteristica_cuantitativaCsv }' -F csv_file=@diametro_olote.csv--

echo "Granos por hilera"
curl -XPOST $SIAGRO_URL -H 'Content-Type: multipart/form-data' -F 'query=mutation { bulkAddCaracteristica_cuantitativaCsv }' -F csv_file=@granos_hilera.csv--

echo "Grosor grano"
curl -XPOST $SIAGRO_URL -H 'Content-Type: multipart/form-data' -F 'query=mutation { bulkAddCaracteristica_cuantitativaCsv }' -F csv_file=@grosor_grano.csv--

echo "Hileras mazorca"
curl -XPOST $SIAGRO_URL -H 'Content-Type: multipart/form-data' -F 'query=mutation { bulkAddCaracteristica_cuantitativaCsv }' -F csv_file=@hileras_mazorca.csv--

echo "Longitud grano"
curl -XPOST $SIAGRO_URL -H 'Content-Type: multipart/form-data' -F 'query=mutation { bulkAddCaracteristica_cuantitativaCsv }' -F csv_file=@longitud_grano.csv--

echo "Longitud mazorca"
curl -XPOST $SIAGRO_URL -H 'Content-Type: multipart/form-data' -F 'query=mutation { bulkAddCaracteristica_cuantitativaCsv }' -F csv_file=@longitud_mazorca.csv--

echo "Mazorca por planta"
curl -XPOST $SIAGRO_URL -H 'Content-Type: multipart/form-data' -F 'query=mutation { bulkAddCaracteristica_cuantitativaCsv }' -F csv_file=@mazorca_planta.csv--

echo "Peso seco"
curl -XPOST $SIAGRO_URL -H 'Content-Type: multipart/form-data' -F 'query=mutation { bulkAddCaracteristica_cuantitativaCsv }' -F csv_file=@peso_seco.csv--

echo "Volumen grano"
curl -XPOST $SIAGRO_URL -H 'Content-Type: multipart/form-data' -F 'query=mutation { bulkAddCaracteristica_cuantitativaCsv }' -F csv_file=@volumen_grano.csv--


#echo "Uploading metodos ..."

#curl -XPOST $SIAGRO_URL -H 'Content-Type: multipart/form-data' -F 'query=mutation { bulkAddMetodoCsv }' -F csv_file=@metodos_procesado.csv


