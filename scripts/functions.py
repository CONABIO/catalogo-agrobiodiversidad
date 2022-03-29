import pandas as pd
import numpy as np
from datetime import datetime,timedelta
import json
import requests
import smtplib 
import os
import paths

def getDate(date,hrs):
    '''
    Convierte la fecha de la base de datos de zendro a nuestra zona horaria
    '''
    date = date.split("+")

    if '.' in str(date):
        date = datetime.strptime(date[0], "%Y-%m-%d %H:%M:%S.%f" )
    else:
        date = datetime.strptime(date[0], "%Y-%m-%d %H:%M:%S" )

    date = date-timedelta(hours = int(hrs))
    date = str(date.year) + '-'+ str(date.month) + '-'+ str(date.day)
    return date


def getHeader(df):
    '''
    Obtiene el header para el history.md dependiendo el dataframe que se reciba.
    Se eliminan las columnas createdAt y updatedAt y se devuelve el header completo de la tabla.    
    '''
    header = ' | '.join(df.columns)
    header = '| '+header+' |'
    header = header.replace("| createdAt ","")
    header = header.replace("| updatedAt ","")

    separator = '| -- |'
    for i in range(len(df.columns)-3):
        separator = separator + ' -- |'

    header = header + '\n' + separator + '\n'

    return header 


def getInfo(df,i):
    '''
    Obtiene la información del registro dependiendo el dataframe que se reciba.
    Se eliminan las columnas createdAt y updatedAt y se devuelve la información de ese registro.    
    '''
    info = "| "

    for j in range(len(df.columns)):
        if j == 1 or j == 2:
            continue

        column = df.columns[j]
        info = info + str(df[column][i]) + ' | '
    
    return info


def getInfoTaxon(id):
    '''
    Hace una consulta a zacatuche para obtener la información que se necesita de un id.
    Devuelve un json con la información solicitada en la query.
    '''
    query = """query taxon{
                dwcTaxon(taxonID:"""+"\""+id+"\""+"""){
                            id
                            taxonomicStatus
                            scientificName
                            acceptedNameUsage{
                            id
                            scientificName
                            }
                        }
                        }"""

    r = requests.post(paths.zacatuche, json={'query': query})
    json_data = json.loads(r.text)
    df_data = json_data['data']['dwcTaxon']

    return df_data

def updateLocal(id,taxon="",estatus="",id_valido="",taxon_valido="",referencia="",categoria_agrobiodiversidad="",subcategoria_agrobiodiversidad="",justificacion_subcategoria="",comentarios_revision="",usuario="Bot validación"):
    '''
    Realiza las modificaciones en la base de catalogo-agrobiodiversidad de los campos que se le pasen como parámetro.
    '''
    
    list=[id,taxon,estatus,id_valido,taxon_valido,referencia,categoria_agrobiodiversidad,subcategoria_agrobiodiversidad,justificacion_subcategoria,comentarios_revision,usuario]
    listAux=['id','taxon','estatus','id_valido','taxon_valido','referencia','categoria_agrobiodiversidad','subcategoria_agrobiodiversidad','justificacion_subcategoria','comentarios_revision','usuario']
    search=""
    for i in range(len(list)):
        if list[i]:            
            if list[i] == "NULL":
                search=search+str(listAux[i])+":\" \" "
                continue
            

            search=search+str(listAux[i])+": \""+str(list[i])+"\" "      

    query = """mutation{
                updateAgrobiodiversidad("""+ search +"""){
                    id
                }
                }"""
    #print(query)
    r = requests.post(paths.siagro, json={'query': query})
    json_data = json.loads(r.text)


def addLocal(id,taxon="",estatus="",id_valido="",taxon_valido="",referencia="",categoria_agrobiodiversidad="",subcategoria_agrobiodiversidad="",justificacion_subcategoria="",comentarios_revision="",usuario="Bot validación"):
    '''
    Agrega un registro a la base de catalogo-agrobiodiversidad con los campos que se le pasen como parámetro.
    '''
    list=[id,taxon,estatus,id_valido,taxon_valido,referencia,categoria_agrobiodiversidad,subcategoria_agrobiodiversidad,justificacion_subcategoria,comentarios_revision,usuario]
    listAux=['id','taxon','estatus','id_valido','taxon_valido','referencia','categoria_agrobiodiversidad','subcategoria_agrobiodiversidad','justificacion_subcategoria','comentarios_revision','usuario']
    search=""

    for i in range(len(list)):
        if list[i]:
            search=search+str(listAux[i])+": \""+str(list[i])+"\" "      

    query = """mutation{
                addAgrobiodiversidad("""+ search +"""){
                    id
                }
                }"""
    #print(query)
    r = requests.post(paths.siagro, json={'query': query})
    json_data = json.loads(r.text)


def sendeMail(string):
    '''
    Envía un correo a las direcciones en "destinatario". Recibe como parámetro el id al que se le necesita dar seguimiento.
    '''
    remitente = "SIAgro <siagro@siagro.conabio.gob.mx>" 
    #destinatario = ["Vivian <vivbass4@gmail.com>", "Vivian <vbass@conabio.gob.mx>", "Alicia <amastretta@conabio.gob.mx>", "Irene <iramos@conabio.gob.mx>"]
    destinatario = ["Vivian <vivbass4@gmail.com>", "Vivian <vbass@conabio.gob.mx>"]
    asunto = "Aviso: no se encontró ID de taxon" 
    mensaje = """En la validación diaria de registros entre Zacatuche con nuestra base de datos de catalogo-agrobiodiversidad, se detectó que el ID """+str(string)+""", no se encontró en Zacatuche. Favor de dar seguimiento al caso.
    
------------------------------------
Este correo ha sido enviado automáticamente. Favor de no responder."""
    email = 'Subject: {}\n\n{}'.format(asunto, mensaje)
    try: 
        smtp = smtplib.SMTP('localhost') 
        smtp.sendmail(remitente, destinatario, email.encode("utf8")) 
        print("Correo enviado")
    except: 
        print("""Error: el mensaje no pudo enviarse. 
        Compruebe que el mensaje no tenga acentos""")