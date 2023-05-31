#!/bin/sh
SIAGRO_URL="http://siagro.conabio.gob.mx:3000/graphql"

curl -XPOST $SIAGRO_URL -H 'Content-Type: multipart/form-data' -F 'query=mutation { bulkAddCaracteristica_cualitativaCsv }' -F csv_file=@forma_mazorca.csv

curl -XPOST $SIAGRO_URL -H 'Content-Type: multipart/form-data' -F 'query=mutation { bulkAddCaracteristica_cualitativaCsv }' -F csv_file=@color_grano.csv

curl -XPOST $SIAGRO_URL -H 'Content-Type: multipart/form-data' -F 'query=mutation { bulkAddCaracteristica_cualitativaCsv }' -F csv_file=@color_olote.csv

curl -XPOST $SIAGRO_URL -H 'Content-Type: multipart/form-data' -F 'query=mutation { bulkAddCaracteristica_cualitativaCsv }' -F csv_file=@color_tallo.csv

curl -XPOST $SIAGRO_URL -H 'Content-Type: multipart/form-data' -F 'query=mutation { bulkAddCaracteristica_cualitativaCsv }' -F csv_file=@disp_hileras.csv

curl -XPOST $SIAGRO_URL -H 'Content-Type: multipart/form-data' -F 'query=mutation { bulkAddCaracteristica_cualitativaCsv }' -F csv_file=@tipo_grano.csv

curl -XPOST $SIAGRO_URL -H 'Content-Type: multipart/form-data' -F 'query=mutation { bulkAddCaracteristica_cualitativaCsv }' -F csv_file=@tipo_hoja.csv