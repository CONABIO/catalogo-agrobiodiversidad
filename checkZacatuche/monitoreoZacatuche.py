import pandas as pd
import numpy as np
from datetime import datetime,timedelta
import json
import requests
import smtplib 
import os
from paths import *

def sendeMail(string,destinatario):
    '''
    Envía un correo a las direcciones en "destinatario". 
    '''
    remitente = "SIAgro <siagro@siagro.conabio.gob.mx>" 
    asunto = "Monitoreo Zacatuche" 
    mensaje = string+"""
    
------------------------------------
Este correo no contiene acentos y ha sido enviado automaticamente. Favor de no responder."""
    email = 'Subject: {}\n\n{}'.format(asunto, mensaje)
    try: 
        smtp = smtplib.SMTP('localhost') 
        smtp.sendmail(remitente, destinatario, email.encode("utf8")) 
        print("Correo enviado")
    except: 
        print("""Error: el mensaje no pudo enviarse. 
        Compruebe que el mensaje no tenga acentos""")


query = """query searchOccurrence{
                searchOccurrence(q:"proyecto:FY001 OR proyecto:FZ001 OR proyecto:FZ002 OR proyecto:FZ003 OR proyecto:FZ007 OR proyecto:FZ014 OR proyecto:FZ015 OR proyecto:FZ016 OR proyecto:FZ018 OR proyecto:FZ023 OR proyecto:Z003 OR proyecto:Z004 OR proyecto:Z005 OR proyecto:Z006 OR proyecto:NM003 OR proyecto:NM002"){
                    edges{
                    node{
                        id,
                        proyecto: projectId,
                        procedencia: basisOfRecord,
                        fecha_colecta_observacion: eventDate,
                        numero_colecta_observacion: recordNumber,
                        colector_observador: recordedBy,
                        coleccion: collectionCode,
                        numero_catalogo: catalogNumber,
                        individuos_copias: individualCount,
                        preparacion: preparations,
                        sexo: sex,
                        fecha_determinacion: dateIdentified,
                        determinador: identifiedBy,
                        calificador_determinacion: identificationQualifier,
                        determinacion_tipo: typeStatus,
                        licencia_uso: license,
                        referencias: references,
                        forma_citar: bibliographicCitation,
                        autorizacion_informacion: accessRights,
                        taxon{
                            taxon_id: id
                        }
                    }
                    cursor
                }
                pageInfo{
                    endCursor
                    hasNextPage
                }
                }
            }"""

r = requests.post(path_zacatuche, json={'query': query})

json_data = json.loads(r.text)
code=r.status_code
response_json_len=len(json_data['data']['searchOccurrence']['edges'])

if code==200 and response_json_len>0:
    string="Todo esta bien, se encontraron "+str(response_json_len)+" registros en la consulta." 
    destinatarios = ["Vivian <vbass@conabio.gob.mx>"]
    sendeMail(string,destinatarios)
else:
    string="ALGO ESTA MAL, REVISA YA. SE ENCONTRARON "+str(response_json_len)+" REGISTROS EN LA CONSULTA Y EL ESTATUS CODE ES "+str(code)+". LA CONSULTA QUE SE REALIZO ES "+str(query)
    destinatarios = ["Vivian <vbass@conabio.gob.mx>","Juan <jbarrios@conabio.gob.mx>"]
    sendeMail(string,destinatarios)
