import json
from numpy import true_divide
import pandas as pd
import requests
import smtplib 
import warnings
warnings.filterwarnings('ignore')

# local import
from paths import *

def loginListado():

    # credential for login to zendro
    auth = {
        "username": username,
        "password": password,
        "client_id": client_id,
        "grant_type": grant_type
    }

    # make a post to a zendro-keycloak endpoint to retrieve session token
    login = requests.post(
        listado_token,
        verify=False,
        data=auth
    )

    # if status code in the response is 200, then the request was successful and we have
    # the session token we need in the login response
    if login.status_code == 200:
        
        # we create a session object to use it for the requests to zendro api
        session = requests.Session()

        # and store the token we receive in the 'Authorization' header as a Bearer token
        session.headers.update({
            "Authorization": "Bearer " + login.json()["access_token"]
        })
        
        print("Successful login")
        return session


def get_pendientes():
    query = """{
            agrobiodiversidads(pagination:{limit:5000} search:{field:id, value:"%pendiente%", operator:like}){
                id
                taxon
                categoria_agrobiodiversidad
                es_parientesilvestre
                es_domesticado
                es_quelite
                comentarios_revision

            }
            }"""

    r = session.post(path_siagro, json={'query': query}, verify=False)
    json_data = json.loads(r.text)
    json_data = json_data['data']['agrobiodiversidads']
    actual=pd.read_csv(path_actual, keep_default_na=False)   
    anterior=pd.read_csv(path_anterior, keep_default_na=False)   
    #print(json_data['data']['agrobiodiversidads'])
    aux=""
    for i in range (len(json_data)):
        #print(json_data[i]['taxon'])
        res=search_taxon(json_data[i],actual,anterior)
        aux=aux + res 

    if aux != "":
        sendeMail(aux)    


def is_equal(info,json_data):
    if (info['taxon'] == json_data['taxon']) and (info['categoria_agrobiodiversidad'] == json_data['categoria_agrobiodiversidad']) and (info['es_parientesilvestre'] == json_data['es_parientesilvestre']) and (info['es_domesticado'] == json_data['es_domesticado']) and (info['es_quelite'] == json_data['es_quelite']):
        return True
    else:
        return False


def delete_pendiente(id):
    print("borrar: ", id)
    query = f'''mutation{{
                deleteAgrobiodiversidad(id:"{id}")
                }}'''
    #print(query)
    session.post(path_siagro, json={'query': query}, verify=False)


def sendeMail(string):
    '''
    Envía un correo a las direcciones en "destinatario". 
    Recibe como parámetro un string con los ids a los que se necesita dar seguimiento.
    '''
    remitente = "SIAgro <siagro@siagro.conabio.gob.mx>" 
    #destinatario = ["Vivian <vivbass4@gmail.com>", "Vivian <vbass@conabio.gob.mx>", "Alicia <amastretta@conabio.gob.mx>", "Irene <iramos@conabio.gob.mx>"]
    destinatario = ["Vivian <vbass@conabio.gob.mx>"]
    asunto = "Revisar taxones con id pendiente" 
    mensaje = """La siguiente lista de taxones pendientes tiene similitudes con los taxones validos indicados, favor de revisar los campos categoria_agrobiodiversidad, es_parientesilvestre, es_domesticado y es_quelite.

 ID pendiente | Taxon valido

"""+string+"""
    
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


def is_new(id,actual,anterior):
    if (actual['id'].isin([id]).any()) and (anterior['id'].isin([id]).any() == False):
        return True
    else:
        return False

def search_taxon(info,actual,anterior):
    #print("taxon:", taxon)
    taxon_split=info['taxon'].split(' ')
    #print("taxon array:", taxon)
    taxon_p = "%"

    for i in taxon_split:
        taxon_p =  taxon_p + i + "%"
    
    #print("taxon_p:", taxon_p)
    query = """{
            agrobiodiversidads(pagination:{limit:50} search:{operator:and search:[{field:taxon, value:"""+"\""+taxon_p+"\""+""", operator:like}, {field:id value:"%pendiente%" operator:notLike}]}){
                id
                taxon
                categoria_agrobiodiversidad
                es_parientesilvestre
                es_domesticado
                es_quelite
            }
        }"""

    #print(query)
    r = session.post(path_siagro, json={'query': query}, verify=False)
    json_data = json.loads(r.text)
    json_data = json_data['data']['agrobiodiversidads']
    formail=""
    if len(json_data) > 0 :
        for i in range(len(json_data)):
            
            #print(json_data[0]['taxon'])
            if is_equal(info,json_data[i]):
                delete_pendiente(info['id'])

            else:
                if is_new(json_data[i]['id'],actual,anterior):
                    formail=formail + info['id'] + " | " + json_data[i]['id'] +"\n" 

    return formail            

if __name__ == '__main__':
    print("Empieza check_pendiente archivos...")
    session=loginListado()
    get_pendientes()